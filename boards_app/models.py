from django.db import models

# Create your models here.


# boards_app
# 	Board
# 		id
# 		title
# 		members  		-> ManyToMany User		
# 		owner_id		-> Foreignkey User

class Board(models.Model):
    title = models.CharField(max_length=255)
    members = models.ManyToManyField('users_app.User', related_name='boards')
    owner = models.ForeignKey('users_app.User', on_delete=models.SET_NULL, null=True, related_name='owned_boards')
    