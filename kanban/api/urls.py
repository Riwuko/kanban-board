from django.urls import path
from kanban.api.views.project import ProjectViewSet

app_name = "kanban"

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
]
