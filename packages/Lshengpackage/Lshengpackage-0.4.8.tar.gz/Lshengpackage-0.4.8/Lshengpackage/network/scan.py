# -*- coding: utf-8 -*-
import os
import re
import socket
import threading
import time
from collections import defaultdict

ip_Mac = defaultdict(list)


# 获取指定IP地址的MAC地址
def getMac(target_IP):
    # 初始化 用正则表达式're'编译出匹配MAC地址的正则表达式对象
    patt_mac = re.compile('([a-f0-9]{2}[-:]){5}[a-f0-9]{2}', re.I)
    # ping
    os.popen('ping -n 1 -w 500 {} > nul'.format(target_IP))
    # 然后使用'arp'命令获取该IP地址对应的MAC地址 返回一个类文件对象 可以通过 read 方法获取命令的输出结果
    arp_file = os.popen('arp -a {}'.format(target_IP))
    # 使用正则表达式'self.patt_mac'在输出结果中查找符合 MAC 地址格式的字符串 并返回找到的第一个匹配项 即 IP 对应的 MAC 地址
    mac_addr = patt_mac.search(arp_file.read())

    # 根据正则表达式对象匹配MAC地址 如果匹配到了就返回MAC地址 否则返回None
    if mac_addr:
        mac_addr = mac_addr.group()
        ip_Mac[target_IP].append(mac_addr)
        return mac_addr
    else:
        # print(target_IP)
        return '00-00-00-00-00-00'


def threadsMac(gate_way, ip_addr, _mix, _max):
    threads = []
    for i in range(_mix, _max):
        target_IP = gate_way + str(i)
        if target_IP != ip_addr:
            threads.append(threading.Thread(target=getMac, args={target_IP, }))
        else:
            threads.append(threading.Thread(target=getMac, args={target_IP, }))

    for i in threads:
        i.start()
    for i in threads:
        i.join()


def common_LAN_WAN(gate_way, ip_addr, _mix, _max):
    threadsMac(gate_way, ip_addr, _mix, _max)
    # 打印方法
    for i in ip_Mac:
        print(i + ':[' + ip_Mac[i][0] + ']')
    print("end time %s" % time.ctime())
    print('本次扫描共检测到本网络存在%s台设备' % len(ip_Mac))


# 获取与本机在同一局域网下的设备 IP与MAC的映射(多线程)除本机
def getLANIpMac(_mix=0, _max=255):
    ip_Mac.clear()
    """
    # 返回默认网卡对应的IP地址
    ip_addr = socket.gethostbyname(socket.gethostname())
    """
    # 创建一个UDP套接字
    sockets = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 连接到一个公共ip地址
    sockets.connect(('www.baidu.com', 80))
    # 获取本地套接字的地址信息 这个地址信息就是本机在局域网中的IP地址
    ip_addr = sockets.getsockname()[0]
    # 关闭套接字
    sockets.close()
    print("start time %s" % time.ctime())
    print("当前本机局域网ip地址为:" + ip_addr)
    # 获取网关
    idx = 0
    cnt = 0
    for i in ip_addr:
        idx = idx + 1
        if i == '.':
            cnt = cnt + 1
            if cnt == 3:
                break
    gate_way = ip_addr[0:idx]
    common_LAN_WAN(gate_way, ip_addr, _mix, _max)
    return ip_Mac


# 获取内网可达的设备 IP与MAC的映射(多线程)除本机
def getWANIpMac(cmd_args, _mix=0, _max=255):
    ip_Mac.clear()
    print("start time %s" % time.ctime())
    # cmd_args = sys.argv[1:]
    args = "".join(cmd_args)
    gate_way = '.'.join(args.split('.')[:-1]) + '.'

    ip_addr = '0'
    common_LAN_WAN(gate_way, ip_addr, _mix, _max)


# while True:
#     x = input('请输入要扫描的ip地址段:')
#     try:
#         if len(x) == 0:
#             getLANIpMac()
#         else:
#             getWANIpMac(x)
#     except OSError as reason:
#         print('格式错误，请重新输入')
#         print('错误原因，reason')
#     input()


