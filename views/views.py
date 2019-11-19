from django.http import HttpResponse
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import login_required


@login_required()
def home(request):
    u = request.user
    if u.is_authenticated is True:
        html = f"<html><body> Home Page\n{u.username}</body></html"
        return HttpResponse(html)


def registration(request):
    html = """<html><body><h1> Register</h1>
    <form action = "/api/registration/" method="post">
    <input type="text" id="username" name="username" placeholder="Enter your user name">
    <input type="email" id="email" name="email" placeholder="email(optional)">
    <input type="password" id="password1" name="password1" placeholder="enter a password" pattern = "(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$">

    <input type="password" id="password2" name="password2" placeholder="confirm password" pattern ="(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$">
    <input type="submit" value="Register">
    </form>
    </body></html"""
    return HttpResponse(html)


def login(request):
    html = """<html><body><h1> Login</h1>
    <h3> <a href="/registration/">Register instead</a></h3>
    <form action = "/api/login/" method="post">
    <input type="text" id="username" name="username" placeholder="Enter your user name">
    <input type="password" id="password" name="password" placeholder="enter a password" pattern = "(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$">

    <input type="submit" value="Login">
    </form>
    </body></html"""
    return HttpResponse(html)


# class RegistrationForm(forms.Form):
#    username = forms.CharField(label="your user name", max_length=100)
#    email =
#    password1 =
#    password2 =
