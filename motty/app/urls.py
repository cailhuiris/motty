from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^motty/$', views.index, name = "index_view"),
    url(r'^motty/resource/(?P<resource_id>[0-9]{1,})/action/create', views.save_action, name='create_action'),
    url(r'^motty/resource/(?P<resource_id>[0-9]{1,})/action/(?P<action_id>[0-9]{1,})/save', views.save_action, name='edit_action'),
    url(r'^motty/action/([0-9]{1,})/view', views.action_view, name='action_view'),
    url(r'^motty/api/action/([0-9]{1,})/delete$', views.delete_action, name = "delete_action"),

    # resource api for interactive app.
    url(r'^motty/api/resources', views.resources, name="api_resources"),
    url(r'^motty/api/resource$', views.save_resource, name="api_save_resource"),
    url(r'^motty/api/resource/([0-9]{1,})/delete', views.delete_resource, name="api_delete_resource"),

    # producing resource api
    url(r'(.+)', views.return_fake_request, name = "return_fake_request"),
    url(r'', views.main, name = "main"),
]