from django.urls import path
from .views import greeting_view,greeting_user

urlpatterns = [
    path("greeting",greeting_view, name="greeting"),
    path("greeting-user", greeting_user, name='greeting_user'),
]
