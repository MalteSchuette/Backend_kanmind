# tasks_app/api/urls.py
from django.urls import path
from .views import (
    TasksView,
    AssignedToMeView,
    ReviewedByMeView,
    TaskDetailView,
    TaskCommentDetailView,
    TaskCommentListView
)

urlpatterns = [
    path('', TasksView.as_view()),
    path('assigned-to-me/', AssignedToMeView.as_view()),
    path('reviewing/', ReviewedByMeView.as_view()),
    path('<int:task_id>/', TaskDetailView.as_view()),
    path('<int:task_id>/comments/', TaskCommentListView.as_view()),
    path('<int:task_id>/comments/<int:comment_id>/',
         TaskCommentDetailView.as_view()),
]
