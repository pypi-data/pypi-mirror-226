import hashlib
import json
import os
import time
import uuid
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from pathlib import Path
from shutil import rmtree
from subprocess import CompletedProcess
from subprocess import run as subprocess_run
from time import mktime, strptime
from typing import Callable

from loguru import logger

# --------------------------------------------------------------------------------------------------


# None Type
NoneType = type(None)


# --------------------------------------------------------------------------------------------------


def v_true(
    v_instance: any = None,
    v_type: any = None,
    true_list: list | tuple | set | str = None,
    false_list: list | tuple | set | str = None,
    debug: bool = False
) -> bool:
    """
    检查变量类型以及变量是否为真
    """
    """
    常见类型:

        Boolean     bool            False
        Numbers     int/float       0/0.0
        String      str             ""
        List        list/tuple/set  []/()/{}
        Dictionary  dict            {}

    函数使用 callable(func) 判断
    """
    try:
        if isinstance(v_instance, v_type):
            if true_list is not None and false_list is None and (
                    isinstance(true_list, list) or
                    isinstance(true_list, tuple) or
                    isinstance(true_list, set) or
                    isinstance(true_list, str)
            ):
                return True if v_instance in true_list else False
            elif true_list is None and false_list is not None and (
                    isinstance(false_list, list) or
                    isinstance(false_list, tuple) or
                    isinstance(false_list, set) or
                    isinstance(false_list, str)
            ):
                return True if v_instance not in false_list else False
            elif true_list is not None and false_list is not None and (
                    isinstance(true_list, list) or
                    isinstance(true_list, tuple) or
                    isinstance(true_list, set) or
                    isinstance(true_list, str)
            ) and (
                    isinstance(false_list, list) or
                    isinstance(false_list, tuple) or
                    isinstance(false_list, set) or
                    isinstance(false_list, str)
            ):
                return True if (v_instance in true_list) and (v_instance not in false_list) else False
            else:
                return True if v_instance not in [False, None, 0, 0.0, '', (), [], {*()}, {*[]}, {*{}}, {}] else False
        else:
            return False
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return False


# --------------------------------------------------------------------------------------------------


def mam_of_numbers(
    numbers: list | tuple = None,
    dest_type: str = None,
    debug: bool = False
) -> tuple[int | float, int | float, int | float] | tuple[None, None, None]:
    """
    返回一组数字中的 最大值(maximum), 平均值(average), 最小值(minimum)
    numbers 数字列表 (仅支持 list 和 tuple, 不支 set)
    dest_type 目标类型 (将数字列表中的数字转换成统一的类型)
    """
    try:
        _numbers = deepcopy(numbers)
        match True:
            case True if dest_type == 'float':
                _numbers = [float(i) for i in numbers]
            case True if dest_type == 'int':
                _numbers = [int(i) for i in numbers]
        _num_max = max(_numbers)
        _num_avg = sum(_numbers) / len(_numbers)
        _num_min = min(_numbers)
        return _num_max, _num_avg, _num_min
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None, None, None


def step_number_for_split_equally(
    integer: int = None,
    split_equally_number: int = None,
    debug: bool = False
) -> int | None:
    """
    平分数字的步长
    integer 数字
    split_equally_number 平分 integer 的数字
    """
    """
    示例:

        [1, 2, 3, 4, 5, 6, 7, 8, 9]

        分成 2 份 -> [[1, 2, 3, 4, 5], [6, 7, 8, 9]] -> 返回 5
        分成 3 份 -> [[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> 返回 3
        分成 4 份 -> [[1, 2, 3], [4, 5], [6, 7], [8, 9]] -> 返回 3
        分成 5 份 -> [[1, 2], [3, 4], [5, 6], [7, 8], [9]] -> 返回 2
    """
    try:
        if integer % split_equally_number == 0:
            return int(integer / split_equally_number)
        else:
            return int(integer / split_equally_number) + 1
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def division(
    dividend: int | float = None,
    divisor: int | float = None,
    debug: bool = False
) -> float | None:
    """
    除法
    """
    try:
        return dividend / divisor
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def divisor_1000(
    dividend: int | float = None,
    debug: bool = False
) -> float | None:
    """
    除法, 除以 1000
    """
    try:
        return dividend / 1000
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def divisor_1024(
    dividend: int | float = None,
    debug: bool = False
) -> float | None:
    """
    除法, 除以 1024
    """
    try:
        return dividend / 1024
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def divisor_square_1000(
    dividend: int | float = None,
    debug: bool = False
) -> float | None:
    """
    除法, 除以 1000的次方
    """
    try:
        return dividend / (1000 * 1000)
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def divisor_square_1024(
    dividend: int | float = None,
    debug: bool = False
) -> float | None:
    """
    除法, 除以 1024的次方
    """
    try:
        return dividend / (1024 * 1024)
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


