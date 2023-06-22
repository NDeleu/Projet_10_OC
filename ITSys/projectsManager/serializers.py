from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Project, Issue, Comment, Contributors


class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('project_id', 'title', 'type', 'author_user_id')


class ProjectDetailSerializer(serializers.ModelSerializer):

    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('project_id', 'title',
                  'description', 'type', 'author_user_id', 'issues')

    def get_issues(self, instance):
        queryset = Issue.objects.filter(project_id=instance.project_id)
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class ProjectCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('title', 'description', 'type')


class ProjectUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('title', 'description', 'type')


class IssueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ('issue_id', 'created_time', 'title', 'priority',
                  'tag', 'status', 'project_id')


class IssueDetailSerializer(serializers.ModelSerializer):

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ('issue_id', 'created_time', 'title', 'desc',
                  'priority', 'tag', 'status', 'author_user_id',
                  'assignee_user_id', 'project_id', 'comments')

    def get_comments(self, instance):
        queryset = Comment.objects.filter(issue_id=instance.issue_id)
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class IssueCreateSerializer(serializers.ModelSerializer):

    email_assignee = serializers.EmailField(allow_null=True, allow_blank=True)

    class Meta:
        model = Issue
        fields = ('title', 'desc', 'priority', 'tag', 'status', 'email_assignee')


class IssueUpdateSerializer(serializers.ModelSerializer):

    email_assignee = serializers.EmailField(allow_null=True, allow_blank=True)

    class Meta:
        model = Issue
        fields = ('title', 'desc', 'priority',
                  'tag', 'status', 'email_assignee')


class CommentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('comment_id', 'created_time', 'author_user_id')


class CommentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('comment_id', 'created_time', 'description',
                  'author_user_id', 'issue_id')


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('description', )


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('description', )


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('user_id', 'email')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('user_id', 'email', 'first_name', 'last_name')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', )

