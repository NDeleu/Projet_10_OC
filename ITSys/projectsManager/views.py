from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from django.db import transaction, IntegrityError

from django.contrib.auth import get_user_model
from .models import Project, Issue, Comment, Contributors
from .serializers import ProjectListSerializer, ProjectDetailSerializer, \
    ProjectCreateSerializer, ProjectUpdateSerializer, \
    IssueListSerializer, IssueDetailSerializer, IssueCreateSerializer, \
    CommentListSerializer, CommentDetailSerializer, CommentCreateSerializer, \
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

    def get_queryset(self):
        return Project.objects.filter(project_id__in=[contributor.project_id.id for contributor in Contributors.objects.filter(user_id=16).all()])

    # self.request.user

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            project = Project.objects.create(**serializer.validated_data)
            project.project_id = project.pk
            project.save()
            project.author_user_id.add(
                get_user_model().objects.all()[1].user_id,
                through_defaults={
                    'permission': 'AUTHOR_PERMISSION',
                    'role': 'AUTHOR'
                })
            project.save()
            response = {'project_id': project.project_id, 'title': project.title, 'description': project.description, 'type': project.type, 'author_user_id': Contributors.objects.filter(role='AUTHOR')[0].user_id.user_id}
            return Response(response, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    #request.user
    #get_user_model().objects.filter(user_id=1)

    def update(self, request, *args, **kwargs):
        return super(ProjectViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(ProjectViewset, self).destroy(request, *args, **kwargs)


class UserViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    create_serializer_class = UserCreateSerializer

    http_method_names = ['get', 'post', 'delete']

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
            return Response(response)
        except IntegrityError:
            response = {'error': 'User with this email already added'}
            return Response(response)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):




class IssueViewset(MultipleSerializerMixin, ModelViewSet):
    pass


class CommentViewset(MultipleSerializerMixin, ModelViewSet):
    pass