# --------------------------------------------------------------------------------------------------


def check_file_type(
    file_object: str = None,
    file_type: any = None,
    debug: bool = False
) -> bool | None:
    """
    检查文件类型
    file_object 文件对象
    file_type 文件类型
    """
    try:
        _file_path = Path(file_object)
        match True:
            case True if _file_path.exists() is False:
                return False
            case True if file_type == 'absolute' and _file_path.is_absolute() is True:
                return True
            case True if file_type == 'block_device' and _file_path.is_block_device() is True:
                return True
            case True if file_type == 'dir' and _file_path.is_dir() is True:
                return True
            case True if file_type == 'fifo' and _file_path.is_fifo() is True:
                return True
            case True if file_type == 'file' and _file_path.is_file() is True:
                return True
            case True if file_type == 'mount' and _file_path.is_mount() is True:
                return True
            case True if file_type == 'relative_to' and _file_path.is_relative_to() is True:
                return True
            case True if file_type == 'reserved' and _file_path.is_reserved() is True:
                return True
            case True if file_type == 'socket' and _file_path.is_socket() is True:
                return True
            case True if file_type == 'symlink' and _file_path.is_symlink() is True:
                return True
            case _:
                return False
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return False


# --------------------------------------------------------------------------------------------------


def list_sort(
    data: list = None,
    deduplication: bool = None,
    debug: bool = False,
    **kwargs
) -> list | None:
    """
    列表排序, 示例: list_sort(['1.2.3.4', '2.3.4.5'], key=inet_aton)
    """
    """
    参考文档:
        https://stackoverflow.com/a/4183538
        https://blog.csdn.net/u013541325/article/details/117530957
    """
    try:

        # from ipaddress import ip_address
        # _ips = [str(i) for i in sorted(ip_address(ip.strip()) for ip in ips)]
        # 注意: list.sort() 是直接改变 list, 不会返回 list

        # 拷贝数据, 去重, 排序, 返回
        _data = deepcopy(data)
        if deduplication is True:
            _data = list(set(_data))
        _data.sort(**kwargs)
        return _data

    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def list_dict_sorted_by_key(
    data: list | tuple = None,
    key: str = None,
    debug: bool = False,
    **kwargs
) -> list | None:
    """
    列表字典排序
    """
    """
    参考文档:
        https://stackoverflow.com/a/73050
    """
    try:
        _data = deepcopy(data)
        return sorted(_data, key=lambda x: x[key], **kwargs)
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def list_split_by_step(
    data: list = None,
    number: int = None,
    debug: bool = False
) -> list | None:
    """
    列表分割
    """
    """
    示例:

        numbers = [1, 2, 3, 4, 5, 6, 7]

        list_split_by_step(numbers, 2)
        [[1, 2], [3, 4], [5, 6], [7]]

        list_split_by_step(numbers, 3)
        [[1, 2, 3], [4, 5, 6], [7]]
    """
    try:

        # 数据拷贝
        data_object = deepcopy(data)
        # 数据长度
        data_length = len(data_object)
        # 数据平分时, 每份数据的最大长度
        index_number_list = list(range(0, data_length, number))
        # 数据平分后的结果
        data_split = []

        if data_length == 0 or data_length <= number:
            data_split.append(data_object)
        else:
            for index_number in index_number_list:
                data_split.append(deepcopy(data_object[index_number:index_number + number]))

        return data_split

    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def list_split_equally(
    data: list = None,
    number: int = None,
    debug: bool = False
) -> list | None:
    """
    列表平分
    """
    """
    示例:

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

        list_split_equally(numbers, 5)
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19]]

        list_split_equally(numbers, 6)
        [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10], [11, 12, 13], [14, 15, 16], [17, 18, 19]]

        list_split_equally(numbers, 7)
        [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17], [18, 19]]
    """
    try:

        # 数据拷贝
        data_object = deepcopy(data)
        # 数据长度
        data_length = len(data_object)
        # 数据平分时, 每份数据的最大长度
        step_number = step_number_for_split_equally(data_length, number)
        # 数据平分后的结果
        data_split = []

        if data_length == 0 or data_length <= step_number:
            data_split.append(data_object)
        else:
            if data_length % number == 0:
                index_number_list = list(range(0, data_length, number))
                for index_number in index_number_list:
                    data_split.append(deepcopy(data_object[index_number:index_number + number]))
            else:
                # 前一部分
                previous_end_number = (data_length % number) * step_number
                previous_index_number_list = list(range(0, previous_end_number, step_number))
                for index_number in previous_index_number_list:
                    data_split.append(deepcopy(data_object[index_number:index_number + step_number]))
                # 后一部分
                next_number_list = list(range(previous_end_number, data_length, step_number - 1))
                for index_number in next_number_list:
                    data_split.append(deepcopy(data_object[index_number:index_number + (step_number - 1)]))

        return data_split

    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def list_print_by_step(
    data: list = None,
    number: int = None,
    separator: str = None,
    debug: bool = False
) -> list | None:
    """
    列表按照 步长 和 分隔符 有规律的输出
    """
    try:

        _data_list = list_split_by_step(data, number)

        for _item in _data_list:
            print(*_item, sep=separator)

    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def list_remove_list(
    original: list = None,
    remove: list = None,
    debug: bool = False
) -> list | None:
    try:
        _original = deepcopy(original)
        _remove = deepcopy(remove)
        return [i for i in _original if i not in _remove]
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def list_merge(
    data: list = None,
    debug: bool = False
) -> list | None:
    """合并 List 中的 List 为一个 List"""
    try:
        results = []
        for i in deepcopy(data):
            results += i
        return results
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def range_zfill(
    start: int = None,
    stop: int = None,
    step: int = None,
    width: int = None,
    debug: bool = False
) -> list | None:
    """生成长度相同的字符串的列表"""
    # 示例: range_zfill(8, 13, 1, 2) => ['08', '09', '10', '11', '12']
    # 生成 小时 列表: range_zfill(0, 24, 1, 2)
    # 生成 分钟和秒 列表: range_zfill(0, 60, 1, 2)
    # https://stackoverflow.com/a/733478
    # the zfill() method to pad a string with zeros
    try:
        return [str(i).zfill(width) for i in range(start, stop, step)]
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


