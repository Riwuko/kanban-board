from kanban.api.serializers import IssueSerializer, AssigneeSerializer
from kanban.models.issue import Issue
from kanban.tasks import (
    issue_assignee_change_notification,
    issue_due_time_notification,
)
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from user_account.models.user_account import UserAccount
from django.shortcuts import get_object_or_404
from rest_framework import status


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.select_related("assignee", "project")
    serializer_class = IssueSerializer

    def _update_due_date(self, instance, previous_due_date):
        if instance.due_date != previous_due_date and instance.assignee is not None:
            issue_due_time_notification.apply_async(
                [instance.pk], eta=instance.due_date
            )

    def perform_update(self, serializer):
        previous_due_date = serializer.instance.due_date
        instance = serializer.save()

        self._update_due_date(instance, previous_due_date)
        return instance


class IssueAssignee(generics.ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = AssigneeSerializer

    def get_queryset(self):
        return self.queryset.filter(issues__pk=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=self.kwargs.get("pk"))
        user = get_object_or_404(UserAccount, email=request.data.get("email"))

        if not issue.project.users.filter(pk=user.pk).exists():
            return Response(
                {"error": "User must belong to the project"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        self._update_assignee(issue, user)
        issue.save(update_fields=["assignee"])
        serializer = self.serializer_class(issue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _update_assignee(self, issue, user):
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
