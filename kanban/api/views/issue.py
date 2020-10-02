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
