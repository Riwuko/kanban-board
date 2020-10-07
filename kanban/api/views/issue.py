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
        user_email = request.data.get("email")
        user = get_object_or_404(UserAccount, email=user_email)
        previous_assignee = issue.assignee
        issue.assignee = user

        try:
            previous_assignee_email = previous_assignee.email
        except AttributeError:
            previous_assignee_email = None

        if issue.assignee != previous_assignee:
            issue_assignee_change_notification.apply_async(
                [
                    issue.title,
                    issue.assignee.email,
                    previous_assignee_email,
                ]
            )

        issue.save(update_fields=["assignee"])
        return Response({"email": issue.assignee.email})
