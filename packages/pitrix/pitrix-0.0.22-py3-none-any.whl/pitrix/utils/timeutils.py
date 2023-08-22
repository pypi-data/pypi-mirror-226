#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import time
import math
import calendar
import datetime
import iso8601
try:
    import zoneinfo
except ImportError:
    # zoneinfo is available in Python >= 3.9
    import pytz
    zoneinfo = None

# from oslo_utils import reflection

# ISO 8601 extended time format with microseconds
ISO8601 = '%Y-%m-%dT%H:%M:%SZ'
ISO8601_MS = '%Y-%m-%dT%H:%M:%S.%fZ'
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
_ISO8601_TIME_FORMAT_SUBSECOND = '%Y-%m-%dT%H:%M:%S.%f'
_ISO8601_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
PERFECT_TIME_FORMAT = _ISO8601_TIME_FORMAT_SUBSECOND

_MAX_DATETIME_SEC = 59

now = time.monotonic


def parse_isotime(timestr):
    """
    按照ISO8601格式解析时间
    timestr:
    "2023-07-18"：只表示日期，不包含时间。
    "'2023-07-18T14:30:00'"：表示具体的日期和时间，没有时区信息。
    "2023-07-18T14:30:00Z"：表示具体的日期和时间，并带有UTC时区的标志"Z"。
    "2023-07-18T14:30:00+08:00"：表示具体的日期和时间，并带有相对于UTC的偏移量为+8小时的时区信息。
    """
    try:
        return iso8601.parse_date(timestr)
    except iso8601.ParseError as e:
        raise ValueError(str(e))
    except TypeError as e:
        raise ValueError(str(e))


def parse_strptime(timestr, fmt=TIME_FORMAT):
    """
    将格式化的时间转换回日期时间
    """
    return datetime.datetime.strptime(timestr, fmt)


def normalize_time(timestamp):
    """Normalize time in arbitrary timezone to UTC naive object."""
    offset = timestamp.utcoffset()
    if offset is None:
        return timestamp
    return timestamp.replace(tzinfo=None) - offset


def utcnow_ts(microsecond=False):
    """Timestamp version of our utcnow function.

    See :py:class:`oslo_utils.fixture.TimeFixture`.

    .. versionchanged:: 1.3
       Added optional *microsecond* parameter.
    """
    if utcnow.override_time is None:
        # NOTE(kgriffs): This is several times faster
        # than going through calendar.timegm(...)
        timestamp = time.time()
        if not microsecond:
            timestamp = int(timestamp)
        return timestamp

    now = utcnow()
    timestamp = calendar.timegm(now.timetuple())

    if microsecond:
        timestamp += float(now.microsecond) / 1000000

    return timestamp


def utcnow(with_timezone=False):
    """
    返回一个utc时间
    eg:with_timezone true -> 2023-08-10 15:24:55.832413
    eg:with_timezone false -> 2023-08-10 15:25:36.800075+00:00
    """
    if utcnow.override_time:
        try:
            return utcnow.override_time.pop(0)
        except AttributeError:
            return utcnow.override_time
    if with_timezone:
        return datetime.datetime.now(tz=iso8601.iso8601.UTC)
    return datetime.datetime.utcnow()


def get_delay_time(interval='hours', delay=0, utc=True, format=ISO8601):
    """
    根据当前世界UTC时间或者本地时间来指定获取之后的某个单位的时间
    :param interval: 单位为：天days、秒seconds、微秒microseconds、毫秒milliseconds、分minutes、小时hours、周weeks
    :param delta: int类型的正数或者负数，正数代表之后的某个时间，负数代表之前的某个时间
    :param utc: 选择采用本地时间还是采用世界UTC时间,默认采用世界UTC时间
    :param format: 默认的格式采用ISO8601
    :return:get_delay_time(interval='minutes',delay=20,utc=True) -> ('2022-08-24T10:58:46Z', '2022-08-24T11:18:46Z')
    """
    if utc:
        now_time = datetime.datetime.utcnow()
    else:
        now_time = datetime.datetime.now()
    if interval == 'hours':
        delta_time = (now_time + datetime.timedelta(hours=delay)).strftime(format)
    elif interval == 'days':
        delta_time = (now_time + datetime.timedelta(days=delay)).strftime(format)
    elif interval == 'weeks':
        delta_time = (now_time + datetime.timedelta(weeks=delay)).strftime(format)
    elif interval == 'seconds':
        delta_time = (now_time + datetime.timedelta(seconds=delay)).strftime(format)
    elif interval == 'microseconds':
        delta_time = (now_time + datetime.timedelta(microseconds=delay)).strftime(format)
    elif interval == 'milliseconds':
        delta_time = (now_time + datetime.timedelta(milliseconds=delay)).strftime(format)
    elif interval == 'minutes':
        delta_time = (now_time + datetime.timedelta(minutes=delay)).strftime(format)
    else:
        raise ValueError('interval error')
    return (now_time.strftime(format),delta_time)

