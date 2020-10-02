from django.urls import path, include
from kanban.api.views.issue import IssueViewSet, IssueAssignee
from kanban.api.views.project import ProjectViewSet
from rest_framework import routers

app_name = "kanban"

router = routers.SimpleRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"issues", IssueViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("issues/<int:pk>/users/", IssueAssignee.as_view(), name="issue-user"),
]
