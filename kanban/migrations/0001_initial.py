# Generated by Django 2.2.16 on 2020-09-29 13:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects_owner', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(blank=True, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'creation_date')},
            },
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=500, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField(null=True)),
                ('status', models.CharField(choices=[('todo', 'TODO'), ('in progress', 'IN_PROGRESS'), ('review', 'REVIEW'), ('done', 'DONE')], default='todo', max_length=32)),
                ('assignee', models.ManyToManyField(blank=True, related_name='issues', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues_owner', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_issues', to='kanban.Project')),
            ],
            options={
                'unique_together': {('title', 'creation_date')},
            },
        ),
    ]