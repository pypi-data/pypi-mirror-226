#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import uuid
import time
import string
import random
from math import ceil
from collections import Counter


def to_list(val):
    """
    转换list类型
    :param val:
    :return:
    """
    return list(val) if isinstance(val, (list, tuple, set)) else [val]

def to_text(value, encoding="utf-8"):
    """
    将值转换为unicode，默认编码为utf-8
    :param value: 需要转化的值
    :param encoding: 所需编码
    :return:
    """
    if not value:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode(encoding)
    return str(value)

def to_binary(value, encoding="utf-8"):
    """
    将值转换为二进制字符串，默认编码为utf-8
    :param value: 需要转化的值
    :param encoding: 所需编码
    """
    if not value:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode(encoding)
    return to_text(value).encode(encoding)

def find_str(s:str,specific_str:str):
    """
    判断字符串中是否有指定的字符串。存在返回True,不存在返回False
    """
    if s.find(specific_str) == -1:
        return False
    else:
        return True

def random_ip_by_address(ip_address):
    """
    随机生成一个同网段的ip地址
    :param ip_address: 172.16.1.254
    :return:
    """
    s = ip_address.split('.')
    s[-1] = str(random.randint(1,253))
    n_s = '.'.join(s)
    return n_s

def find_duplicate_elements(lst):
    """
    找出列表中的重复元素
    """
    seen = set()
    duplicates = set()
    for element in lst:
        if element in seen:
            duplicates.add(element)
        else:
            seen.add(element)
    return list(duplicates)

def rand_name(name='', prefix='qingcloud_api_test'):
    """
    生成一个包含随机数的随机名称
    :param str name: The name that you want to include
    :param str prefix: The prefix that you want to include
    :return: a random name. The format is
             '<prefix>-<name>-<random number>'.
             (e.g. 'qingcloud_api_test-namebar-154876201')
    :rtype: string
    """
    rand_name = str(random.randint(1, 0x7fffffff))
    if name:
        rand_name = name + '-' + rand_name
    if prefix:
        rand_name = prefix + '-' + rand_name
    return rand_name

def rand_uuid():
    """
    生成一个随机UUID字符串
    :return: a random UUID (e.g. '1dc12c7d-60eb-4b61-a7a2-17cf210155b6')
    :rtype: string
    """
    return str(uuid.uuid4())

def rand_uuid_hex():
    """
    生成一个随机的UUID十六进制字符串
    :return: a random UUID (e.g. '0b98cf96d90447bda4b46f31aeb1508c')
    :rtype: string
    """
    return uuid.uuid4().hex

def rand_password(length=15):
    """
    生成随机密码
    :param int length: The length of password that you expect to set
                       (If it's smaller than 3, it's same as 3.)
    :return: a random password. The format is
        ``'<random upper letter>-<random number>-<random special character>
        -<random ascii letters or digit characters or special symbols>'``
        (e.g. ``G2*ac8&lKFFgh%2``)
    :rtype: string
    """
    upper = random.choice(string.ascii_uppercase)
    ascii_char = string.ascii_letters
    digits = string.digits
    digit = random.choice(string.digits)
    puncs = '~!@#%^&*_=+'
    punc = random.choice(puncs)
    seed = ascii_char + digits + puncs
    pre = upper + digit + punc
    password = pre + ''.join(random.choice(seed) for x in range(length - 3))
    return password

def resource_replace(resource_ids: list, character: str) -> list:
    """
    替换资源名称，例如eip-xxxx,替换为:eipt-xxxx
    :param resource_ids:例如为['eip-xxxx']
    :param character:例如为't-'
    :return:
    """
    resource_list = []
    for resouce_id in resource_ids:
        a = resouce_id.split('-')
        a = a[0] + character + a[1]
        resource_list.append(a)
    return resource_list

def generate_txt_file(file_size=None, filepath='./'):
    """
    生成指定大小的txt文档
    :param file_size: 单位Byte
    :param filepath: 文件路径
    :return:
    """
    if file_size <= 0:
        raise ValueError("file size is not less that 0")
    if not filepath:
        raise ValueError("file path is not none")
    fileSize = int(file_size)
    filename = time.strftime('%Y%m%d%H%M%S', time.localtime(
        time.time())) + '_' + str(file_size) + 'Byte.txt'
    f = open(filepath + filename, 'w')
    for i in range(fileSize):
        try:
            f.write('1')
        except Exception:
            f.close()
            exit(-1)
    f.close()
    return filename

