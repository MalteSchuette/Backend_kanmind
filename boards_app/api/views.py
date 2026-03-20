# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT

from boards_app.api.serializers import BoardSerializer, BoardCreateSerializer
from boards_app.api.permissions import IsBoardMemberOrOwner, IsBoardOwner
from boards_app.models import Board


class BoardListView(APIView):
    """Handles listing and creating boards."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns all boards where the user is owner or member."""
        boards = Board.objects.filter(
            members=request.user) | Board.objects.filter(owner=request.user)
        return Response(BoardSerializer(boards.distinct(), many=True).data)

    def post(self, request):
        """Creates a new board with the authenticated user as owner."""
        serializer = BoardCreateSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.save(owner=request.user)
            return Response(BoardSerializer(board).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class BoardDetailView(APIView):
    """Handles retrieving, updating and deleting a single board."""

    permission_classes = [IsAuthenticated]

    def get_board(self, board_id):
        """Returns a board by ID or None if not found."""
        try:
            return Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return None

    def get(self, request, board_id):
        """Returns details of a single board."""
        board = self.get_board(board_id)
        if not board:
            return Response({'error': 'Board not found'}, status=HTTP_404_NOT_FOUND)
        if not IsBoardMemberOrOwner().has_object_permission(request, self, board):
            return Response({'error': 'You do not have permission'}, status=HTTP_403_FORBIDDEN)
        return Response(BoardSerializer(board).data)

    def patch(self, request, board_id):
        """Partially updates a board."""
        board = self.get_board(board_id)
        if not board:
            return Response({'error': 'Board not found'}, status=HTTP_404_NOT_FOUND)
        if not IsBoardMemberOrOwner().has_object_permission(request, self, board):
            return Response({'error': 'You do not have permission'}, status=HTTP_403_FORBIDDEN)
        serializer = BoardCreateSerializer(
            board, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(BoardSerializer(serializer.save()).data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, board_id):
        """Deletes a board. Only the owner can delete."""
        board = self.get_board(board_id)
        if not board:
            return Response({'error': 'Board not found'}, status=HTTP_404_NOT_FOUND)
        if not IsBoardOwner().has_object_permission(request, self, board):
            return Response({'error': 'You do not have permission'}, status=HTTP_403_FORBIDDEN)
        board.delete()
        return Response(status=HTTP_204_NO_CONTENT)
