from django.db import models
from user_account.models.user_account import UserAccount


class Project(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(
        UserAccount, related_name="projects_owner", on_delete=models.CASCADE, null=False
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(UserAccount, related_name="projects", blank=True)

    def __str__(self):
        return f"{self.owner} : {self.name}"

    class Meta:
        unique_together = (
            "name",
            "creation_date",
        )
