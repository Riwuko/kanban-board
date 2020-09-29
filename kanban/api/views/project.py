from django.db.models import Q
from kanban.api.serializers import ProjectSerializer
from kanban.models.project import Project
from rest_framework import viewsets


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user) | Q(users__pk=self.request.user.pk)
        )
