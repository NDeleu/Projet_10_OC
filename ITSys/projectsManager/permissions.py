from rest_framework.permissions import BasePermission
from .models import Project, Issue, Comment, Contributors


class ContributorsViewsetPermission(BasePermission):

    """
    Permission on Contributors management (views.UserViewset).
    CONTRIBUTOR with CONTRIBUTOR_PERMISSION
    have permission to get list and retrieve,
    AUTHOR with AUTHOR_PERMISSION
    have permission to get list and retrieve, create and delete.
    """

    message = 'Permission required'

    def check_contribution(self, user, project, authorizedrole):
        for contributor in Contributors.objects.filter(project_id=project.project_id):
            if user == contributor.user_id:
                if contributor.permission in authorizedrole:
                    return True
        return False

    def has_permission(self, request, view):
        if not request.user and request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'list']:
            return self.check_contribution(request.user, Project.objects.filter(project_id=view.kwargs['projects_pk'])[0], ['CONTRIBUTOR_PERMISSION', 'AUTHOR_PERMISSION'])
        elif view.action in ['update', 'partial_update', 'create', 'destroy']:
            if Contributors.objects.filter(project_id=view.kwargs['projects_pk'], user_id=request.user):
                return True
            else:
                return False


class CategoryViewsetPermission(BasePermission):

    """
    Permission on Categories management
    (views.ProjectViewset, views.IssueViewset, views.CommentViewset).
    User identified can create project.
    CONTRIBUTOR with CONTRIBUTOR_PERMISSION
    have permission to get list and retrieve for project
    and get list and retrive and create for issue and comment,
    AUTHOR with AUTHOR_PERMISSION for project
    and author_user_id for issue and comment
    have permission to get list and retrieve, create update and delete.
    """

    message = 'Permission required'

    def check_contribution(self, user, project, authorizedrole):
        for contributor in Contributors.objects.filter(project_id=project.project_id):
            if user == contributor.user_id:
                if contributor.permission in authorizedrole:
                    return True
        return False

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if obj.__class__ == Project:
            if view.action in ['list', 'retrieve']:
                return self.check_contribution(request.user, obj, ['CONTRIBUTOR_PERMISSION', 'AUTHOR_PERMISSION'])
            elif view.action in ['update', 'partial_update', 'destroy']:
                return self.check_contribution(request.user, obj, 'AUTHOR_PERMISSION')
            return True
        elif obj.__class__ == Issue:
            if view.action in ['list', 'create', 'retrieve']:
                return self.check_contribution(request.user, obj.project_id, ['CONTRIBUTOR_PERMISSION', 'AUTHOR_PERMISSION'])
            elif view.action in ['update', 'partial_update', 'destroy']:
                return bool(request.user == obj.author_user_id)
        elif obj.__class__ == Comment:
            if view.action in ['list', 'create', 'retrieve']:
                return self.check_contribution(request.user, obj.issue_id.project_id, ['CONTRIBUTOR_PERMISSION', 'AUTHOR_PERMISSION'])
            elif view.action in ['update', 'partial_update', 'destroy']:
                return bool(request.user == obj.author_user_id)
