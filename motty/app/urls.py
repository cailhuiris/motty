from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^motty/$', views.IndexView.as_view(), name = "index_view"),
    url(r'^motty/resource/(?P<resource_id>[0-9]{1,})/action/create', views.SaveAction.as_view(), name='create_action'),
    url(r'^motty/resource/(?P<resource_id>[0-9]{1,})/action/(?P<action_id>[0-9]{1,})/save', views.SaveAction.as_view(), name='edit_action'),
    url(r'^motty/action/([0-9]{1,})/view', views.ActionView.as_view(), name='action_view'),
    url(r'^motty/api/action/([0-9]{1,})/delete$', views.DeleteAction.as_view(), name = "delete_action"),

    # resource api for interactive app.
    url(r'^motty/api/resources', views.FetchResources.as_view(), name="api_resources"),
    url(r'^motty/api/resource$', views.SaveResource.as_view(), name="api_save_resource"),
    url(r'^motty/api/resource/([0-9]{1,})/delete', views.DeleteResource.as_view(), name="api_delete_resource"),

    # producing resource api
    url(r'(.+)', views.return_fake_request, name = "return_fake_request"),
    url(r'', views.MainView.as_view(), name = "main"),
]