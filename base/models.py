from django.db import models
from django.forms.models import model_to_dict

from utils import time_utils


class BaseModel(models.Model):
    '''
    '''
    dt_create = models.DateTimeField(auto_now_add=True)
    dt_update = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def to_dict(self):
        data = model_to_dict(self)
        dt_update = time_utils.datetime2str_by_format(self.dt_update, '%Y-%m-%d %H:%M:%S')
        dt_create = time_utils.datetime2str_by_format(self.dt_create, '%Y-%m-%d %H:%M:%S')
        data['dt_update'] = dt_update
        data['dt_create'] = dt_create
        return data
