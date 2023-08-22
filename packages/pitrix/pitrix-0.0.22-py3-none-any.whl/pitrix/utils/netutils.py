#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import os
import re
import random
import socket
import netaddr
import requests
import ipaddress
import netifaces
from IPy import IP
from pitrix.utils.log import logger
from netaddr.core import INET_PTON
from netaddr.ip import IPAddress, IPRange, IPNetwork
from ping3 import ping,verbose_ping as ping_verbose
from concurrent.futures import ThreadPoolExecutor

def parse_host_port(address, default_port=None):
    """Interpret a string as a host:port pair.

    An IPv6 address MUST be escaped if accompanied by a port,
    because otherwise ambiguity ensues: 2001:db8:85a3::8a2e:370:7334
    means both [2001:db8:85a3::8a2e:370:7334] and
    [2001:db8:85a3::8a2e:370]:7334.

    >>> parse_host_port('server01:80')
    ('server01', 80)
    >>> parse_host_port('server01')
    ('server01', None)
    >>> parse_host_port('server01', default_port=1234)
    ('server01', 1234)
    >>> parse_host_port('[::1]:80')
    ('::1', 80)
    >>> parse_host_port('[::1]')
    ('::1', None)
    >>> parse_host_port('[::1]', default_port=1234)
    ('::1', 1234)
    >>> parse_host_port('2001:db8:85a3::8a2e:370:7334', default_port=1234)
    ('2001:db8:85a3::8a2e:370:7334', 1234)
    >>> parse_host_port(None)
    (None, None)
    """
    if not address:
        return (None, None)

    if address[0] == '[':
        # Escaped ipv6
        _host, _port = address[1:].split(']')
        host = _host
        if ':' in _port:
            port = _port.split(':')[1]
        else:
            port = default_port
    else:
        if address.count(':') == 1:
            host, port = address.split(':')
        else:
            # 0 means ipv4, >1 means ipv6.
            # We prohibit unescaped ipv6 addresses with port.
            host = address
            port = default_port

    return (host, None if port is None else int(port))

def get_ip_network(network, suppress_error=False):
    ''' return IPNetwork '''
    try:
        ip_network = netaddr.IPNetwork(network)
        return ip_network
    except Exception as e:
        if not suppress_error:
            print("invalid network [%s]: %s", network, e)
        return None


def is_ipv4_network(network: str):
    """
    判断是否是ipv4地址
    :param network:
    :return:
    """
    n = network
    if not isinstance(n, (IPNetwork, IPAddress)):
        n = get_ip_network(network)
    return getattr(n, "version", None) == 4


def is_ipv6_network(network: str):
    """
    判断是否是ipv6地址
    :param network:
    :return:
    """
    n = network
    if not isinstance(n, (IPNetwork, IPAddress)):
        n = get_ip_network(network)
    return getattr(n, "version", None) == 6

def is_valid_ipv4(address, strict=None):
    """Verify that address represents a valid IPv4 address.

    :param address: Value to verify
    :type address: string
    :param strict: flag allowing users to restrict validation
        to IP addresses in presentation format (``a.b.c.d``) as opposed to
        address format (``a.b.c.d``, ``a.b.c``, ``a.b``, ``a``).
    :type flags: bool
    :returns: bool

    .. versionadded:: 1.1
    .. versionchanged:: 4.8.0
       Allow to restrict validation to IP addresses in presentation format
       (``a.b.c.d``) as opposed to address format
       (``a.b.c.d``, ``a.b.c``, ``a.b``, ``a``).
    """
    if strict is not None:
        flag = INET_PTON if strict else 0
        try:
            return netaddr.valid_ipv4(address, flags=flag)
        except netaddr.AddrFormatError:
            return False

    # non strict mode
    try:
        if netaddr.valid_ipv4(address, flags=INET_PTON):
            return True
        else:
            if netaddr.valid_ipv4(address):
                logger.warning(
                    'Converting in non strict mode is deprecated. '
                    'You should pass strict=False if you want to '
                    'preserve legacy behavior')
                return True
            else:
                return False
    except netaddr.AddrFormatError:
        return False


