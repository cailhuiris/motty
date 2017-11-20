from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^motty/$', views.index, name = "index_view"),
    url(r'^motty/resource/(?P<resource_id>[0-9]{1,})/action/create', views.create_action, name='create_action'),
    url(r'^motty/action/([0-9]{1,})/view', views.action_view, name='action_view'),

    # resource api
    url(r'^motty/api/resources', views.resources, name="api_resources"),
    url(r'^motty/api/resource$', views.save_resource, name="api_save_resource"),
    url(r'^motty/api/resource/([0-9]{1,})/delete', views.delete_resource, name="api_delete_resource"),

    # action api
    # url(r'^motty/api/action$', views.save_action, name = "api_save_action"),
    url(r'^motty/api/action/([0-9]{1,})$', views.get_action, name = "api_get_action"),
    url(r'^motty/api/action/([0-9]{1,})/delete$', views.delete_action, name = "api_delete_action"),

    # producing resource api
    url(r'^motty/base/(.+)', views.return_fake_request, name = "return_fake_request"),

    url(r'', views.main, name = "main"),
]