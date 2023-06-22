from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from .permissions import CategoryViewsetPermission, \
    ContributorsViewsetPermission

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_200_OK

from django.db import transaction, IntegrityError

from django.contrib.auth import get_user_model
from .models import Project, Issue, Comment, Contributors
from .serializers import ProjectListSerializer, ProjectDetailSerializer, \
    ProjectCreateSerializer, ProjectUpdateSerializer, \
    IssueListSerializer, IssueDetailSerializer, IssueCreateSerializer, \
    IssueUpdateSerializer, \
    CommentListSerializer, CommentDetailSerializer, CommentCreateSerializer, \
    CommentUpdateSerializer, \
    UserListSerializer, UserDetailSerializer, UserCreateSerializer


class MultipleSerializerMixin:
    detail_serializer_class = None
    create_serializer_class = None
    update_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None :
            return self.detail_serializer_class
        elif self.action == 'create' and self.create_serializer_class is not None :
            return self.create_serializer_class
        elif self.action == 'update' and self.update_serializer_class is not None :
            return self.update_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    create_serializer_class = ProjectCreateSerializer
    update_serializer_class = ProjectUpdateSerializer

    http_method_names = ['get', 'post', 'put', 'delete']

    permission_classes = (CategoryViewsetPermission,)

    def get_queryset(self):
        return Project.objects.filter(project_id__in=[contributor.project_id.id for contributor in Contributors.objects.filter(user_id=self.request.user).all()])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            project = Project.objects.create(**serializer.validated_data)
            project.project_id = project.pk
            project.save()
            project.author_user_id.add(
                request.user.user_id,
                through_defaults={
                    'permission': 'AUTHOR_PERMISSION',
                    'role': 'AUTHOR'
                })
            project.save()
            response = {'project_id': project.project_id, 'title': project.title, 'description': project.description, 'type': project.type, 'author_user_id': Contributors.objects.filter(role='AUTHOR')[0].user_id.user_id}
            return Response(response, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return super(ProjectViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(ProjectViewset, self).destroy(request, *args, **kwargs)


class UserViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    create_serializer_class = UserCreateSerializer

    http_method_names = ['get', 'post', 'delete']

    permission_classes = (ContributorsViewsetPermission,)

    def get_queryset(self):
        return get_user_model().objects.filter(user_id__in=[contributor.user_id.id for contributor in Contributors.objects.filter(project_id=self.kwargs['projects_pk'])])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            add_user = get_user_model().objects.filter(email=request.data['email'])[0]
            if add_user:
                contributor = Contributors.objects.create(
                    user_id=add_user,
                    project_id=Project.objects.filter(project_id=self.kwargs['projects_pk'])[0],
                    permission='CONTRIBUTOR_PERMISSION',
                    role='CONTRIBUTOR'
                )
                contributor.save()
                response = {
                    'user_id': add_user.user_id,
                    'project_id': Project.objects.filter(project_id=self.kwargs['projects_pk'])[0].project_id,
                    'permission': 'CONTRIBUTOR_PERMISSION',
                    'role': 'CONTRIBUTOR'
                    }
                return Response(response, status=HTTP_201_CREATED)
            response = {'errors': 'No user responds to this email'}
            return Response(response, status=HTTP_400_BAD_REQUEST)
        except IntegrityError:
            response = {'error': 'User with this email already added'}
            return Response(response, status=HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        del_user = get_user_model().objects.filter(user_id=self.kwargs['pk'])[0]
        if del_user:
            if del_user == request.user:
                response = {'errors': 'Main author user cannot be deleted'}
                return Response(response, status=HTTP_400_BAD_REQUEST)
            del_contributor = Contributors.objects.filter(user_id=self.kwargs['pk'], project_id=self.kwargs['projects_pk'])[0]
            if del_contributor:
                del_contributor.delete()
                return Response()
            response = {'errors': 'Main author is not a contributor on this project'}
            return Response(response, status=HTTP_400_BAD_REQUEST)
        response = {'errors': 'No user responds to this email'}
        return Response(response, status=HTTP_400_BAD_REQUEST)


class IssueViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    create_serializer_class = IssueCreateSerializer
    update_serializer_class = IssueUpdateSerializer

    http_method_names = ['get', 'post', 'put', 'delete']

    permission_classes = (CategoryViewsetPermission,)

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['projects_pk'])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = IssueCreateSerializer(data=request.data)
        if serializer.is_valid():
            author_user_id = request.user
            if serializer.validated_data['email_assignee']:
                if get_user_model().objects.filter(email=serializer.validated_data['email_assignee']).exists():
                    assignee_user_id = get_user_model().objects.filter(email=serializer.validated_data['email_assignee'])[0]
                else:
                    assignee_user_id = author_user_id
            else:
                assignee_user_id = author_user_id
            issue = Issue.objects.create(
                title=serializer.validated_data['title'],
                desc=serializer.validated_data['desc'],
                tag=serializer.validated_data['tag'],
                priority=serializer.validated_data['priority'],
                project_id=Project.objects.filter(project_id=self.kwargs['projects_pk'])[0],
                status=serializer.validated_data['status'],
                author_user_id=author_user_id,
                assignee_user_id=assignee_user_id
            )
            issue.save()

            issue.issue_id = issue.pk
            issue.save()
            response = {'issue_id': issue.issue_id, 'created_time': issue.created_time, 'title': issue.title, 'description': issue.desc, 'priority': issue.priority, 'tag': issue.tag, 'status': issue.status, 'author_user_id': author_user_id.user_id, 'assignee_user_id': assignee_user_id.user_id, 'project_id': int(self.kwargs['projects_pk'])}
            return Response(response, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        serializer = IssueCreateSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['email_assignee']:
                if get_user_model().objects.filter(email=serializer.validated_data['email_assignee']).exists():
                    assignee_user_id = get_user_model().objects.filter(email=serializer.validated_data['email_assignee'])[0]
                else:
                    assignee_user_id = Issue.objects.filter(issue_id=self.kwargs['pk'])[0].assignee_user_id
            else:
                assignee_user_id = Issue.objects.filter(issue_id=self.kwargs['pk'])[0].assignee_user_id
            issue = Issue.objects.filter(issue_id=self.kwargs['pk'])[0]
            issue.assignee_user_id = assignee_user_id
            issue.save()
            return super(IssueViewset, self).update(request, *args, **kwargs)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return super(IssueViewset, self).destroy(request, *args, **kwargs)


class CommentViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    create_serializer_class = CommentCreateSerializer
    update_serializer_class = CommentUpdateSerializer

    http_method_names = ['get', 'post', 'put', 'delete']

    permission_classes = (CategoryViewsetPermission,)

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issues_pk'])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            author_user_id = request.user

            comment = Comment.objects.create(
                description=serializer.validated_data['description'],
                author_user_id=author_user_id,
                issue_id=Issue.objects.filter(issue_id=self.kwargs['issues_pk'])[0],
            )
            comment.save()
            comment.comment_id = comment.pk
            comment.save()
            response = {'comment_id': comment.comment_id, 'created_time': comment.created_time, 'description': comment.description, 'author_user_id': author_user_id.user_id, 'issue_id': comment.issue_id.issue_id}
            return Response(response, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return super(CommentViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(CommentViewset, self).destroy(request, *args, **kwargs)
