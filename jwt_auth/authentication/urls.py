from django.urls import path
from .views import RegisterView, AuthView, LogoutView, DeleteView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", AuthView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("delete/", DeleteView.as_view())
]
