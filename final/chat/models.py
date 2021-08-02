from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class chat(models.Model):
    creator = models.ForeignKey('User', on_delete=models.CASCADE)



# message
#   author, content, group(foreign)

#   will show messages based on an api call to the correct group
#   this will be triggered by the html in the dropdown
#       click will call api whenever a group is shown on screen
#       will need to figure out how to update chat dynamically

# group
#   users, creator
#   