def format_byte(number=None):
    """
    格式化文件大小的函数
    :param number: 要格式化的字节数
    :return:
    example:
    format_byte(4096)
    """
    if not number:
        raise ValueError("number is not none..")
    for (scale, label) in [(1024 * 1024 * 1024, "GB"),
                           (1024 * 1024, "MB"), (1024, "KB")]:
        if number >= scale:
            return "%.2f %s" % (number * 1.0 / scale, label)
        elif number == 1:
            return "1 字节"
        else:
            byte = "%.2f" % (number or 0)
    # 去掉结尾的.00，并且加上单位字节
    return (byte[:-3] if byte.endswith('.00') else byte) + " 字节"


def is_all_chinese(strs):
    """
    检验是否全是中文字符
    :param strs:
    :return:
    """
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def is_contains_chinese(strs):
    """
    检验是否含有中文字符
    :param strs:
    :return:
    """
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def all_unique(lst: list):
    """
    检查列表元素中是否包含重复元素
    :param lst:
    :return:x = [1,1,2,2,3,2,3,4,5,6]，y = [1,2,3,4,5]，all_unique(x) # False，all_unique(y) # True
    """
    return len(lst) == len(set(lst))

def anagram(first: str, second: str):
    """
    检查两个字符串的组成元素是不是一样的
    :param first:
    :param second:
    :return:anagram("abcd3", "3acdb") # True
    """
    return Counter(first) == Counter(second)

def chunk(lst: list, size: int):
    """
    根据指定的大小切割列表
    :param lst:
    :param size:
    :return: chunk([1,2,3,4,5],2) # [[1,2],[3,4],5]
    """
    return list(
        map(lambda x: lst[x * size:x * size + size],
            list(range(0, ceil(len(lst) / size)))))

def compact(lst: list):
    """
    去掉布尔值(False, None, 0, "")，并返回新列表
    :param lst:
    :return:compact([0, 1, False, 2, '', 3, 'a', 's', 34]) # [ 1, 2, 3, 'a', 's', 34 ]
    """
    return list(filter(bool, lst))

def deep_flatten(lst: list):
    """
    将嵌套列表展开为单个列表
    :param lst:
    :return:deep_flatten([1, [2], [[3], 4], 5]) # [1,2,3,4,5]
    """
    def spread(arg):
        ret = []
        for i in arg:
            if isinstance(i, list):
                ret.extend(i)
            else:
                ret.append(i)
        return ret
    result = []
    result.extend(
        spread(list(map(lambda x: deep_flatten(x) if isinstance(x, list) else x, lst))))
    return result

def rand_url():
    """
    生成包含随机数的随机url
    :return: a random url. The format is 'https://url-<random number>.com'.
             (e.g. 'https://url-154876201.com')
    :rtype: string
    """
    randbits = str(random.randint(1, 0x7fffffff))
    return 'https://url-' + randbits + '.com'

def rand_int_id(start=0, end=0x7fffffff):
    """
    生成一个随机整数值
    :param int start: The value that you expect to start here
    :param int end: The value that you expect to end here
    :return: a random integer value
    :rtype: int
    """
    return random.randint(start, end)

def rand_mac_address():
    """
    生成随机MAC地址
    :return: an random Ethernet MAC address
    :rtype: string
    """
    mac = [0xfa, 0x16, 0x3e,
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(["%02x" % x for x in mac])

def rand_infiniband_guid_address():
    """
    生成ib GUID地址
    :return: an random Infiniband GUID address
    :rtype: string
    """
    guid = []
    for _ in range(8):
        guid.append("%02x" % random.randint(0x00, 0xff))
    return ':'.join(guid)

def difference(list_a: list, list_b: list):
    """
    返回两个列表的差
    :param list_a:
    :param list_b:
    :return:difference([1,2,3], [1,2,4]) # [3]
    """
    set_a = set(list_a)
    set_b = set(list_b)
    comparison1 = set_a.difference(set_b)
    comparison2 = set_b.difference(set_a)
    return list(comparison1) + list(comparison2)