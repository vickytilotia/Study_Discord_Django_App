from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField( max_length=250)

    def __str__(self):
        return self.name
    




# Create your models here.
class Room(models.Model):

    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    # participants = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 
    # difference between the now and now_add is now_add only take time once 
    #  and then never update whereas auto_now update everytime with the update in function.



    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
    
    