from kanban.models.issue import Issue
from kanban.models.project import Project
from rest_framework import serializers


class IssueSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_email = serializers.CharField(source="owner.email", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model = Issue
        fields = [
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
            "assignee": {"required": False},
            "description": {"required": False},
            "due_date": {"required": False},
            "project": {"write_only": True},
            "status": {"required": False},
        }


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_email = serializers.CharField(source="owner.email", read_only=True)
    project_issues = serializers.SlugRelatedField(
        many=True, slug_field="title", queryset=Issue.objects.all()
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "owner",
            "owner_email",
            "users",
            "project_issues",
        ]
        extra_kwargs = {
            "users": {"required": False},
        }
