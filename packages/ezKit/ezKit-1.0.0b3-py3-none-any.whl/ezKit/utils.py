import datetime
import hashlib
import json
import os
import subprocess
import time
from copy import deepcopy
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from pathlib import Path
from shutil import rmtree
from typing import Callable
from uuid import uuid4

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
        logger.exception(e) if debug is True else next
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
        logger.exception(e) if debug is True else next
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
        logger.exception(e) if debug is True else next
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
        logger.exception(e) if debug is True else next
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
        logger.exception(e) if debug is True else next
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
        logger.exception(e) if debug is True else next
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
        logger.exception(e) if debug is True else next
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
        logger.exception(e) if debug is True else next
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
        logger.exception(e) if debug is True else next
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
        logger.exception(e) if debug is True else next
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
        logger.exception(e) if debug is True else next
        return None


def list_split(
    data: list = None,
    number: int = None,
    equally: bool = False,
    debug: bool = False
) -> list | None:
    """
    列表分割
    """
    """
    默认: 将 list 以 number个元素为一个list 分割

        data = [1, 2, 3, 4, 5, 6, 7]

        list_split(data, 2) -> 将 data 以 2个元素为一个 list 分割
        [[1, 2], [3, 4], [5, 6], [7]]

        list_split(data, 3) -> 将 data 以 3个元素为一个 list 分割
        [[1, 2, 3], [4, 5, 6], [7]]

    equally 为 True 时, 将 data 平均分成 number 份

        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

        list_split_equally(data, 5) -> 将 data 平均分成 5 份
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19]]

        list_split_equally(data, 6) -> 将 data 平均分成 6 份
        [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10], [11, 12, 13], [14, 15, 16], [17, 18, 19]]

        list_split_equally(data, 7) -> 将 data 平均分成 7 份
        [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17], [18, 19]]
    """
    try:

        # 数据拷贝
        _data_object = deepcopy(data)
        # 数据长度
        _data_length = len(_data_object)
        # 数据平分后的结果
        _data_result = []

        if debug is True:
            logger.info(f"data object: {_data_object}")
            logger.info(f"data length: {_data_length}")

        if _data_length < number:
            logger.error('number must greater than data length') if debug is True else next
            return None
        elif _data_length == number:
            _data_result = [[i] for i in _data_object]
        else:

            if equally is True:

                # 数据平分时, 每份数据的最大长度
                _step_number = step_number_for_split_equally(_data_length, number, debug=debug)
                logger.info(f"step number: {_step_number}") if debug is True else next
                if _data_length % number == 0:
                    index_number_list = list(range(0, _data_length, number))
                    logger.info(f"index number list: {index_number_list}") if debug is True else next
                    for index_number in index_number_list:
                        logger.info(f"index: {index_number}, data: {_data_object[index_number:index_number + number]}") if debug is True else next
                        _data_result.append(deepcopy(_data_object[index_number:index_number + number]))
                else:
                    # 前一部分
                    previous_end_number = (_data_length % number) * _step_number
                    previous_index_number_list = list(range(0, previous_end_number, _step_number))
                    for index_number in previous_index_number_list:
                        _data_result.append(deepcopy(_data_object[index_number:index_number + _step_number]))
                    # 后一部分
                    next_number_list = list(range(previous_end_number, _data_length, _step_number - 1))
                    for index_number in next_number_list:
                        _data_result.append(deepcopy(_data_object[index_number:index_number + (_step_number - 1)]))

            else:

                for index_number in list(range(0, _data_length, number)):
                    _data_result.append(deepcopy(_data_object[index_number:index_number + number]))

        return _data_result

    except Exception as e:
        logger.exception(e) if debug is True else next
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
        _data_list = list_split(data, number, debug=debug)
        for _item in _data_list:
            print(*_item, sep=separator)
    except Exception as e:
        logger.exception(e) if debug is True else next
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
        logger.exception(e) if debug is True else next
        return None


