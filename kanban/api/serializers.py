from kanban.models.issue import Issue
from kanban.models.project import Project
from rest_framework import serializers
from rest_framework.reverse import reverse
from user_account.api.serializers import UserAccountSerializer
from user_account.models.user_account import UserAccount


class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["email"]


class IssueSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault())
    )
    assignee = AssigneeSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "status",
            "owner",
            "assignee",
            "project",
        ]
        extra_kwargs = {
            "description": {"required": False},
            "due_date": {"required": False},
            "status": {"required": False},
        }


class IssueListSerializer(serializers.ModelSerializer):
    assignee = AssigneeSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "due_date",
            "status",
            "assignee",
        ]


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "owner",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault())
    )
    users = AssigneeSerializer(many=True, read_only=True)
    project_issues = IssueListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "owner",
            "users",
            "project_issues",
        ]


class AssignIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id"]