def is_valid_ipv6(address):
    """Verify that address represents a valid IPv6 address.

    :param address: Value to verify
    :type address: string
    :returns: bool

    .. versionadded:: 1.1
    """
    if not address:
        return False

    parts = address.rsplit("%", 1)
    address = parts[0]
    scope = parts[1] if len(parts) > 1 else None
    if scope is not None and (len(scope) < 1 or len(scope) > 15):
        return False

    try:
        return netaddr.valid_ipv6(address, netaddr.core.INET_PTON)
    except netaddr.AddrFormatError:
        return False


def is_valid_cidr(address):
    """Verify that address represents a valid CIDR address.
    eg:
    192.168.1.120/24 -> True
    192.168.1.1200/24 -> False
    """
    try:
        # Validate the correct CIDR Address
        netaddr.IPNetwork(address)
    except (TypeError, netaddr.AddrFormatError):
        return False

    # Prior validation partially verify /xx part
    # Verify it here
    ip_segment = address.split('/')

    if (len(ip_segment) <= 1 or
            ip_segment[1] == ''):
        return False

    return True


def is_valid_ipv6_cidr(address):
    """Verify that address represents a valid IPv6 CIDR address.

    :param address: address to verify
    :type address: string
    :returns: true if address is valid, false otherwise

    .. versionadded:: 3.17
    """
    try:
        netaddr.IPNetwork(address, version=6).cidr
        return True
    except (TypeError, netaddr.AddrFormatError):
        return False


def get_network_version(network):
    """
    判断ip的版本
    :param network:
    :return: 4 or 6
    """
    n = get_ip_network(network)
    if not n:
        raise Exception("无效网络: [%s]" % network)
    return n.version


def get_ipv6_addr_by_EUI64(prefix, mac):
    """Calculate IPv6 address using EUI-64 specification.

    This method calculates the IPv6 address using the EUI-64
    addressing scheme as explained in rfc2373.

    :param prefix: IPv6 prefix.
    :param mac: IEEE 802 48-bit MAC address.
    :returns: IPv6 address on success.
    :raises ValueError, TypeError: For any invalid input.

    eg:
    prefix:'2001:db8::'
    mac:'00:01:02:03:04:05'
    ->2001:db8::201:2ff:fe03:405
    """
    # Check if the prefix is an IPv4 address
    if is_valid_ipv4(prefix):
        msg = "Unable to generate IP address by EUI64 for IPv4 prefix"
        raise ValueError(msg)
    try:
        eui64 = int(netaddr.EUI(mac).eui64())
        prefix = netaddr.IPNetwork(prefix)
        return netaddr.IPAddress(prefix.first + eui64 ^ (1 << 57))
    except (ValueError, netaddr.AddrFormatError):
        raise ValueError('error generating IP address')
    except TypeError:
        raise TypeError('error generating IP address')


def get_mac_addr_by_ipv6(ipv6, dialect=netaddr.mac_unix_expanded):
    """Extract MAC address from interface identifier based IPv6 address.

    For example from link-local addresses (fe80::/10) generated from MAC.

    :param ipv6: An interface identifier (i.e. mostly MAC) based IPv6
                 address as a netaddr.IPAddress() object.
    :param dialect: The netaddr dialect of the the object returned.
                    Defaults to netaddr.mac_unix_expanded.
    :returns: A MAC address as a netaddr.EUI() object.

    See also:
    * https://tools.ietf.org/html/rfc4291#appendix-A
    * https://tools.ietf.org/html/rfc4291#section-2.5.6

    .. versionadded:: 4.3.0
    """
    return netaddr.EUI(int(
        # out of the lowest 8 bytes (byte positions 8-1)
        # delete the middle 2 bytes (5-4, 0xff_fe)
        # by shifting the highest 3 bytes to the right by 2 bytes (8-6 -> 6-4)
        (((ipv6 & 0xff_ff_ff_00_00_00_00_00) >> 16) +
         # adding the lowest 3 bytes as they are (3-1)
         (ipv6 & 0xff_ff_ff)) ^
        # then invert the universal/local bit
        0x02_00_00_00_00_00),
        dialect=dialect)


def get_host_ip(hostname, suppress_warning=False, default=None):
    """
    获取主机IP地址
    :param hostname:
    :param suppress_warning:
    :param default:
    :return:
    """
    try:
        socket.setdefaulttimeout(3)
        ip = socket.gethostbyname(hostname)
    except Exception as e:
        logger.error(f"从{hostname}获取ip失败,原因:{str(e)}")
        return default if default else hostname
    return ip