def list_merge(
    data: list = None,
    debug: bool = False
) -> list | None:
    """合并 List 中的 List 为一个 List"""
    try:
        _results = []
        for i in deepcopy(data):
            _results += i
        return _results
    except Exception as e:
        logger.exception(e) if debug is True else next
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
        logger.exception(e) if debug is True else next
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
        if v_true(data, dict, debug=debug):
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
        logger.exception(e) if debug is True else next
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
        if debug is True:
            logger.info(f"file: {file}")
            logger.info(f"split: {split}")
        _basename = str(os.path.basename(file))
        logger.info(f"basename: {_basename}") if debug is True else next
        _index_of_split = _basename.index(split)
        logger.info(f"index of split: {_index_of_split}") if debug is True else next
        logger.info(f"filename: {_basename[:_index_of_split]}") if debug is True else next
        return _basename[:_index_of_split]
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def filehash(
    file: str = None,
    sha: str = 'md5',
    debug: bool = False
) -> str | None:
    """获取文件Hash"""
    """
    参考文档:
        https://stackoverflow.com/a/59056837
        https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
    """
    try:
        with open(file, "rb") as _file:
            match True:
                case True if sha == 'sha1':
                    file_hash = hashlib.sha1()
                case True if sha == 'sha224':
                    file_hash = hashlib.sha224()
                case True if sha == 'sha256':
                    file_hash = hashlib.sha256()
                case True if sha == 'sha384':
                    file_hash = hashlib.sha384()
                case True if sha == 'sha512':
                    file_hash = hashlib.sha512()
                case True if sha == 'sha3_224':
                    file_hash = hashlib.sha3_224()
                case True if sha == 'sha3_256':
                    file_hash = hashlib.sha3_256()
                case True if sha == 'sha3_384':
                    file_hash = hashlib.sha3_384()
                case True if sha == 'sha3_512':
                    file_hash = hashlib.sha3_512()
                case True if sha == 'shake_128':
                    file_hash = hashlib.shake_128()
                case True if sha == 'shake_256':
                    file_hash = hashlib.shake_256()
                case _:
                    file_hash = hashlib.md5()
            # 建议设置为和 block size 相同的值, 多数系统默认为 4096, 可使用 stat 命令查看
            # stat / (IO Block)
            # stat -f / (Block size)
            while chunk := _file.read(4096):
                file_hash.update(chunk)
            return file_hash.hexdigest()
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def filesize(
    file: str = None,
    debug: bool = False
) -> int | None:
    """获取文件大小"""
    try:
        return os.path.getsize(file)
    except Exception as e:
        logger.exception(e) if debug is True else next
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
        return str(Path(path, **kwargs).parent.resolve()) if v_true(path, str, debug=debug) else None
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def real_path(
    path: str = None,
    debug: bool = False,
    **kwargs
) -> str | None:
    """获取真实路径"""
    try:
        logger.info(f"path: {path}") if debug is True else next
        return os.path.realpath(path, **kwargs)
    except Exception as e:
        logger.exception(e) if debug is True else next
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
                logger.exception(e) if debug is True else next
                logger.success('retrying ...')
                continue
            # break
    except Exception as e:
        logger.exception(e) if debug is True else next
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
    date_object: datetime.datetime = None,
    debug: bool = False
) -> datetime.datetime | None:
    """'日期'转换为'日期时间'"""
    # https://stackoverflow.com/a/1937636
    try:
        return datetime.datetime.combine(date_object, datetime.datetime.min.time())
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def datetime_to_date(
    date_time: datetime.datetime = None,
    debug: bool = False
) -> datetime.date | None:
    """'日期时间'转换为'日期'"""
    # https://stackoverflow.com/a/3743240
    try:
        return date_time.date()
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def local_timezone():
    """获取当前时区"""
    return datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo


