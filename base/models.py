from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):# we put topic above room model bcause room is a child of topic
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # null is for the database while blank is for the same
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    update = models.DateTimeField(auto_now=True)# Takes snashot everytime we save item 
    created =models.DateTimeField(auto_now_add=True) #Takes timestamp when we first save the item

    '''class Meta:
        ordering = ['-updated', '-created']'''

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)# Takes snashot everytime we save item 
    created =models.DateTimeField(auto_now_add=True) #Takes timestamp when we first save the item
    
    '''class Meta:
        ordering = ['-updated', '-created']'''

    def __str__(self):
        return self.body[0:50]