# --------------------------------------------------------------------------------------------------


def dict_nested_update(
    data: dict = None,
    key: str = None,
    value: any = None,
    debug: bool = False
) -> dict | None:
    """
    dictionary nested update
    https://stackoverflow.com/a/58885744
    """
    try:
        if v_true(data, dict):
            for _k, _v in data.items():
                # callable() 判断是非为 function
                if (key is not None and key == _k) or (callable(key) is True and key() == _k):
                    if callable(value) is True:
                        data[_k] = value()
                    else:
                        data[_k] = value
                elif isinstance(_v, dict) is True:
                    dict_nested_update(_v, key, value)
                elif isinstance(_v, list) is True:
                    for _o in _v:
                        if isinstance(_o, dict):
                            dict_nested_update(_o, key, value)
                else:
                    pass
        else:
            pass
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


# --------------------------------------------------------------------------------------------------


def filename(
    file: str = None,
    split: str = '.',
    debug: bool = False
) -> str | None:
    """获取文件名称"""
    '''
    https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
    https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    '''
    try:
        if v_true(file, str) and file[-1] != '/' and v_true(split, str):
            _basename = str(os.path.basename(file))
            _index_of_dot = _basename.index(split)
            return _basename[:_index_of_dot]
        else:
            return None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def file_md5(
    file: str = None,
    debug: bool = False
) -> str | None:
    """获取文件MD5"""
    '''https://stackoverflow.com/a/59056837'''
    try:
        with open(file, "rb") as _file:
            file_hash = hashlib.md5()
            while chunk := _file.read(8192):
                file_hash.update(chunk)
            return file_hash.hexdigest()
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def file_size(
    file: str = None,
    debug: bool = False
) -> int | None:
    """获取文件大小"""
    try:
        return os.path.getsize(file)
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


# --------------------------------------------------------------------------------------------------


def resolve_path() -> str | None:
    """获取当前目录名称"""
    return str(Path().resolve())


def parent_path(
    path: str = None,
    debug: bool = False,
    **kwargs
) -> str | None:
    """获取父目录名称"""
    try:
        return str(Path(path, **kwargs).parent.resolve()) if v_true(path, str) else None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def real_path(
    path: str = None,
    debug: bool = False,
    **kwargs
) -> str | None:
    """获取真实路径"""
    try:
        return os.path.realpath(path, **kwargs) if v_true(path, str) else None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


