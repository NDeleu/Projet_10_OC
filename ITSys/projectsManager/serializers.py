from rest_framework import serializers

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
        queryset = instance.issues.filter(active=True)
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class IssueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ('issue_id', 'created_time', 'title', 'priority',
                  'tag', 'status', 'project_id')


class IssueDetailSerializer(serializers.ModelSerializer):

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ('issue_id', 'created_time', 'title', 'description',
                  'priority', 'tag', 'status', 'author_user_id',
                  'assignee_user_id', 'project_id', 'comments')

    def get_comments(self, instance):
        queryset = instance.comments.filter(active=True)
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class CommentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('comment_id', 'created_time', 'author_user_id', 'issue_id')


class CommentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('comment_id', 'created_time', 'description',
                  'author_user_id', 'issue_id')


class ContributorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = ('user_id', 'project_id', 'permission', 'role')
