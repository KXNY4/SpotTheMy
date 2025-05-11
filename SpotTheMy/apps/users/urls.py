from django.urls import path
from .views import MeView, UserListView, RegisterView


urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("register/", RegisterView.as_view(), name='register'),
    path("me/", MeView.as_view(), name='me'),
]