# --------------------------------------------------------------------------------------------------


def retry(
    times: int = None,
    func: Callable = None,
    debug: bool = False,
    **kwargs
) -> any:
    """重试"""
    """
    函数传递参数: https://stackoverflow.com/a/803632
    callable() 判断类型是非为函数: https://stackoverflow.com/a/624939
    """
    try:
        _num = 0
        while True:
            # 重试次数判断 (0 表示无限次数, 这里条件使用 > 0, 表示有限次数)
            if times > 0:
                _num += 1
                if _num > times:
                    return
            # 执行函数
            try:
                return func(**kwargs)
            except Exception as e:
                if debug is True:
                    logger.exception(e)
                else:
                    logger.error(e)
                logger.success('retrying ...')
                continue
            # break
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


# --------------------------------------------------------------------------------------------------


"""
日期时间有两种: UTC datetime (UTC时区日期时间) 和 Local datetime (当前时区日期时间)

Unix Timestamp 仅为 UTC datetime 的值

但是, Local datetime 可以直接转换为 Unix Timestamp, UTC datetime 需要先转换到 UTC TimeZone 再转换为 Unix Timestamp

相反, Unix Timestamp 可以直接转换为 UTC datetime, 要获得 Local datetime, 需要再将 UTC datetime 转换为 Local datetime

    https://stackoverflow.com/a/13287083
    https://stackoverflow.com/a/466376
    https://stackoverflow.com/a/7999977
    https://stackoverflow.com/a/3682808
    https://stackoverflow.com/a/63920772
    https://www.geeksforgeeks.org/how-to-remove-timezone-information-from-datetime-object-in-python/

pytz all timezones

    https://stackoverflow.com/a/13867319
    https://stackoverflow.com/a/15692958

    import pytz
    pytz.all_timezones
    pytz.common_timezones
    pytz.timezone('US/Eastern')

timezone

    https://stackoverflow.com/a/39079819
    https://stackoverflow.com/a/1681600
    https://stackoverflow.com/a/4771733
    https://stackoverflow.com/a/63920772
    https://toutiao.io/posts/sin4x0/preview

其它:

    dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    (dt.replace(tzinfo=timezone.utc).astimezone(tz=None)).strftime(format)
    datetime.fromisoformat((dt.replace(tzinfo=timezone.utc).astimezone(tz=None)).strftime(format))
    string_to_datetime((dt.replace(tzinfo=timezone.utc).astimezone(tz=None)).strftime(format), format)

    datetime.fromisoformat(time.strftime(format, time.gmtime(dt)))
"""


def date_to_datetime(
    date_object: datetime = None,
    debug: bool = False
) -> datetime | None:
    """'日期'转换为'日期时间'"""
    # https://stackoverflow.com/a/1937636
    try:
        return datetime.combine(date_object, datetime.min.time())
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def datetime_to_date(
    date_time: datetime = None,
    debug: bool = False
) -> date | None:
    """'日期时间'转换为'日期'"""
    # https://stackoverflow.com/a/3743240
    try:
        return date_time.date()
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def local_timezone():
    """获取当前时区"""
    return datetime.now(timezone.utc).astimezone().tzinfo


