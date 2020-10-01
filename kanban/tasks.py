from config.celery import app
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from kanban.models.issue import Issue


@app.task()
def issue_due_time_notification(issue_pk):

    try:
        issue = Issue.objects.get(pk=issue_pk)
    except Issue.DoesNotExist:
        return
    else:
        if issue.status != Issue.DONE:
            subject = "Task finished with status not done!"
            html_message = render_to_string(
                "email_templates/issue_due_time_notification.html", {"context": issue}
            )
            plain_message = strip_tags(html_message)
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [issue.assignee.email],
                html_message=html_message,
                fail_silently=False,
            )


@app.task()
def issue_assignee_change_notification(issue_title, assignee, previous_assignee):
    subject = "Issue asignee has changed"
    context = {
        "issue_title": issue_title,
        "assignee": assignee,
        "previous_assignee": previous_assignee,
    }
    html_message = render_to_string(
        "email_templates/assignee_change_notification.html", {"context": context}
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [assignee, previous_assignee],
        html_message=html_message,
        fail_silently=False,
    )
