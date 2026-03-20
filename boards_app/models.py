from django.db import models


class Board(models.Model):
    """Represents a Kanban board with an owner and multiple members."""

    title = models.CharField(max_length=255)
    members = models.ManyToManyField('users_app.User', related_name='boards')
    owner = models.ForeignKey(
        'users_app.User', on_delete=models.SET_NULL, null=True, related_name='owned_boards')

    def __str__(self):
        return self.title
