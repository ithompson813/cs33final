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
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),   
        }
    

class Group(models.Model):
    #creator = models.ForeignKey('User', on_delete=models.CASCADE)
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


# message
#   author, content, group(foreign)

#   will show messages based on an api call to the correct group
#   this will be triggered by the html in the dropdown
#       click will call api whenever a group is shown on screen
#       will need to figure out how to update chat dynamically

# group
#   id, users, creator
#   



# new group in html leads to a new group creation page
#   it can then redirect you to that page on the single-page view

# display each group that a user is in on a dropdown on the left side (or at the top, if left is too hard)
#   clicking each group displays the messages in that group and shows a chat box to contribute
#   need to figure out how to dynamically update a group's messages