def get_delay_time_before(interval='hours', delay=0, utc=True, format=ISO8601):
    """
    根据当前世界UTC时间或者本地时间来指定获取之前的某个单位的时间
    :param interval: 单位为：天days、秒seconds、微秒microseconds、毫秒milliseconds、分minutes、小时hours、周weeks
    :param delta: int类型的正数或者负数，正数代表之后的某个时间，负数代表之前的某个时间
    :param utc: 选择采用本地时间还是采用世界UTC时间,默认采用世界UTC时间
    :param format: 默认的格式采用ISO8601
    :return:get_delay_time(interval='minutes',delay=20,utc=True) -> ('2022-08-24T10:58:46Z', '2022-08-24T11:18:46Z')
    """
    if utc:
        now_time = datetime.datetime.utcnow()
    else:
        now_time = datetime.datetime.now()
    if interval == 'hours':
        delta_time = (now_time - datetime.timedelta(hours=delay)).strftime(format)
    elif interval == 'days':
        delta_time = (now_time - datetime.timedelta(days=delay)).strftime(format)
    elif interval == 'weeks':
        delta_time = (now_time - datetime.timedelta(weeks=delay)).strftime(format)
    elif interval == 'seconds':
        delta_time = (now_time - datetime.timedelta(seconds=delay)).strftime(format)
    elif interval == 'microseconds':
        delta_time = (now_time - datetime.timedelta(microseconds=delay)).strftime(format)
    elif interval == 'milliseconds':
        delta_time = (now_time - datetime.timedelta(milliseconds=delay)).strftime(format)
    elif interval == 'minutes':
        delta_time = (now_time - datetime.timedelta(minutes=delay)).strftime(format)
    else:
        raise ValueError('interval error')
    return (now_time.strftime(format),delta_time)


def marshall_now(now=None):
    """
    Make an rpc-safe datetime with microseconds.
    eg:{'day': 10, 'month': 8, 'year': 2023, 'hour': 15, 'minute': 27, 'second': 21, 'microsecond': 829788}
    """
    if not now:
        now = utcnow()
    d = dict(day=now.day, month=now.month, year=now.year, hour=now.hour,
             minute=now.minute, second=now.second,
             microsecond=now.microsecond)
    if now.tzinfo:
        # Need to handle either iso8601 or python UTC format
        tzname = now.tzinfo.tzname(None)
        d['tzname'] = 'UTC' if tzname == 'UTC+00:00' else tzname
    return d


def unmarshall_time(tyme):
    """Unmarshall a datetime dict.
    eg: {'day': 10, 'month': 8, 'year': 2023, 'hour': 15, 'minute': 28, 'second': 27, 'microsecond': 437671}
    ->2023-08-10 15:28:27.437984
    """
    # NOTE(ihrachys): datetime does not support leap seconds,
    # so the best thing we can do for now is dropping them
    # http://bugs.python.org/issue23574
    second = min(tyme['second'], _MAX_DATETIME_SEC)
    dt = datetime.datetime(day=tyme['day'],
                           month=tyme['month'],
                           year=tyme['year'],
                           hour=tyme['hour'],
                           minute=tyme['minute'],
                           second=second,
                           microsecond=tyme['microsecond'])
    tzname = tyme.get('tzname')
    if tzname:
        # Need to handle either iso8601 or python UTC format
        tzname = 'UTC' if tzname == 'UTC+00:00' else tzname

        if zoneinfo:
            tzinfo = zoneinfo.ZoneInfo(tzname)
            dt = dt.replace(tzinfo=tzinfo)
        else:
            tzinfo = pytz.timezone(tzname)
            dt = tzinfo.localize(dt)

    return dt

