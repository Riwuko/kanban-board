from kanban.api.serializers import IssueSerializer
from kanban.models.issue import Issue
from kanban.tasks import issue_assignee_change_notification, issue_due_time_notification
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from user_account.api.serializers import AssignUserSerializer
from user_account.models.user_account import UserAccount


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.select_related("assignee", "project")
    serializer_class = IssueSerializer

    def perform_update(self, serializer):
        previous_due_date = serializer.instance.due_date
        instance = serializer.save()

        if instance.due_date != previous_due_date and instance.assignee is not None:
            issue_due_time_notification.apply_async([instance.pk], eta=instance.due_date)

        return instance

    @action(detail=True, methods=["get", "post"], url_path="users", url_name="issue-users")
    def issue_assignee(self, request, pk=None):
        self.serializer_class = AssignUserSerializer
        if request.method == "GET":
            return self.get_issue_assignee(request, pk)
        if request.method == "POST":
            return self.set_issue_assignee(request, pk)

    def set_issue_assignee(self, request, pk):
        issue = self.get_object()
        user_email = request.data.get("email")
        try:
            user = UserAccount.objects.get(email=user_email)
        except UserAccount.DoesNotExist:
            return Response({"status": "Not a proper user."})
        else:
            if not issue.assignee == user:
                try:
                    previous_email = issue.assignee.email
                except AttributeError:
                    previous_email = "nobody"

                issue_assignee_change_notification.apply_async(
                    [issue.title, user.email, previous_email]
                )

                issue.assignee = user
                issue.save()
                return Response(
                    {"status": "User assigned to issue.", "assignee": issue.assignee.email}
                )
            return Response({"status": "User already assigned to issue."})

    def get_issue_assignee(self, request, pk):
        issue = self.get_object()
        try:
            user = issue.assignee.email
        except AttributeError:
            user = "None"
        return Response({"Issue assignee": user})
