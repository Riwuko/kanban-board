from kanban.models.issue import Issue
from kanban.models.project import Project
from rest_framework import serializers
from user_account.api.serializers import UserAccountSerializer


class IssueSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault())
    )
    owner_email = serializers.CharField(source="owner.email", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    assignee = UserAccountSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "status",
            "owner",
            "owner_email",
            "assignee",
            "project",
            "project_name",
        ]
        extra_kwargs = {
            "description": {"required": False},
            "due_date": {"required": False},
            "status": {"required": False},
            "project": {"write_only": True},
            "id": {"read_only": True},
        }


class IssueListSerializer(serializers.ModelSerializer):
    assignee = UserAccountSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = [
            "title",
            "due_date",
            "status",
            "assignee",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault())
    )
    owner_email = serializers.CharField(source="owner.email", read_only=True)
    users = UserAccountSerializer(many=True, read_only=True)
    project_issues = IssueListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "owner",
            "owner_email",
            "users",
            "project_issues",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }
