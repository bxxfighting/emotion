import ujson as json

from django.db import transaction

from base.api import Api
from dataset import data_ctl


class ListCommentView(Api):

    def POST(self, request):
        data = json.loads(request.body)
        label = data.get('label')
        status = data.get('status')
        keyword = data.get('keyword')
        page_num = data.get('page_num')
        page_size = data.get('page_size')
        data = {
            'label': label,
            'status': status,
            'keyword': keyword,
            'page_num': page_num,
            'page_size': page_size,
        }
        data = data_ctl.list_comment(**data)
        return data


class UpdateCommentView(Api):

    def POST(self, request):
        data = json.loads(request.body)
        obj_id = data.get('id')
        label = data.get('label')
        data = {
            'obj_id': obj_id,
            'label': label,
        }
        data = data_ctl.update_comment(**data)
        return data


class CheckCommentView(Api):

    def POST(self, request):
        data = json.loads(request.body)
        obj_id = data.get('id')
        data = {
            'obj_id': obj_id,
        }
        data = data_ctl.check_comment(**data)
        return data


class ListStopwordView(Api):

    def POST(self, request):
        data = json.loads(request.body)
        status = data.get('status')
        keyword = data.get('keyword')
        page_num = data.get('page_num')
        page_size = data.get('page_size')
        data = {
            'status': status,
            'keyword': keyword,
            'page_num': page_num,
            'page_size': page_size,
        }
        data = data_ctl.list_stopword(**data)
        return data


class CreateStopwordView(Api):

    def POST(self, request):
        data = json.loads(request.body)
        word = data.get('word')
        data = {
            'word': word,
        }
        data_ctl.create_stopword(**data)


class UpdateStopwordView(Api):

    def POST(self, request):
        data = json.loads(request.body)
        obj_id = data.get('id')
        status = data.get('status')
        data = {
            'obj_id': obj_id,
            'status': status,
        }
        data = data_ctl.update_stopword(**data)
        return data


class DeleteStopwordView(Api):

    def POST(self, request):
        data = json.loads(request.body)
        obj_id = data.get('id')
        data = {
            'obj_id': obj_id,
        }
        data_ctl.delete_stopword(**data)
