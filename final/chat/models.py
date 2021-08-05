from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Message(models.Model):
    creator = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.creator} said '{self.content}' to {self.group}"

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "content": self.content,
            "group": self.group.name,  
            "timestamp": self.timestamp,   
        }
    

class Group(models.Model):
    name = models.CharField(max_length=80, blank=True)
    users = models.ManyToManyField(User, related_name="invited_users", blank=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "users": [user.username for user in self.users.all()],
        }
