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
from rest_framework import generics
from django.shortcuts import get_object_or_404


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related("users")
    serializer_class = ProjectListSerializer
    permission_classes = [AllowAny]
    detail_serializer_class = ProjectSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class

        return super(ProjectViewSet, self).get_serializer_class()


class ProjectUsers(generics.ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = AssignUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        project_pk = self.kwargs["pk"]
        return self.queryset.filter(projects__pk=project_pk)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs.get("pk"))
        user_email = request.data.get("email")
        user = get_object_or_404(UserAccount, email=user_email)
        project.users.add(user)
        return Response({"users": user.email})


class ProjectIssues(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        project_pk = self.kwargs["pk"]
        return self.queryset.filter(project__pk=project_pk)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs.get("pk"))
        issue, created = Issue.objects.get_or_create(
            title=request.data.get("title"),
            description=request.data.get("description"),
            status=request.data.get("status", Issue.TODO),
            due_date=request.data.get("due_date"),
            project=project,
            owner=self.request.user,
        )

        project.project_issues.add(issue)
        return Response({"issue": issue.title})