def delta_seconds(before, after):
    """Return the difference between two timing objects.

    Compute the difference in seconds between two date, time, or
    datetime objects (as a float, to microsecond resolution).

    eg:
    from datetime import datetime
    # 创建一个日期对象
    before = datetime(2023, 7, 5)
    # 创建一个日期时间对象
    after = datetime(2023, 7, 6)
    -> 86400.0
    """
    delta = after - before
    return delta.total_seconds()


def exec_time(start_time, end_time):
    """
    返回两个时间戳的时间差
    :param start_time:
    :param end_time:
    :return:
    """
    return "{:.2f} s".format(end_time - start_time)


def get_ts(ts=None):
    """
    获取当前UTC时间
    :param ts:
    :return: example->2022-06-13T04:41:55Z
    """
    if not ts:
        ts = time.gmtime()
    return time.strftime(ISO8601, ts)


def parse_ts(ts):
    """
    返回时间戳
    :param ts:
    :return:
    """
    ts = ts.strip()
    try:
        ts_s = time.strptime(ts, ISO8601)
        return time.mktime(ts_s)
    except ValueError:
        try:
            ts_s = time.strptime(ts, ISO8601_MS)
            return time.mktime(ts_s)
        except ValueError:
            return 0


def local_ts(utc_ts):
    """
    UTC时间转时间戳
    :param utc_ts:2022-05-31T16:00:00.000Z  ->   1653994800.0
    :return:
    """
    ts = parse_ts(utc_ts)
    if ts:
        return ts - (-10800)
    else:
        return 0


def get_asctime():
    """
    获取格式化的时间
    eg:Thu Aug 10 23:20:40 2023
    :return:
    """
    return time.asctime(time.localtime(time.time()))


def utc_to_local(utc_time,format=ISO8601_MS):
    """
    UTC时间转换为本地时间
    :utc_time:UTC时间字符串
    :return:
    eg：2022-05-31T16:00:00.000Z  -> 2022-06-01 00:00:00
    """
    utc_time = datetime.datetime.strptime(utc_time, format)
    local_time = utc_time + datetime.timedelta(hours=8)
    return local_time

def format_timer(allTime):
    """
    秒转成格式化时间
    :param allTime:sec
    :return:
    eg:1d:3h:46m:40s
    2h:46m:40s
    1m:40s
    59s
    """
    day = 24 * 60 * 60
    hour = 60 * 60
    min = 60
    if allTime < 60:
        return f"{math.ceil(allTime)}s"
    elif allTime > day:
        days = divmod(allTime, day)
        return f"{int(days[0])}d:{format_timer(days[1])}"
    elif allTime > hour:
        hours = divmod(allTime, hour)
        return f"{int(hours[0])}h:{format_timer(hours[1])}"
    else:
        mins = divmod(allTime, min)
        return f"{int(mins[0])}m:{math.ceil(mins[1])}s"


def yesterday(format="%Y-%m-%d"):
    """
    获取昨天日期
    :return: 今天的头一天的日期
    """
    now_time = datetime.datetime.now()
    return (now_time + datetime.timedelta(days=-1)).strftime(format)


def previous_date(n):
    """
    获取过去 N 天的日期
    :param n:
    :return:
    eg: 3 -> ['2023-08-04', '2023-08-05', '2023-08-06']
    """
    before_n_days = []
    for i in range(1, n + 1)[::-1]:
        before_n_days.append(
            str(datetime.date.today() - datetime.timedelta(days=i)))
    return before_n_days


