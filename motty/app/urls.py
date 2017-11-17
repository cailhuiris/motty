from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^app/$', views.index, name = "index_view"),
    url(r'^app/action/create', views.create_action_view, name='create_action_view'),

    url(r'^motty/api/actions', views.actions, name = "actions"),
    url(r'^motty/api/action$', views.create_new_action, name = "create_new_action"),
    url(r'^motty/api/action/([0-9]{1,})$', views.get_action, name = "get_action"),
    url(r'^motty/api/action/([0-9]{1,})/edit$', views.edit_action, name = "edit_action"),
    url(r'^motty/api/action/([0-9]{1,})/delete$', views.delete_action, name = "delete_action"),
    url(r'^motty/api/action/delete/all$', views.delete_all, name = "delete_all"),

    url(r'^motty/base/(.+)', views.return_fake_request, name = "return_fake_request"),

    url(r'', views.main, name = "main"),
]