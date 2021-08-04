
from django.urls import path

from . import views

urlpatterns = [

    # default routes
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_group", views.new_group, name="new_group"),

    # api calls
    path("groups", views.get_groups, name="get_groups"),
    path("messages/<str:id>", views.get_messages, name="get_messages")
]
