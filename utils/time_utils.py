from datetime import datetime
from datetime import timedelta

def str2datetime_by_format(dt_str, dt_format='%Y-%m-%d %H:%M:%S'):
    '''
    时间字符串转datetime
    '''
    return datetime.strptime(dt_str, dt_format)


def datetime2str_by_format(dt, dt_format='%Y-%m-%d %H:%M:%S'):
    '''
    本地datetime转本地字符串
    '''
    if not dt:
        return ''
    return dt.strftime(dt_format)


def datetime2date_range(dt):
    '''
    datetime转换成一天的开始和结束时间[start, end)
    '''
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end


def yesterday():
    dt = datetime.now()
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt - timedelta(days=1)


def utcts2dt(ts):
    '''
    UTC时间戳转Datetime
    '''
    dt = datetime.utcfromtimestamp(ts)
    dt = dt + timedelta(hours=8)
    return dt
