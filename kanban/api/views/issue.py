from kanban.api.serializers import IssueSerializer
from kanban.models.issue import Issue
from kanban.tasks import (
    issue_assignee_change_notification,
    issue_due_time_notification,
)
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from user_account.api.serializers import AssignUserSerializer
from user_account.models.user_account import UserAccount
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.select_related("assignee", "project")
    serializer_class = IssueSerializer
    permission_classes = [AllowAny]

    def perform_update(self, serializer):
        previous_due_date = serializer.instance.due_date
        instance = serializer.save()

        if instance.due_date != previous_due_date and instance.assignee is not None:
            issue_due_time_notification.apply_async(
                [instance.pk], eta=instance.due_date
            )

        return instance


class IssueAssignee(generics.ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = AssignUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        issue_pk = self.kwargs["pk"]
        return self.queryset.filter(issues__pk=issue_pk)

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=self.kwargs.get("pk"))
        user = get_object_or_404(UserAccount, email=request.data.get("email"))

        if not issue.project.users.filter(pk=user.pk).exists():
            return Response({"response": "User must belong to the project"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        self._check_assignee_change(issue, user)
        issue.save(update_fields=["assignee"])
        content = {"email": issue.assignee.email}
        return Response(content, status=status.HTTP_201_CREATED)

    def _check_assignee_change(self, issue, user):
        previous_assignee = issue.assignee
        issue.assignee = user

        previous_assignee_email = getattr(previous_assignee, "email", None)

        if issue.assignee != previous_assignee:
            issue_assignee_change_notification.apply_async(
                [
                    issue.title,
                    issue.assignee.email,
                    previous_assignee_email,
                ]
            )
