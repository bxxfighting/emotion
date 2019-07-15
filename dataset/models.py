import os

from django.db import models
from django.conf import settings

from base.models import BaseModel


class CommentModel(BaseModel):
    '''
    评价
    '''
    LABEL_POSITIVE = 10
    LABEL_NEGATIVE = 20
    LABEL_CHOICES = (
        (LABEL_POSITIVE, '正向评价'),
        (LABEL_NEGATIVE, '负向评价'),
    )
    comment = models.TextField('评价文本')
    label = models.SmallIntegerField('情绪标注', choices=LABEL_CHOICES)

    class Meta:
        db_table = 'comment'


class StopwordModel(BaseModel):
    '''
    停止词
    '''
    ST_ENABLED = 10
    ST_DISABLED = 20
    ST_CHOICES = (
        (ST_ENABLED, '启用'),
        (ST_DISABLED, '禁用'),
    )

    status = models.SmallIntegerField('状态', choices=ST_CHOICES, default=ST_ENABLED)
    word = models.CharField('词语', max_length=128)

    class Meta:
        db_table = 'stopword'
