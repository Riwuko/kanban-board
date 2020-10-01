from django.db import models
from kanban.models.project import Project
from user_account.models import UserAccount


class Issue(models.Model):
    TODO = "todo"
    IN_PROGRESS = "in progress"
    REVIEW = "review"
    DONE = "done"
    STATUS = [
        (TODO, "TODO"),
        (IN_PROGRESS, "IN_PROGRESS"),
        (REVIEW, "REVIEW"),
        (DONE, "DONE"),
    ]

    title = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=500, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True, default=None)
    status = models.CharField(max_length=32, choices=STATUS, default=TODO)

    owner = models.ForeignKey(
        UserAccount,
        related_name="issues_owner",
        on_delete=models.CASCADE,
    )

    assignee = models.ForeignKey(
        UserAccount, related_name="issues", null=True, on_delete=models.SET_NULL
    )
    project = models.ForeignKey(Project, related_name="project_issues", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project} : {self.owner} : {self.title}"
