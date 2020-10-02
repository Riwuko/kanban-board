from django.db.models import Q
from kanban.api.serializers import (
    IssueSerializer,
    ProjectListSerializer,
    ProjectSerializer,
)
from kanban.models.issue import Issue
from kanban.models.project import Project
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from user_account.api.serializers import AssignUserSerializer
from user_account.models import UserAccount
from rest_framework.permissions import AllowAny


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related("users")
    serializer_class = ProjectListSerializer
    permission_classes = [AllowAny]
    detail_serializer_class = ProjectSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class

        return super(ProjectViewSet, self).get_serializer_class()

    # def get_queryset(self):
    #     return self.queryset.filter(
    #         Q(owner=self.request.user) | Q(users__pk=self.request.user.pk)
    #     )

    # def get_project_users(self, request, pk):
    #     project = self.get_object()
    #     users = project.users.values("email")
    #     return Response({"Project users": users})

    # @action(
    #     detail=True,
    #     methods=["get", "post"],
    #     url_path="issues",
    #     url_name="project-issues",
    # )
    # def project_issues(self, request, pk=None):
    #     self.serializer_class = IssueSerializer
    #     if request.method == "GET":
    #         return self.get_project_issues(request, pk)
    #     if request.method == "POST":
    #         return self.set_project_issues(request, pk)

    # def set_project_issues(self, request, pk):
    #     project = self.get_object()
    #     issue, created = Issue.objects.get_or_create(
    #         title=request.data.get("title"),
    #         description=request.data.get("description"),
    #         status=request.data.get("status", Issue.TODO),
    #         due_date=request.data.get("due_date"),
    #         project=project,
    #         owner=self.request.user,
    #     )
    #     if created:
    #         project.project_issues.add(issue)
    #         return Response({"status": "Issue added to project."})
    #     return Response({"status": "Issue already assigned to project."})

    # def get_project_issues(self, request, pk):
    #     project = self.get_object()
    #     issues = project.project_issues.values("title")
    #     return Response({"Project users": issues})
