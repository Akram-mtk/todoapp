from django.urls import path
from .views import main, sign, login, remove

urlpatterns = [
    path("", main, name="main"),
    path('sign-up', sign, name="sign"),
    path('login', login, name="login"),
    path('remove/<int:id>', remove, name="rmv")
]