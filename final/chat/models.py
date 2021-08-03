from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Message(models.Model):
    creator = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.creator} said '{self.content}' to {self.group}"

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator,
            "group": self.group          
        }
    

class Group(models.Model):
    creator = models.ForeignKey('User', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="invited_users", blank=True)

    def __str__(self):
        return f"{self.creator}'s Group ({self.id})"

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator,
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