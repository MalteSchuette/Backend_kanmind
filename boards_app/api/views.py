from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from boards_app.api.serializers import BoardSerializer, BoardCreateSerializer
from boards_app.models import Board
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

class BoardListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards = Board.objects.filter(members=request.user) | Board.objects.filter(owner=request.user)
        boards = boards.distinct()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BoardCreateSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.save(owner=request.user)
            return Response(BoardSerializer(board).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class BoardDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found'}, status=HTTP_404_NOT_FOUND)
        
        if request.user not in board.members.all() and request.user != board.owner:
            return Response({'error': 'You do not have permission to view this board'}, status=HTTP_403_FORBIDDEN)
        
        serializer = BoardSerializer(board)
        return Response(serializer.data)
    
    def patch(self, request, board_id):
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found'}, status=HTTP_404_NOT_FOUND)
        
        if request.user not in board.members.all() and request.user != board.owner:
            return Response({'error': 'You do not have permission'}, status=HTTP_403_FORBIDDEN)
        
        serializer = BoardCreateSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            board = serializer.save()
            return Response(BoardSerializer(board).data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, board_id):
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found'}, status=HTTP_404_NOT_FOUND)
        
        if request.user != board.owner:
            return Response({'error': 'You do not have permission to delete this board'}, status=HTTP_403_FORBIDDEN)
        
        board.delete()
        return Response(status=HTTP_204_NO_CONTENT)
            