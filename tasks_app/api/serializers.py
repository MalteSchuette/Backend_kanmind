from rest_framework import serializers
from django.contrib.auth import get_user_model
from tasks_app.models import Task, Comment

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    """Serializer for displaying minimal user information."""

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for displaying full task details including nested user info."""

    assignee = UserMinimalSerializer(read_only=True)
    reviewer = UserMinimalSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status',
                  'priority', 'assignee', 'reviewer', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        """Returns the total number of comments on the task."""
        return obj.comments.count()


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating a task."""

    class Meta:
        model = Task
        fields = ['board', 'title', 'description', 'status',
                  'priority', 'assignee', 'reviewer', 'due_date']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for displaying comment details including nested author info."""

    author = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'task', 'content']


class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new comment."""

    class Meta:
        model = Comment
        fields = ['content']
