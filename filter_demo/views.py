from django.shortcuts import render

# Create your views here.

def greeting_user(request):
    books = {"The night rider": "Ben Author",
             "The Justice": "Don Abeman"}

    user_name = request.user.username
    return render(request, "templatetags/simple_tag_template.html",
                  {"username":user_name,'books':books})