from django.urls import path
from kanban.api.views.issue import IssueViewSet
from kanban.api.views.project import ProjectViewSet
from rest_framework import routers

app_name = "kanban"

router = routers.SimpleRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"issues", IssueViewSet)

urlpatterns = router.urls
