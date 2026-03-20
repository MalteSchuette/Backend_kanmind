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
    """Serializer for displaying full task
      details including nested user info."""

    assignee = UserMinimalSerializer(read_only=True)
    reviewer = UserMinimalSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status',
            'priority', 'assignee', 'reviewer', 'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):
        """Returns the total number of comments on the task."""
        return obj.comments.count()


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating a task."""

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        required=False,
        allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            'board', 'title', 'description', 'status',
            'priority', 'assignee_id', 'reviewer_id', 'due_date'
        ]

    def validate(self, data):
        """Ensures assignee and reviewer are members of the board."""
        board = data.get('board')
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')
        if board and assignee:
            if assignee not in board.members.all() and assignee != board.owner:
                raise serializers.ValidationError(
                    'Assignee must be a member of the board.'
                )
        if board and reviewer:
            if reviewer not in board.members.all() and reviewer != board.owner:
                raise serializers.ValidationError(
                    'Reviewer must be a member of the board.'
                )
        return data


class TaskPatchSerializer(serializers.ModelSerializer):
    """Serializer for updating a
    task - board cannot be changed."""

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        required=False,
        allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            'title', 'description', 'status',
            'priority', 'assignee_id', 'reviewer_id', 'due_date'
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for displaying comment
      details including nested author info."""

    author = serializers.CharField(source='author.fullname', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']


class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new comment."""

    class Meta:
        model = Comment
        fields = ['content']
