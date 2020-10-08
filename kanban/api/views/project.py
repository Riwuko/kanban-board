from django.db.models import Q
from kanban.api.serializers import (
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
from user_account.api.serializers import AssignUserSerializer
from user_account.models import UserAccount
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import status


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related("users")
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class

        return self.serializer_class

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user) | Q(users__pk=self.request.user.pk)
        )


class ProjectUsers(generics.ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = AssignUserSerializer

    def get_queryset(self):
        return self.queryset.filter(projects__pk=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs.get("pk"))
        user_email = request.data.get("email")
        user = get_object_or_404(UserAccount, email=user_email)
        project.users.add(user)
        return Response({"users": user.email}, status=status.HTTP_200_OK)


class ProjectIssues(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self):
        return self.queryset.filter(project__pk=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        serializer = AssignIssueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = get_object_or_404(Project, id=self.kwargs.get("pk"))
        issue, _ = Issue.objects.get_or_create(
            title=serializer.data.get("title"),
            defaults={
                "description": serializer.data.get("description"),
                "status": serializer.data.get("status", Issue.TODO),
                "due_date": serializer.data.get("due_date"),
                "project": project,
                "owner": self.request.user,
            },
        )

        project.project_issues.add(issue)
        return Response({"issue": issue.title}, status=status.HTTP_200_OK)
