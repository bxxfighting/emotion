import ujson as json
import logging
import traceback

from django.http import HttpResponse
from django.core.signing import TimestampSigner
from django.core.signing import SignatureExpired

from base import errors


class Api:
    NEED_LOGIN = True
    NEED_PERMISSION = True
    need_params = {}
    user_id = None

    def __inif__(self, **opts):
        for k, v in opts.iteritems():
            setattr(self, k, v)

    def check_params(self, request):
        '''
        校验参数
        need_params = {
            'username': ('用户名', 'required str 32'),
            'password': ('密码', 'required str 32'),
        }
        '''
        data = json.loads(request.body)
        for key in self.need_params.keys():
            value = data.get(key)
            name, condition = self.need_params.get(key)
            method, *condition = condition.split(' ')
            method = 'check_{}'.format(method)
            getattr(self, method)(name, value, condition)

    def check_required(self, name, value, condition):
        '''
        必填项校验
        '''
        if value is None or value == '':
            raise errors.InvalidArgsError('{}为必填项'.format(name))
        if len(condition) == 0:
            return
        method, *condition = condition
        method = 'check_{}'.format(method)
        getattr(self, method)(name, value, condition)

    def check_optional(self, name, value, condition):
        '''
        可选项校验
        '''
        if value is None or value == '':
            return
        if len(condition) == 0:
            return
        method, *condition = condition
        method = 'check_{}'.format(method)
        getattr(self, method)(name, value, condition)

    def check_str(self, name, value, condition):
        '''
        '''
        if not isinstance(value, str):
            raise errors.InvalidArgsError('{}需要字符串参数'.format(name))
        length = len(value)
        if len(condition) == 0:
            return
        elif len(condition) == 1:
            max_length = int(condition[0])
            if length > max_length:
                raise errors.InvalidArgsError('{}长度不能大于{}'.format(name, max_length))
        else:
            min_length, max_length, *_ = condition
            min_length = int(min_length)
            max_length = int(max_length)
            if not (min_length <= length <= max_length):
                raise errors.InvalidArgsError('{}长度应在{}~{}个字符之间'.format(name, min_length, max_length))

    def check_int(self, name, value, condition):
        '''
        '''
        if not isinstance(value, int):
            raise errors.InvalidArgsError('{}需要整数参数'.format(name))
        if len(condition) == 0:
            return
        elif len(condition) == 1:
            max_value = condition[0]
            if value > max_value:
                raise errors.InvalidArgsError('{}最大值不超过{}'.format(name, max_value))
        else:
            min_value, max_value, *_ = condition
            if not (min_value <= value <= max_value):
                raise errors.InvalidArgsError('{}值应在{}~{}之间'.format(name, min_value, max_value))

    def check_list(self, name, value, condition):
        if not isinstance(value, list):
            raise errors.InvalidArgsError('{}需要列表'.format(name))

    def _get_token(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise errors.NoTokenError
        return token

    def _token2user_id(self, token):
        signer = TimestampSigner()
        try:
            # 如果加上max_age就可以控制登录有效时长
            user_id = signer.unsign(token, max_age=12*60*60)
            # user_id = signer.unsign(token)
        except SignatureExpired as e:
            raise errors.LoginExpireError
        return int(user_id)

    def _identification(self, request):
        token = self._get_token(request)
        self.user_id = self._token2user_id(token)

    def _permission(self, user_id, url):
        '''
        权限验证
        '''
        from account.controllers import is_permission
        if not is_permission(user_id, url):
            raise errors.CommonError('权限不足，无法进行此操作')

    def _pre_handle(self, request):
        '''
        请求处理前处理
        '''
        if self.NEED_LOGIN:
            self._identification(request)
        if self.NEED_PERMISSION:
            self._permission(self.user_id, request.path)
        self.check_params(request)

    def _after_handle(self):
        '''
        请求处理后处理
        '''
        pass

    def find_method(self, request):
        method = getattr(self, request.method, None)
        if not method:
            raise errors.MethodError
        return method

    def __call__(self, request, *args, **kwargs):
        errno = 0
        errmsg = ''
        data = None
        try:
            self._pre_handle(request)
            info_logger = logging.getLogger('info')
            body = json.loads(request.body)
            mesg = '{} {} {}'.format(request.get_full_path(), self.user_id, json.dumps(body))
            info_logger.info(mesg)
            method = self.find_method(request)
            data = method(request, *args, **kwargs)
            self._after_handle()
            if isinstance(data, HttpResponse):
                return data
        except errors.BaseError as e:
            errno = e.errno
            errmsg = e.errmsg
        except Exception as e:
            logger = logging.getLogger('error')
            logger.exception(e)
            errno = errors.BaseError.errno
            errmsg = errors.BaseError.errmsg
        data = {
            'errno': errno,
            'errmsg': errmsg,
            'data': data,
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