def is_valid_ip(ip_addr):
    """
    检查IP地址是否有效
    :param ip_addr:
    :return:
    """
    try:
        netaddr.IPAddress(ip_addr, flags=1)
    except:
        return False
    return True


def is_valid_mac(address):
    """Verify the format of a MAC address.

    Check if a MAC address is valid and contains six octets. Accepts
    colon-separated format only.

    :param address: MAC address to be validated.
    :returns: True if valid. False if not.

    .. versionadded:: 3.17
    """
    m = "[0-9a-f]{2}(:[0-9a-f]{2}){5}$"
    return isinstance(address, str) and re.match(m, address.lower())


def _is_int_in_range(value, start, end):
    """Try to convert value to int and check if it lies within
    range 'start' to 'end'.

    :param value: value to verify
    :param start: start number of range
    :param end: end number of range
    :returns: bool
    """
    try:
        val = int(value)
    except (ValueError, TypeError):
        return False
    return (start <= val <= end)


def is_valid_port(port):
    """Verify that port represents a valid port number.

    Port can be valid integer having a value of 0 up to and
    including 65535.

    .. versionadded:: 1.1.1
    """
    return _is_int_in_range(port, 0, 65535)


def ip_version(ip):
    """
    获取IP版本
    :param ip: ipv4:12.12.1.1 or ipv6:fe80::6111:d4dd:b65d:1535
    :return: 4 or 6
    """
    return IP(ip).version()


def ip_type(ip):
    """
    获取IP类型
    :param ip:
    :return:PUBLIC \\ LINKLOCAL \\ PRIVATE
    """
    return IP(ip).iptype()


def get_ip_list(ip_segment):
    """
    获取指定网段的IP的清单信息
    :param ip: IP段，例如：10.0.0.0/28
    :return:
    """
    ip = IP(ip_segment)
    # ip的起始点
    ip_start = ip.net()
    # ip的子网掩码
    ip_mask = ip.netmask()
    # ip的广播地址
    ip_broadcast = ip.broadcast()
    return (ip_start, ip_mask, ip_broadcast)


def ip_con(ip):
    """
    IP地址的进制转换
    :param ip:
    :return:
    """
    ip = IP(ip)
    # 转二进制
    ip_int = ip.int()
    # 转十进制
    ip_bin = ip.strBin()
    # 转十六进制
    ip_hex = ip.strHex()
    return (ip_int, ip_bin, ip_hex)


def ip_len(ip_segment):
    """
    遍历获取一个网段的所有IP地址
    :param ip_segment:
    :return:
    """
    ip = IP(ip_segment)
    ip_list = []
    for i in ip:
        ip_list.append(str(i))
    print(f"网段:{ip_segment} 下IP数量共计:{len(ip_list)} 个")
    return ip_list


def is_ip_seg(ip, ip_segment):
    """
    判断一个IP地址是否在一个网段
    :param ip:
    :param ip_segment:
    :return: True or False
    """
    return ip in IP(ip_segment)


def get_private_ip_network(seq=1, vpc_network=None, excludes=None):
    ''' get valid ip network '''
    if excludes is None:
        excludes = []
    if vpc_network:
        network = IPNetwork(vpc_network)
        subnets = list(network.subnet(24))
        for exc in excludes:
            if IPNetwork(exc) in subnets:
                subnets.remove(IPNetwork(exc))
        network = subnets[seq % (len(subnets) - 2)]
        logger.info("network [%s]"%network)
        return str(network)


def get_ip_network_first_and_last_ip_addr(ip_network):
    """
    生成一个段的第一个IP地址和最后一个IP地址
    :param network: 172.20.0.0/24
    :return: (172.20.0.1,172.20.0.254)
    """
    subnet = ipaddress.ip_network(ip_network)
    first_ip = str(subnet.network_address + 1)
    last_ip = str(subnet.broadcast_address - 1)
    return (first_ip,last_ip)


