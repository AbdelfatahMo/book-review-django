from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse

def greeting_view(request):
    """Greet the user."""
    return HttpResponse("Hey there, welcome to Bookr!")
        
@login_required
def greeting_user(request):
    username = request.user.username
    return HttpResponse("Welcome to Bookr! {username}".format(username=username))