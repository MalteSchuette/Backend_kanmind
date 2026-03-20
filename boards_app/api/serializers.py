from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Board

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    """Serializer for displaying minimal user information."""

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for displaying board list with computed statistics."""

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'member_count', 'ticket_count',
            'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id'
        ]

    def get_member_count(self, obj):
        """Returns the number of members in the board."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Returns the total number of tasks in the board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Returns the number of tasks with status 'to-do'."""
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        """Returns the number of tasks with priority 'high'."""
        return obj.tasks.filter(priority='high').count()


class BoardDetailSerializer(serializers.ModelSerializer):
    """Serializer for displaying full board
      details including members and tasks."""

    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = UserMinimalSerializer(many=True, read_only=True)
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']

    def get_tasks(self, obj):
        """Returns all tasks belonging to the board."""
        from tasks_app.api.serializers import TaskSerializer
        return TaskSerializer(obj.tasks.all(), many=True).data


class BoardPatchSerializer(serializers.ModelSerializer):
    """Serializer for displaying board
      after PATCH with owner and members data."""

    owner_data = UserMinimalSerializer(source='owner', read_only=True)
    members_data = UserMinimalSerializer(
        source='members', many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data', 'members_data']


class BoardCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating a board."""

    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Board
        fields = ['title', 'members']
