import platform
import sys
import os
import time
import threading

live_ip = 0


def get_os():
    os = platform.system()
    if os == "Windows":
        return "n"
    else:
        return "c"


def ping_ip(ip_str):
    cmd = ["ping", "-{op}".format(op=get_os()),
           "1", ip_str]
    output = os.popen(" ".join(cmd)).readlines()
    for line in output:
        if str(line).upper().find("TTL") >= 0:
            print("ip: %s is ok ***" % ip_str)
            global live_ip
            live_ip += 1
            break


def find_ip(ip_prefix):
    """''
    给出当前的127.0.0 ，然后扫描整个段所有地址
    """
    threads = []
    for i in range(1, 256):
        ip = '%s.%s' % (ip_prefix, i)
        threads.append(threading.Thread(target=ping_ip, args={ip, }))
    for i in threads:
        i.start()
    for i in threads:
        i.join()


def getgetget(cmd_args):
    print("start time %s" % time.ctime())
    # cmd_args = sys.argv[1:]
    args = "".join(cmd_args)
    ip_pre = '.'.join(args.split('.')[:-1])
    find_ip(ip_pre)
    print("end time %s" % time.ctime())
    print('本次扫描共检测到本网络存在%s台设备' % live_ip)


getgetget('10.147.18.1/24')