def create_assist_date(datestart=None, dateend=None):
    """
    生成一段时间区间内的日期
    :param datestart:开始日期
    :param dateend:结束日期
    :return:
    eg:['2023-04-01', '2023-04-02', '2023-04-03']
    """
    if datestart is None:
        datestart = '2022-01-01'
    if dateend is None:
        dateend = datetime.datetime.now().strftime('%Y-%m-%d')

    datestart = datetime.datetime.strptime(datestart, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(dateend, '%Y-%m-%d')
    date_list = []
    date_list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend:
        datestart += datetime.timedelta(days=+1)
        date_list.append(datestart.strftime('%Y-%m-%d'))
    return date_list


def strftimer(flag=0):
    """
    获取时间和日期
    eg:
    flag = 0为时间和日期         eg:2018-04-11 10:04:55
    flag = 1仅获取日期           eg:2018-04-11
    flag = 2仅获取时间           eg:10:04:55
    flag = 3纯数字的日期和时间    eg:20180411100455
    """
    now = time.localtime(time.time())
    if flag == 0:
        return time.strftime('%Y-%m-%d %H:%M:%S', now)
    if flag == 1:
        return time.strftime('%Y-%m-%d', now)
    if flag == 2:
        return time.strftime('%H:%M:%S', now)
    if flag == 3:
        return time.strftime('%Y%m%d%H%M%S', now)


def get_timestamp(fmt='s'):
    """
    返回当前unix时间戳
    :param unit:单位为s or ms
    :return:s->1655095947.66132  ms->1655095947661
    """
    if fmt == 's':
        return time.time()
    if fmt == 'ms':
        return round(time.time() * 1000)


def get_isoformat():
    """
    获取iso格式的时间
    eg:2022-06-13T13:05:36.887720
    """
    return datetime.datetime.now().isoformat()


def local_to_timestamp():
    """
    将本地时间转化为时间戳
    :return:
    eg:1691682215.0
    """
    return time.mktime(time.localtime())


def get_first_and_last_day(date):
    """
    获取某月的第一天和最后一天的日期
    :param date: '2023-08-28
    :return:
    eg: ('2023-08-01', '2023-08-31')
    """
    if date.count('-') != 2:
        raise ValueError('年月日规则输入错误')
    year, month = str(date).split('-')[0], str(date).split('-')[1]
    end = calendar.monthrange(int(year), int(month))[1]
    start_date = '%s-%s-01' % (year, month)
    end_date = '%s-%s-%s' % (year, month, end)
    return start_date, end_date


def iterate_months(start_year_month, end_year_month):
    """
    Starting month
    迭代两个月份之间的月份
    :params: start_year_month: '2021-7'
    :params: end_year_month: '2022-08'
    :return: >>> list(iterate_months('2021-7', '2022-08'))
    ['2021-07', '2021-08', '2021-09', '2021-10', ..., '2022-07', '2022-08']
    """
    assert start_year_month <= end_year_month, '开始月份必须小于等于结束月份'
    year, month = start_year_month.split('-')
    year = int(year)
    month = int(month)

    end_year, end_month = end_year_month.split('-')
    end_year = int(end_year)
    end_month = int(end_month)
    assert month <= 12 and end_month <= 12, '月份必须在 1 - 12月之间'

    while True:
        yield '{}-{:02}'.format(year, month)
        if year == end_year and month == end_month:
            break
        else:
            month = ((month + 1) % 12) or 12
            if month == 1:
                year += 1


def get_datetime_range(year_month, to_timestamp=False):
    """
    获取给定月份的开始时间和结束时间
    :params: year_month: '2022-07'
    :return: (datetime.datetime(2022, 7, 1, 0, 0), datetime.datetime(2022, 7, 31, 23, 59, 59, 999999)) or (1656604800, 1659283199)
    """
    from datetime import date, datetime
    year, month = year_month.split('-')
    year = int(year)
    month = int(month)
    start_time = datetime.combine(date(year, month, 1), datetime.min.time())
    _end_date = date(year, month, calendar.monthrange(year, month)[1])
    end_time = datetime.combine(_end_date, datetime.max.time())
    if to_timestamp:
        start_time = int(time.mktime(start_time.timetuple()))
        end_time = int(time.mktime(end_time.timetuple()))
    return start_time, end_time