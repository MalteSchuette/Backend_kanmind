from django.db import models

# Create your models here.

	# Tasks
	# 	id
	# 	title
	# 	description
	# 	Status
	# 	priority
	# 	assignee		-> ForeignKey User
	# 	Reviewer		-> ForeignKey User
	# 	due_date	
	# 	board			-> ForeignKey Board	

	# Comments
	# 	id
	# 	created_at
	# 	author			-> ForeignKey User
	# 	Task			-> ForeignKey Tasks


class Task(models.Model):
    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='to-do')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='medium')
    assignee = models.ForeignKey('users_app.User', on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    reviewer = models.ForeignKey('users_app.User', on_delete=models.SET_NULL, null=True, related_name='reviewed_tasks')
    due_date = models.DateTimeField(null=True, blank=True)
    board = models.ForeignKey('boards_app.Board', on_delete=models.CASCADE, related_name='tasks')

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('users_app.User', on_delete=models.SET_NULL, null=True, related_name='comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()