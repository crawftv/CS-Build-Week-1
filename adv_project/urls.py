from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from views import views

urlpatterns = [
    path("", views.home),
    path("login/", views.login),
    path("registration/", views.registration),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/adv/", include("adventure.urls")),
]
