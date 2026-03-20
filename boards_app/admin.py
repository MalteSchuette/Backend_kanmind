# boards_app/admin.py
from django.contrib import admin
from .models import Board

admin.site.register(Board)