def datetime_now(
        debug: bool = False,
        **kwargs
) -> datetime | None:
    """获取当前日期和时间"""
    _utc = kwargs.pop("utc", False)
    try:
        return datetime.utcnow() if _utc is True else datetime.now(**kwargs)
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def datetime_offset(
    date_time: datetime = None,
    debug: bool = False,
    **kwargs
) -> datetime | None:
    """获取'向前或向后特定日期时间'的日期和时间"""
    _utc = kwargs.pop("utc", False)
    try:
        if isinstance(date_time, datetime):
            return date_time + timedelta(**kwargs)
        else:
            return datetime.utcnow() + timedelta(**kwargs) if _utc is True else datetime.now() + timedelta(**kwargs)
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def datetime_to_string(
    date_time: datetime = None,
    string_format: str = '%Y-%m-%d %H:%M:%S',
    debug: bool = False
) -> str | None:
    """'日期时间'转换为'字符串'"""
    try:
        return datetime.strftime(date_time, string_format) if isinstance(date_time, datetime) is True else None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def datetime_to_timestamp(
    date_time: datetime = None,
    utc: bool = False,
    debug: bool = False
) -> int | None:
    """
    Datatime 转换为 Unix Timestamp
    Local datetime 可以直接转换为 Unix Timestamp
    UTC datetime 需要先替换 timezone 再转换为 Unix Timestamp
    """
    try:
        if isinstance(date_time, datetime):
            return int(date_time.replace(tzinfo=timezone.utc).timestamp()) if utc is True else int(date_time.timestamp())
        else:
            return None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def datetime_local_to_timezone(
    date_time: datetime = None,
    tz: timezone = timezone.utc,
    debug: bool = False
) -> datetime | None:
    """
    Local datetime to TimeZone datetime (默认转换为 UTC datetime)
    replace(tzinfo=None) 移除结尾的时区信息
    """
    try:
        return (datetime.fromtimestamp(date_time.timestamp(), tz=tz)).replace(tzinfo=None) if isinstance(date_time, datetime) is True else None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def datetime_utc_to_timezone(
    date_time: datetime = None,
    tz: timezone = datetime.now(timezone.utc).astimezone().tzinfo,
    debug: bool = False
) -> datetime | None:
    """
    UTC datetime to TimeZone datetime (默认转换为 Local datetime)
    replace(tzinfo=None) 移除结尾的时区信息
    """
    try:
        return date_time.replace(tzinfo=timezone.utc).astimezone(tz).replace(tzinfo=None) if isinstance(date_time, datetime) is True else None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def timestamp_to_datetime(
    timestamp: int = None,
    tz: timezone = timezone.utc,
    debug: bool = False
) -> datetime | None:
    """Unix Timestamp 转换为 Datatime"""
    try:
        return (datetime.fromtimestamp(timestamp, tz=tz)).replace(tzinfo=None) if v_true(timestamp, int) else None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def datetime_string_to_datetime(
    datetime_string: str = None,
    datetime_format: str = '%Y-%m-%d %H:%M:%S',
    debug: bool = False
) -> datetime | None:
    try:
        return datetime.strptime(datetime_string, datetime_format) if v_true(datetime_string, str) else None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def datetime_string_to_timestamp(
    datetime_string: str = None,
    datetime_format: str = '%Y-%m-%d %H:%M:%S',
    debug: bool = False
) -> int | None:
    try:
        return int(mktime(strptime(datetime_string, datetime_format))) if v_true(datetime_string, str) else None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def datetime_object(
    date_time: datetime = None,
    debug: bool = False
) -> dict | None:
    try:
        return {
            'date': date_time.strftime("%Y-%m-%d"),
            'time': date_time.strftime("%H:%M:%S"),
            'datetime_now': date_time.strftime("%Y-%m-%d %H:%M:%S"),
            'datetime_zero': date_time.strftime('%Y-%m-%d 00:00:00')
        }
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


# --------------------------------------------------------------------------------------------------


'''
run_cmd = bash('echo ok', universal_newlines=True, stdout=PIPE)

if run_cmd != None:
    returncode = run_cmd.returncode
    outputs = run_cmd.stdout.splitlines()
    print(returncode, type(returncode))
    print(outputs, type(outputs))

# echo 'echo ok' > /tmp/ok.sh
run_script = bash('/tmp/ok.sh', file=True, universal_newlines=True, stdout=PIPE)

if run_script != None:
    returncode = run_script.returncode
    outputs = run_script.stdout.splitlines()
    print(returncode, type(returncode))
    print(outputs, type(outputs))
'''


def shell(
    cmd: str = None,
    isfile: bool = False,
    sh: str = '/bin/bash',
    debug: bool = False,
    **kwargs
) -> CompletedProcess | None:
    """run shell command or script"""
    try:
        match True:
            case True if not check_file_type(sh, 'file'):
                return None
            case True if v_true(sh, str) and v_true(cmd, str):
                if isfile is True:
                    return subprocess_run([sh, cmd], **kwargs)
                else:
                    return subprocess_run([sh, "-c", cmd], **kwargs)
            case _:
                return None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


# --------------------------------------------------------------------------------------------------


def json_file_parser(
    file: str = None,
    debug: bool = False
) -> dict | None:
    try:
        if check_file_type(file, 'file'):
            with open(file) as json_raw:
                json_dict = json.load(json_raw)
            return json_dict
        else:
            logger.error(f"No such file: {file}")
            return None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


"""
json_raw = '''
{
    "markdown.preview.fontSize": 14,
    "editor.minimap.enabled": false,
    "workbench.iconTheme": "vscode-icons",
    "http.proxy": "http://127.0.0.1:1087"

}
'''

print(json_sort(json_raw))

{
    "editor.minimap.enabled": false,
    "http.proxy": "http://127.0.0.1:1087",
    "markdown.preview.fontSize": 14,
    "workbench.iconTheme": "vscode-icons"
}
"""


