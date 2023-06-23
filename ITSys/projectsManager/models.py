from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


class Project(models.Model):

    UserModel = get_user_model()

    """
    Type choice
    """
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
    title = models.CharField(max_length=128, verbose_name='titreproject')
    description = models.CharField(max_length=2048, verbose_name='descriptionproject')
    type = models.CharField(max_length=16, choices=TYPES_ALT)
    author_user_id = models.ManyToManyField(
        UserModel,
        through='Contributors',
        related_name='contributs')

    def __str__(self):
        return self.title


class Issue(models.Model):

    UserModel = get_user_model()

    """
    Tag choice
    """
    BUG = 'BUG'
    IMPROVEMENT = 'IMPROVEMENT'
    TASK = 'TASK'
    TAGS_CHOICES = (
        (BUG, 'Bug'),
        (IMPROVEMENT, 'Improvement'),
        (TASK, 'Task')
    )

    """
    Priority choice
    """
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    PRIORITY_CHOICES = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High')
    )

    """
    Status choice
    """
    TODO = 'TODO'
    WIP = 'WIP'
    DONE = 'DONE'
    STATUS_CHOICES = (
        (TODO, 'To-do'),
        (WIP, 'WIP'),
        (DONE, 'Done')
    )

    created_time = models.DateTimeField(auto_now_add=True)

    issue_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=128, verbose_name='titreissue')
    desc = models.CharField(max_length=2048, verbose_name='descriptionissue')
    tag = models.CharField(max_length=12, choices=TAGS_CHOICES)
    priority = models.CharField(max_length=12, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(to=Project,
                                   on_delete=models.CASCADE,
                                   related_name='issues')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='issue_author')
    assignee_user_id = models.ForeignKey(to=UserModel,
                                         on_delete=models.CASCADE,
                                         default=author_user_id,
                                         related_name='issue_assignee')

    def __str__(self):
        return self.title


class Comment(models.Model):

    created_time = models.DateTimeField(auto_now_add=True)

    comment_id = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=2048, 
                                   verbose_name='descriptioncomment')
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='comment_author')
    issue_id = models.ForeignKey(to=Issue,
                                 on_delete=models.CASCADE,
                                 related_name='comments')

    def __str__(self):
        return f'comment_number_{str(self.comment_id)}'


class Contributors(models.Model):

    """
    Permission (Perm) choice
    """
    CONTRIBUTOR_PERMISSION = 'CONTRIBUTOR_PERMISSION'
    AUTHOR_PERMISSION = 'AUTHOR_PERMISSION'
    PERMS_ALT = (
        (CONTRIBUTOR_PERMISSION, 'contributorsPermission'),
        (AUTHOR_PERMISSION, 'authorPermission')
    )

    """
    Role choice
    """
    CONTRIBUTOR = 'CONTRIBUTOR'
    AUTHOR = 'AUTHOR'
    ROLE_ALT = (
        (CONTRIBUTOR, 'contributor'),
        (AUTHOR, 'author')
    )

    user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    project_id = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE)

    permission = models.CharField(max_length=25, choices=PERMS_ALT)
    role = models.CharField(max_length=25, choices=ROLE_ALT)

    class Meta:
        unique_together = ('user_id', 'project_id',)
