class BaseError(Exception):
    errno = 10001
    errmsg = '服务暂时不可用'

    def __init__(self, errmsg=None):
        if errmsg:
            self.errmsg = errmsg


class MethodError(BaseError):
    errno = 10002
    errmsg = '不支持的请求方式'


class InvalidArgsError(BaseError):
    errno = 10003
    errmsg = '无效的参数'


class NoTokenError(BaseError):
    '''
    缺少token
    '''
    errno = 10004
    errmsg = '请求header中缺少token'


class LoginExpireError(BaseError):
    '''
    登录过期
    '''
    errno = 10005
    errmsg = '登录状态过期，请重新登录'


class CommonError(BaseError):
    errno = 10006
    errmsg = '出错了'
