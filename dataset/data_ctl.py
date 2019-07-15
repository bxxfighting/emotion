import os
import pandas as pd

from base import errors

from .models import CommentModel
from .models import StopwordModel


def init_comment(path):
    CommentModel.objects.filter().delete()
    df = pd.read_csv(path)
    obj_list = []
    index = 1
    label_dict = {
        0: CommentModel.LABEL_POSITIVE,
        1: CommentModel.LABEL_NEGATIVE,
    }
    for label, comment in zip(df.label.values, df.comment.values):
        data = {
            'label': label_dict[int(label)],
            'comment': comment,
        }
        obj_list.append(CommentModel(**data))
        if index % 2000 == 0:
            CommentModel.objects.bulk_create(obj_list)
            obj_list = []
    if obj_list:
        CommentModel.objects.bulk_create(obj_list)


def init_stopword(path):
    StopwordModel.objects.filter().delete()
    with open(path) as f:
        stopwords = f.read()
    stopwords = stopwords.split('\n')
    obj_list = []
    index = 1
    for word in stopwords:
        data = {
            'word': word,
        }
        obj_list.append(StopwordModel(**data))
        if index % 2000 == 0:
            StopwordModel.objects.bulk_create(obj_list)
            obj_list = []
    if obj_list:
        StopwordModel.objects.bulk_create(obj_list)


def list_comment(status=None, label=None, keyword=None, page_num=None, page_size=None):
    '''
    获取评价列表
    '''
    base_query = CommentModel.objects.filter(is_deleted=False)
    if status:
        base_query = base_query.filter(status=status)
    if label:
        base_query = base_query.filter(label=label)
    if keyword:
        base_query = base_query.filter(comment__icontains=keyword)
    total = base_query.count()
    if page_num and page_size:
        end = page_num * page_size
        start = end - page_size
        base_query = base_query[start:end]
    objs = base_query.all()
    data_list = [obj.to_dict() for obj in objs]
    data = {
        'total': total,
        'data_list': data_list,
    }
    return data


def update_comment(obj_id, label):
    '''
    编辑评价
    '''
    obj = CommentModel.objects.filter(id=obj_id, is_deleted=False).first()
    if not obj:
        raise errors.CommonError('评论不存在')
    obj.label = label
    obj.status = CommentModel.ST_CHECKED
    obj.save()


def check_comment(obj_id):
    obj = CommentModel.objects.filter(id=obj_id, is_deleted=False).first()
    if not obj:
        raise errors.CommonError('评论不存在')
    obj.status = CommentModel.ST_CHECKED
    obj.save()


def list_comment_for_train():
    comments = CommentModel.objects.values_list('comment', 'label').filter(is_deleted=False).all()
    return list(comments)


def list_stopword(status=None, keyword=None, page_num=None, page_size=None):
    '''
    获取停止词列表
    '''
    base_query = StopwordModel.objects.filter(is_deleted=False)
    if status:
        base_query = base_query.filter(status=status)
    if keyword:
        base_query = base_query.filter(word__icontains=keyword)
    total = base_query.count()
    if page_num and page_size:
        end = page_num * page_size
        start = end - page_size
        base_query = base_query[start:end]
    objs = base_query.all()
    data_list = [obj.to_dict() for obj in objs]
    data = {
        'total': total,
        'data_list': data_list,
    }
    return data


def create_stopword(word):
    '''
    创建停止词
    '''
    obj = StopwordModel.objects.filter(word=word, is_deleted=False).first()
    if obj:
        raise errors.CommonError('此停止词已经存在')
    data = {
        'word': word,
    }
    obj = StopwordModel.objects.create(**data)


def update_stopword(obj_id, status):
    '''
    编辑停止词
    '''
    obj = StopwordModel.objects.filter(id=obj_id, is_deleted=False).first()
    if not obj:
        raise errors.CommonError('停止词不存在')
    obj.status = status
    obj.save()


def delete_stopword(obj_id):
    '''
    删除停止词
    '''
    obj = StopwordModel.objects.filter(id=obj_id, is_deleted=False).first()
    if not obj:
        raise errors.CommonError('停止词不存在')
    obj.is_deleted = True
    obj.save()


def list_stopword_for_train():
    words = StopwordModel.objects.values_list('word', flat=True)\
            .filter(status=StopwordModel.ST_ENABLED, is_deleted=False).all()
    return words
