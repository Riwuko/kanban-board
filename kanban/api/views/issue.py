from kanban.api.serializers import IssueSerializer
from kanban.models.issue import Issue
from rest_framework import viewsets


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
