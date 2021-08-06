from django import forms

from .models import User, Message, Group

# the NewGroupForm is displayed to the user on new_group.html
class NewGroupForm(forms.Form):
    name = forms.CharField(label="Name: ", max_length="80")
    invited_users = forms.ModelMultipleChoiceField(label="Invite Users: ", queryset=User.objects.all())