from django.urls import path
from .views import BoardListView, BoardDetailView

urlpatterns = [
    path('', BoardListView.as_view()),
    path('<int:board_id>/', BoardDetailView.as_view()),
]
