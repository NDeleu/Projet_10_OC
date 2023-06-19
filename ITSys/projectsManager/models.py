from django.db import models
from django.conf import settings


class Project(models.Model):

    FRONTEND = 'FRONTEND'
    BACKEND = 'BACKEND'
    IOS = 'IOS'
    ANDROID = 'ANDROID'
    TYPES_ALT = (
        (FRONTEND, 'Front-end'),
        (BACKEND, 'Back-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android')
    )

    project_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=128, verbose_name='titre')
    description = models.CharField(max_length=2048, verbose_name='description')
    type = models.CharField(max_length=16, choices=TYPES_ALT)
    author_user_id = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Contributors',
        related_name='contributs')

    def __str__(self):
        return self.title


class Issue(models.Model):

    created_time = models.DateTimeField(auto_now_add=True)

    title =
    desc =
    tag =
    priority =
    project_id =
    status =
    author_user_id =
    assignee_user_id =

    def __str__(self):
        return self.title


class Comment(models.Model):

    created_time = models.DateTimeField(auto_now_add=True)

    comment_id =
    description =
    author_user_id =
    issue_id =

    def __str__(self):
        return 'comment_number_', self.comment_id


class Contributors(models.Model):

    user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    project_id = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE)

    permission =
    role =

    class Meta:
        unique_together = ('user_id', 'project_id',)

