from datetime import datetime
from django.db import models

class Resource(models.Model):
    '''Resource manages actions.'''
    name = models.CharField(unique=True, max_length=30)
    url = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return "name: {0}, url: {1}".format(self.name, self.url)

class Action(models.Model):
    '''Action produces responses to client, and all actions are managed by resource.'''
    resource = models.ForeignKey(Resource, null=False, related_name='actions', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=50)
    method = models.CharField(max_length=50)
    contentType = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(default = datetime.now())

    def __str__(self):
        return "name: {0}, url: {1}, method: {2}, contentType: {3}, body: {4}, created_at: {5}"\
            .format(self.name, self.url, self.method, self.contentType, self.body, self.created_at)