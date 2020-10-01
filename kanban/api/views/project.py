from django.db.models import Q
from kanban.api.serializers import IssueSerializer, ProjectSerializer
from kanban.models.issue import Issue
from kanban.models.project import Project
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from user_account.api.serializers import AssignUserSerializer
from user_account.models import UserAccount


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related("users")
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user) | Q(users__pk=self.request.user.pk)
        )

    @action(
        detail=True, methods=["get", "post"], url_path="users", url_name="project-user"
    )
    def project_users(self, request, pk=None):
        self.serializer_class = AssignUserSerializer
        if request.method == "GET":
            return self.get_project_users(request, pk)
        if request.method == "POST":
            return self.set_project_users(request, pk)

    def set_project_users(self, request, pk):
        project = self.get_object()
        user_email = request.data.get("email")
        try:
            user = UserAccount.objects.get(email=user_email)
        except UserAccount.DoesNotExist:
            return Response({"status": "Not a proper user."})
        else:
            if not project.users.filter(pk=user.pk).exists():
                project.users.add(user)
                return Response({"status": "User assigned to project."})
            return Response({"status": "User already assigned to project."})

    def get_project_users(self, request, pk):
        project = self.get_object()
        users = project.users.values("email")
        return Response({"Project users": users})

    @action(
        detail=True,
        methods=["get", "post"],
        url_path="issues",
        url_name="project-issues",
    )
    def project_issues(self, request, pk=None):
        self.serializer_class = IssueSerializer
        if request.method == "GET":
            return self.get_project_issues(request, pk)
        if request.method == "POST":
            return self.set_project_issues(request, pk)

    def set_project_issues(self, request, pk):
        project = self.get_object()
        issue, created = Issue.objects.get_or_create(
            title=request.data.get("title"),
            description=request.data.get("description"),
            status=request.data.get("status", Issue.TODO),
            due_date=request.data.get("due_date"),
            project=project,
            owner=self.request.user,
        )
        if created:
            project.project_issues.add(issue)
            return Response({"status": "Issue added to project."})
        return Response({"status": "Issue already assigned to project."})

    def get_project_issues(self, request, pk):
        project = self.get_object()
        issues = project.project_issues.values("title")
        return Response({"Project users": issues})
