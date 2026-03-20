from rest_framework.permissions import BasePermission


class IsBoardMemberOrOwner(BasePermission):
    """Allows access only to board members or the board owner."""

    def has_object_permission(self, request, view, obj):
        """Returns True if the user is the owner or a member of the board."""
        return request.user == obj.owner or request.user in obj.members.all()


class IsBoardOwner(BasePermission):
    """Allows access only to the board owner."""

    def has_object_permission(self, request, view, obj):
        """Returns True if the user is the owner of the board."""
        return request.user == obj.owner
