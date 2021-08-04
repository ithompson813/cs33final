from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import NewGroupForm
from .models import User, Group, Message


def index(request):

    groups = Group.objects.filter(users__username=request.user.username)

    return render(request, "chat/index.html", {
        "groups": groups
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chat/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "chat/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chat/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "chat/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chat/register.html")



def new_group(request):

    # if received as a GET request, load new_group page with NewGroupForm
    # NewGroupForm is defined in forms.py
    if request.method == "GET":

        return render(request, "chat/new_group.html", {

            "form": NewGroupForm()

        })

    
    elif request.method == "POST":

        # store data received in NewGroupForm
        form = NewGroupForm(request.POST)
        
        # check data validity
        if form.is_valid():

            # assign data to variables
            form_name = form.cleaned_data["name"]
            form_users = form.cleaned_data["invited_users"]

            group = Group(name=form_name)
            group.save()

            group.users.add(*form_users)
            group.users.add(request.user)
            group.save()

            return HttpResponseRedirect(reverse("index"))

        # if data is invalid, return user to form
        else: 
            return render(request, "chat/new_group.html", {
                "form": form
            })

    return HttpResponse("error")


def get_groups(request):

    # get groups that current user has access to
    groups = Group.objects.filter(users__username=request.user.username)

    # return JSON data
    return JsonResponse([group.serialize() for group in groups], safe=False)


def get_messages(request, id):

    group_object = Group.objects.get(id=int(id))
    messages = Message.objects.filter(group = group_object)

    return JsonResponse([message.serialize() for message in messages], safe=False)