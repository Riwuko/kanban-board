from django.shortcuts import get_object_or_404
from kanban.models.issue import Issue
from kanban.models.project import Project
from rest_framework import serializers
from user_account.models.user_account import UserAccount


class UserAccountRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            user = UserAccount.objects.get(email=data)
        except UserAccount.DoesNotExist:
            user = get_object_or_404(UserAccount, id=data)
        return user


class IssueSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault())
    )
    owner_email = serializers.CharField(source="owner.email")
    project_name = serializers.CharField(source="project.name")
    assignee = UserAccountRelatedField(many=True, queryset=UserAccount.objects.all())

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
            "status": {"required": False},
            "project": {"write_only": True},
            "owner_email": {"read_only": True},
            "project_name": {"read_only": True},
        }


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault())
    )
    owner_email = serializers.CharField(source="owner.email", read_only=True)
    project_issues = serializers.SlugRelatedField(many=True, slug_field="title", read_only=True)
    users = UserAccountRelatedField(many=True, queryset=UserAccount.objects.all(), required=False)

    class Meta:
        model = Project
        fields = [
            "name",
            "owner",
            "owner_email",
            "users",
            "project_issues",
        ]
