from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT

from tasks_app.api.serializers import TaskSerializer, TaskCreateSerializer, CommentSerializer, CommentCreateSerializer
from tasks_app.api.permissions import IsTaskBoardMemberOrOwner, IsCommentAuthor
from tasks_app.models import Task, Comment


class AssignedToMeView(APIView):
    """Returns all tasks assigned to the authenticated user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns a list of tasks where the user is the assignee."""
        return Response(TaskSerializer(request.user.assigned_tasks.all(), many=True).data)


class ReviewedByMeView(APIView):
    """Returns all tasks where the authenticated user is the reviewer."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns a list of tasks where the user is the reviewer."""
        return Response(TaskSerializer(request.user.reviewed_tasks.all(), many=True).data)


class TasksView(APIView):
    """Handles task creation."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Creates a new task and returns the full task details."""
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    """Handles updating and deleting a single task."""

    permission_classes = [IsAuthenticated]

    def get_task(self, task_id):
        """Returns a task by ID or None if not found."""
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None

    def patch(self, request, task_id):
        """Partially updates a task."""
        task = self.get_task(task_id)
        if not task:
            return Response({'error': 'Task not found'}, status=HTTP_404_NOT_FOUND)
        if not IsTaskBoardMemberOrOwner().has_object_permission(request, self, task):
            return Response({'error': 'You do not have permission'}, status=HTTP_403_FORBIDDEN)
        serializer = TaskCreateSerializer(
            task, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(TaskSerializer(serializer.save()).data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        """Deletes a task if the user is a board member or owner."""
        task = self.get_task(task_id)
        if not task:
            return Response({'error': 'Task not found'}, status=HTTP_404_NOT_FOUND)
        if not IsTaskBoardMemberOrOwner().has_object_permission(request, self, task):
            return Response({'error': 'You do not have permission'}, status=HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class TaskCommentListView(APIView):
    """Handles listing and creating comments for a task."""

    permission_classes = [IsAuthenticated]

    def get_task(self, task_id):
        """Returns a task by ID or None if not found."""
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None

    def get(self, request, task_id):
        """Returns all comments for a specific task."""
        task = self.get_task(task_id)
        if not task:
            return Response({'error': 'Task not found'}, status=HTTP_404_NOT_FOUND)
        if not IsTaskBoardMemberOrOwner().has_object_permission(request, self, task):
            return Response({'error': 'You do not have permission'}, status=HTTP_403_FORBIDDEN)
        return Response(CommentSerializer(task.comments.all(), many=True).data)

    def post(self, request, task_id):
        """Creates a new comment on a task."""
        task = self.get_task(task_id)
        if not task:
            return Response({'error': 'Task not found'}, status=HTTP_404_NOT_FOUND)
        if not IsTaskBoardMemberOrOwner().has_object_permission(request, self, task):
            return Response({'error': 'You do not have permission'}, status=HTTP_403_FORBIDDEN)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(author=request.user, task=task)
            return Response(CommentSerializer(comment).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TaskCommentDetailView(APIView):
    """Handles deleting a single comment."""

    permission_classes = [IsAuthenticated]

    def delete(self, request, task_id, comment_id):
        """Deletes a comment if the user is the author."""
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=HTTP_404_NOT_FOUND)
        if not IsCommentAuthor().has_object_permission(request, self, comment):
            return Response({'error': 'You do not have permission'}, status=HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=HTTP_204_NO_CONTENT)
