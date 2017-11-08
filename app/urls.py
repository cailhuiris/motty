from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^app/', views.index, name = "index"),
    url(r'', views.main, name = "main"),
]