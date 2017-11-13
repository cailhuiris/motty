from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^app/$', views.index, name = "index"),
    url(r'^app/api/actions', views.actions, name = "actions"),
    url(r'^app/api/action$', views.create_new_action, name = "create_new_action"),
    url(r'^app/api/action/([0-9]{1,})$', views.get_action, name = "get_action"),
    url(r'^app/api/action/([0-9]{1,})/edit$', views.edit_action, name = "edit_action"),
    url(r'^app/api/action/([0-9]{1,})/delete$', views.delete_action, name = "delete_action"),
    url(r'^motty/base/(.+)', views.return_fake_request, name = "return_fake_request"),
    url(r'', views.main, name = "main"),
]