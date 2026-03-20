# permissions.py
from rest_framework.permissions import BasePermission


class IsTaskBoardMemberOrOwner(BasePermission):
    """Allows access only to members or the owner of the board the task belongs to."""

    def has_object_permission(self, request, view, obj):
        """Returns True if the user is the owner or a member of the task's board."""
        board = obj.board
        return request.user == board.owner or request.user in board.members.all()


class IsCommentAuthor(BasePermission):
    """Allows access only to the author of the comment."""

    def has_object_permission(self, request, view, obj):
        """Returns True if the user is the author of the comment."""
        return request.user == obj.author
