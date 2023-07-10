from django.urls import path
from .views import greeting_user


urlpatterns = [
    path("greet/",greeting_user, name="greet"),
]
