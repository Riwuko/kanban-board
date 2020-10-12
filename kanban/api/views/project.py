from django.db.models import Q
from kanban.api.serializers import (
    AssigneeSerializer,
    IssueSerializer,
    ProjectListSerializer,
    ProjectSerializer,
    AssignIssueSerializer,
)
from kanban.models.issue import Issue
from kanban.models.project import Project
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from user_account.models import UserAccount
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import status


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related("users")
    list_serializer_class = ProjectListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class

        return self.serializer_class

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user) | Q(users__pk=self.request.user.pk)
        )


class ProjectUsers(generics.ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = AssigneeSerializer

    def get_queryset(self):
        return self.queryset.filter(projects__pk=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs.get("pk"))
        user = get_object_or_404(UserAccount, email=request.data.get("email"))

        project.users.add(user)
        serializer = self.serializer_class(user)
        return Response({"users": serializer.data}, status=status.HTTP_200_OK)


class ProjectIssues(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self):
        return self.queryset.filter(project__pk=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs.get("pk"))
        issue = get_object_or_404(Issue, id=request.data.get("id"))

        project.project_issues.add(issue)
        serializer = self.serializer_class(issue)
        return Response({"issues": serializer.data}, status=status.HTTP_200_OK)