def datetime_now(
        debug: bool = False,
        **kwargs
) -> datetime.datetime | None:
    """获取当前日期和时间"""
    _utc = kwargs.pop("utc", False)
    try:
        return datetime.datetime.utcnow() if _utc is True else datetime.datetime.now(**kwargs)
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def datetime_offset(
    date_time: datetime.datetime = None,
    debug: bool = False,
    **kwargs
) -> datetime.datetime | None:
    """获取'向前或向后特定日期时间'的日期和时间"""
    _utc = kwargs.pop("utc", False)
    try:
        if isinstance(date_time, datetime.datetime):
            return date_time + datetime.timedelta(**kwargs)
        else:
            return datetime.datetime.utcnow() + datetime.timedelta(**kwargs) if _utc is True else datetime.datetime.now() + datetime.timedelta(**kwargs)
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def datetime_to_string(
    date_time: datetime.datetime = None,
    string_format: str = '%Y-%m-%d %H:%M:%S',
    debug: bool = False
) -> str | None:
    """'日期时间'转换为'字符串'"""
    try:
        return datetime.datetime.strftime(date_time, string_format) if isinstance(date_time, datetime.datetime) is True else None
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def datetime_to_timestamp(
    date_time: datetime.datetime = None,
    utc: bool = False,
    debug: bool = False
) -> int | None:
    """
    Datatime 转换为 Unix Timestamp
    Local datetime 可以直接转换为 Unix Timestamp
    UTC datetime 需要先替换 timezone 再转换为 Unix Timestamp
    """
    try:
        if isinstance(date_time, datetime.datetime):
            return int(date_time.replace(tzinfo=datetime.timezone.utc).timestamp()) if utc is True else int(date_time.timestamp())
        else:
            return None
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def datetime_local_to_timezone(
    date_time: datetime.datetime = None,
    tz: datetime.timezone = datetime.timezone.utc,
    debug: bool = False
) -> datetime.datetime | None:
    """
    Local datetime to TimeZone datetime (默认转换为 UTC datetime)
    replace(tzinfo=None) 移除结尾的时区信息
    """
    try:
        return (datetime.datetime.fromtimestamp(date_time.timestamp(), tz=tz)).replace(tzinfo=None) if isinstance(date_time, datetime.datetime) is True else None
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def datetime_utc_to_timezone(
    date_time: datetime.datetime = None,
    tz: datetime.timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo,
    debug: bool = False
) -> datetime.datetime | None:
    """
    UTC datetime to TimeZone datetime (默认转换为 Local datetime)
    replace(tzinfo=None) 移除结尾的时区信息
    """
    try:
        return date_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz).replace(tzinfo=None) if isinstance(date_time, datetime.datetime) is True else None
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def timestamp_to_datetime(
    timestamp: int = None,
    tz: datetime.timezone = datetime.timezone.utc,
    debug: bool = False
) -> datetime.datetime | None:
    """Unix Timestamp 转换为 Datatime"""
    try:
        return (datetime.datetime.fromtimestamp(timestamp, tz=tz)).replace(tzinfo=None) if v_true(timestamp, int, debug=debug) else None
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def datetime_string_to_datetime(
    datetime_string: str = None,
    datetime_format: str = '%Y-%m-%d %H:%M:%S',
    debug: bool = False
) -> datetime.datetime | None:
    try:
        return datetime.datetime.strptime(datetime_string, datetime_format) if v_true(datetime_string, str, debug=debug) else None
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def datetime_string_to_timestamp(
    datetime_string: str = None,
    datetime_format: str = '%Y-%m-%d %H:%M:%S',
    debug: bool = False
) -> int | None:
    try:
        return int(time.mktime(time.strptime(datetime_string, datetime_format))) if v_true(datetime_string, str, debug=debug) else None
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


def datetime_object(
    date_time: datetime.datetime = None,
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
        logger.exception(e) if debug is True else next
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
) -> subprocess.CompletedProcess | None:
    """run shell command or script"""
    try:
        match True:
            case True if not check_file_type(sh, 'file', debug=debug):
                return None
            case True if v_true(sh, str, debug=debug) and v_true(cmd, str, debug=debug):
                if isfile is True:
                    return subprocess.run([sh, cmd], **kwargs)
                else:
                    return subprocess.run([sh, "-c", cmd], **kwargs)
            case _:
                return None
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