def json_sort(
    string: str = None,
    debug: bool = False,
    **kwargs
) -> dict | None:
    try:
        return json.dumps(json.loads(string), indent=4, sort_keys=True, **kwargs) if v_true(string, str) else None
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


# --------------------------------------------------------------------------------------------------


def delete_files(
    files: str | list = None,
    debug: bool = False
) -> bool:
    """删除文件"""
    try:

        if v_true(files, str) and check_file_type(files, 'file'):

            os.remove(files)
            logger.success('deleted file: {}'.format(files))
            return True

        elif v_true(files, list):

            for _file in files:

                if v_true(_file, str) and check_file_type(_file, 'file'):
                    try:
                        os.remove(_file)
                        logger.success('deleted file: {}'.format(_file))
                    except Exception as e:
                        logger.error('error file: {} {}'.format(_file, e))
                else:
                    logger.error('error file: {}'.format(_file))

            return True

        else:

            logger.error('error file: {}'.format(files))
            return False

    except Exception as e:
        # logger.error('error file: {} {}'.format(files, e))
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return False


def delete_dirs(
    dirs: str | list = None,
    debug: bool = False
) -> bool:
    """
    delete directory

    https://docs.python.org/3/library/os.html#os.rmdir

        os.rmdir(path, *, dir_fd=None)

    Remove (delete) the directory path.

    If the directory does not exist or is not empty, an FileNotFoundError or an OSError is raised respectively.

    In order to remove whole directory trees, shutil.rmtree() can be used.

    https://docs.python.org/3/library/shutil.html#shutil.rmtree

        shutil.rmtree(path, ignore_errors=False, onerror=None)

    Delete an entire directory tree; path must point to a directory (but not a symbolic link to a directory).

    If ignore_errors is true, errors resulting from failed removals will be ignored;

    if false or omitted, such errors are handled by calling a handler specified by onerror or, if that is omitted, they raise an exception.
    """
    try:

        if v_true(dirs, str) and check_file_type(dirs, 'dir'):

            rmtree(dirs)
            logger.success('deleted directory: {}'.format(dirs))
            return True

        elif v_true(dirs, list):

            for _dir in dirs:

                if v_true(_dir, str) and check_file_type(_dir, 'dir'):
                    try:
                        rmtree(_dir)
                        logger.success('deleted directory: {}'.format(_dir))
                    except Exception as e:
                        logger.error('error directory: {} {}'.format(_dir, e))
                else:
                    logger.error('error directory: {}'.format(_dir))

            return True

        else:

            logger.error('error directory: {}'.format(dirs))
            return False

    except Exception as e:
        # logger.error('error directory: {} {}'.format(dirs, e))
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return False


# --------------------------------------------------------------------------------------------------


def pool_process(
    process_func: Callable = None,
    process_data: any = None,
    process_num: int = None,
    thread: bool = None,
    debug: bool = False,
    **kwargs
) -> list | bool:
    """
    Pool 进程池
    ThreadPool 线程池
    ThreadPool 共享内存, Pool 不共享内存
    ThreadPool 可以解决 Pool 在某些情况下产生的 Can't pickle local object 的错误
    https://stackoverflow.com/a/58897266
    """

    if callable(process_func) is False:
        logger.error('process function error')
        return False

    if v_true(process_data, list) is False:
        logger.error('process data error')
        return False

    if process_num is None:
        process_num = 1

    try:
        if v_true(process_num, int):
            if thread is True:
                with ThreadPool(process_num, **kwargs) as p:
                    return p.map(process_func, process_data)
            else:
                with Pool(process_num, **kwargs) as p:
                    return p.map(process_func, process_data)
        else:
            return False
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return False


# --------------------------------------------------------------------------------------------------


def create_empty_file(
    file: str = None,
    debug: bool = False
) -> str | None:
    try:
        if file is None:
            # 当前时间戳(纳秒)
            timestamp = time.time_ns()
            # 空文件路径
            file = f'/tmp/.{timestamp}.txt'
        # 创建一个空文件
        open(file, 'w').close()
        # 返回文件路径
        return file
    except Exception as e:
        if debug is True:
            logger.exception(e)
        else:
            logger.error(e)
        return None


# --------------------------------------------------------------------------------------------------


def uuid4_hex() -> str:
    return uuid.uuid4().hex
