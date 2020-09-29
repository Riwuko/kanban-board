from kanban.models.project import Project
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_email = serializers.CharField(source="owner.email", read_only=True)

    class Meta:
        model = Project
        fields = [
            "name",
            "owner",
            "owner_email",
            "users",
        ]
        extra_kwargs = {
            "users": {"required": False},
        }