def ip_in_network(ip, network):
    try:
        if isinstance(network, (list, tuple)):
            if len(network) == 2 and network[0].find("/") == -1:
                is_in = netaddr.IPAddress(ip) in netaddr.IPRange(network[0], network[1])
            else:
                is_in = False
                for _net in network:
                    if netaddr.IPAddress(ip) in \
                            netaddr.IPNetwork(_net):
                        is_in = True
                        break
        else:
            is_in = netaddr.IPAddress(ip) in netaddr.IPNetwork(network)
        if not is_in:
            return False
        return True
    except Exception as e:
        logger.error("invalid ip [%s] in network [%s]: %s", ip, network, e)
        return False


def get_my_ipv4():
    """Returns the actual ipv4 of the local machine.

    This code figures out what source address would be used if some traffic
    were to be sent out to some well known address on the Internet. In this
    case, IP from RFC5737 is used, but the specific address does not
    matter much. No traffic is actually sent.

    .. versionadded:: 1.1

    .. versionchanged:: 1.2.1
       Return ``'127.0.0.1'`` if there is no default interface.
    """
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('192.0.2.0', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return _get_my_ipv4_address()


def _get_my_ipv4_address():
    """Figure out the best ipv4
    """
    LOCALHOST = '127.0.0.1'
    gtw = netifaces.gateways()
    try:
        interface = gtw['default'][netifaces.AF_INET][1]
    except (KeyError, IndexError):
        logger.info('Could not determine default network interface, '
                 'using 127.0.0.1 for IPv4 address')
        return LOCALHOST

    try:
        return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    except (KeyError, IndexError):
        logger.info('Could not determine IPv4 address for interface %s, '
                 'using 127.0.0.1',
                 interface)
    except Exception as e:
        logger.info('Could not determine IPv4 address for '
                 'interface %(interface)s: %(error)s',
                 {'interface': interface, 'error': e})
    return LOCALHOST


def get_my_ipv6():
    """Returns the actual IPv6 address of the local machine.

    This code figures out what source address would be used if some traffic
    were to be sent out to some well known address on the Internet. In this
    case, IPv6 from RFC3849 is used, but the specific address does not
    matter much. No traffic is actually sent.

    .. versionadded:: 6.1
       Return ``'::1'`` if there is no default interface.
    """
    try:
        csock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        csock.connect(('2001:db8::1', 80))
        (addr, _, _, _) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return _get_my_ipv6_address()


def _get_my_ipv6_address():
    """Figure out the best IPv6 address
    """
    LOCALHOST = '::1'
    gtw = netifaces.gateways()
    try:
        interface = gtw['default'][netifaces.AF_INET6][1]
    except (KeyError, IndexError):
        logger.info('Could not determine default network interface, '
                 'using %s for IPv6 address', LOCALHOST)
        return LOCALHOST

    try:
        return netifaces.ifaddresses(interface)[netifaces.AF_INET6][0]['addr']
    except (KeyError, IndexError):
        logger.info('Could not determine IPv6 address for interface '
                 '%(interface)s, using %(address)s',
                 {'interface': interface, 'address': LOCALHOST})
    except Exception as e:
        logger.info('Could not determine IPv6 address for '
                 'interface %(interface)s: %(error)s',
                 {'interface': interface, 'error': e})
    return LOCALHOST


def pings(ips,max_workers=500):
    """
    ping 一个IP组成的列表并返回 ping的状态
    :param ips: IP列表,Example ["192.168.85.1","192.168.85.200"]
    :return: Dict, Example {'192.168.85.1': False, '192.168.85.200': True}
    """
    ips_status = dict()
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        results = pool.map(ping,ips)
    for index,result in enumerate(results):
        ip = ips[index]
        if type(result) == float:
            ips_status[ip] = True
        else:
            ips_status[ip] = False
    return ips_status


def verbose_ping(dest_addr: str, count: int = 4, interval: float = 0):
    """
    对目标地址执行连续ping并打印耗时
    :param dest_addr: 需要ping的IP或域名
    :param count: 执行ping的次数
    :param interval: 每次ping的间隔
    :return: example
        ping 'www.qingcloud.com' ... 125ms
        ping 'www.qingcloud.com' ... 136ms
        ping 'www.qingcloud.com' ... 92ms
        ping 'www.qingcloud.com' ... 78ms
    """
    return ping_verbose(dest_addr, count, interval)
