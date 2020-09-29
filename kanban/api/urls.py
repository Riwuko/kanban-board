from django.urls import path
from kanban.api.views.issue import IssueViewSet
from kanban.api.views.project import ProjectViewSet

app_name = "kanban"

issue_detail = IssueViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
    }
)

issue_create = IssueViewSet.as_view(
    {
        "post": "create",
    }
)

project_list = ProjectViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)
project_detail = ProjectViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
    }
)

urlpatterns = [
    path("projects/", project_list, name="project-list"),
    path("projects/<int:pk>/", project_detail, name="project-detail"),
    path("issues/<int:pk>/", issue_detail, name="issue-detail"),
    path("issues/create/", issue_create, name="issue-create"),
]
