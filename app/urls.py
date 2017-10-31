from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^app/', views.index, name = "index")
]