# --------------------------------------------------------------------------------------------------


def json_file_parser(
    file: str = None,
    debug: bool = False
) -> dict | None:
    try:
        if check_file_type(file, 'file', debug=debug):
            with open(file) as json_raw:
                json_dict = json.load(json_raw)
            return json_dict
        else:
            logger.error(f"No such file: {file}")
            return None
    except Exception as e:
        logger.exception(e) if debug is True else next
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
        return json.dumps(json.loads(string), indent=4, sort_keys=True, **kwargs) if v_true(string, str, debug=debug) else None
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


# --------------------------------------------------------------------------------------------------


def delete_files(
    files: str | list = None,
    debug: bool = False
) -> bool:
    """删除文件"""
    try:

        if v_true(files, str, debug=debug) and check_file_type(files, 'file', debug=debug):

            os.remove(files)
            logger.success('deleted file: {}'.format(files))
            return True

        elif v_true(files, list, debug=debug):

            for _file in files:

                if v_true(_file, str, debug=debug) and check_file_type(_file, 'file', debug=debug):
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
        logger.exception(e) if debug is True else next
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

        if v_true(dirs, str, debug=debug) and check_file_type(dirs, 'dir', debug=debug):

            rmtree(dirs)
            logger.success('deleted directory: {}'.format(dirs))
            return True

        elif v_true(dirs, list, debug=debug):

            for _dir in dirs:

                if v_true(_dir, str, debug=debug) and check_file_type(_dir, 'dir', debug=debug):
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
        logger.exception(e) if debug is True else next
        return False


# --------------------------------------------------------------------------------------------------


def process_pool(
    process_func: Callable = None,
    process_data: any = None,
    process_num: int = 2,
    thread: bool = True,
    debug: bool = False,
    **kwargs
) -> list | bool:
    """
    多线程(MultiThread) | 多进程(MultiProcess)
    """
    """
    ThreadPool 线程池
    ThreadPool 共享内存, Pool 不共享内存
    ThreadPool 可以解决 Pool 在某些情况下产生的 Can't pickle local object 的错误
    https://stackoverflow.com/a/58897266
    """
    try:

        # 处理数据
        logger.info(f"data split ......") if debug is True else next
        if len(process_data) <= process_num:
            process_num = len(process_data)
            _data = process_data
        else:
            _data = list_split(process_data, process_num, equally=True, debug=debug)
        logger.info(f"data: {_data}") if debug is True else next

        # 执行函数
        if thread is True:
            # 多线程
            logger.info(f"execute multi thread ......") if debug is True else next
            with ThreadPool(process_num, **kwargs) as p:
                return p.map(process_func, _data)
        else:
            # 多进程
            logger.info(f"execute multi process ......") if debug is True else next
            with Pool(process_num, **kwargs) as p:
                return p.map(process_func, _data)

    except Exception as e:
        logger.exception(e) if debug is True else next
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
            logger.info(f"timestamp: {timestamp}") if debug is True else next
            # 空文件路径
            file = f'/tmp/empty_file_{timestamp}.txt'
        # 创建一个空文件
        logger.info(f"file: {file}") if debug is True else next
        open(file, 'w').close()
        # 返回文件路径
        return file
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None


# --------------------------------------------------------------------------------------------------


def uuid4_hex() -> str:
    return uuid4().hex


# --------------------------------------------------------------------------------------------------


def change_directory(
    directory: str = None,
    debug: bool = False
) -> bool:
    """改变目录"""
    try:
        directory = str(directory) if v_true(directory, str, debug=debug) else next
        logger.info(f"directory: {directory}") if debug is True else next
        if check_file_type(directory, 'dir', debug=debug):
            logger.info(f"change directory to {directory}") if debug is True else next
            os.chdir(directory)
            return True
        else:
            logger.error(f"no such directory: {directory}") if debug is True else next
            return False
    except Exception as e:
        logger.exception(e) if debug is True else next
        return False
