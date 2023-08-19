# -*coding:utf-8 -*-
# !/usr/bin/env python

from PIL import ImageFile
from PIL import Image
import os


class command:
    def __init__(self):
        super().__init__()

    def devices(self, device):
        if device is not None:
            s = '-s ' + device
            # print(s)
        else:
            s = ''
        return s

    def dev(self):
        # 查看当前链接设备
        com = os.popen('adb devices').read()
        return com

    #
    def state(self, device=None):
        # 返回连接状态
        s = self.devices(device)
        com = os.popen('adb {} get-state'.format(s)).read()
        return com

    #
    def connect(self, ip):
        # 连接ip+端口号
        com = os.popen('adb connect {}'.format(ip)).read()
        return com

    #
    def insert(self, text, device=None):
        s = self.devices(device)
        com = os.system('adb {} shell input text {}'.format(s, text))  # 输入文本
        return com

    def log(self, device=None):
        # 查看日志
        s = self.devices(device)
        com = os.popen('adb {} logcat').read()
        return com

    def kill(self):
        # 结束adb服务
        com = os.system('adb kill-server')
        return com

    def star(self):
        # 开始adb服务
        com = os.system('adb start-server')
        return com

    def install(self, apk_name, device=None):
        # 安装软件
        s = self.devices(device)
        com = os.system('adb {} install -r {}.apk'.format(s, apk_name))
        return com

    def uninstall(self, apk_name, device=None):
        # 卸载
        s = self.devices(device)
        com = os.system('adb {} uninstall {}.apk'.format(s, apk_name))
        return com

    def update(self, file_name, path_phone, device=None):
        # 上传SDCard/../..手机端路径
        s = self.devices(device)
        com = os.system('adb {} push {} {}'.format(s, file_name, path_phone))
        return com

    def download(self, file_name, device=None):
        # 下载
        s = self.devices(device)
        com = os.system('adb {} uninstall {}'.format(s, file_name))
        return com

    def scr(self, path_pic_name, device=None):
        # 屏幕截图到手机根目录
        s = self.devices(device)
        com = os.system('adb {} shell screencap -p /sdcard/{}.png'.format(s, path_pic_name))
        return com

    def video_scr(self, video_name, device=None):
        # 录屏，默认mp4格式
        s = self.devices(device)
        com = os.system('adb {} shell screenrecord /sdcard/{}.mp4'.format(s, video_name))
        return com

    def cut_scr(self, fol_path, device=None):
        # 屏幕截图到本地
        # pic_name:屏幕截图生成地址+名称，默认为手机的根目录,默认的来
        # path为文件夹目录下
        s = self.devices(device)
        fpath = fol_path.split('\\')[-1].split('/')[-1].split('.')[0]
        self.scr(fpath)
        com = os.system("adb {} pull /sdcard/{}.png {}".format(s, fpath, fol_path))
        # os.system("adb shell rm /sdcard/{}.png".format(fpath))
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        return com

    def spec_scr(self, pic_path, int_x1, int_y1, int_x2, int_y2):
        """
        指定截图保存
        左上角的点到右下角的点
        """
        self.cut_scr(pic_path)
        img = Image.open(pic_path)
        # (4)将图片验证码截取
        code_image = img.crop((int_x1, int_y1, int_x2, int_y2))
        code_image.save(pic_path)  # 原地址重写
        return True

    def tap_work(self, x, y, device=None):
        """
        模拟点击操作
        """
        s = self.devices(device)
        com = os.system('adb {} shell input tap {} {}'.format(s, x, y))
        return com

    def swip_work(self, x, y, x2, y2, device=None):
        """
        模拟滑动操作
        """
        s = self.devices(device)
        com = os.system('adb {} shell input swipe {} {} {} {}'.format(s, x, y, x2, y2))
        return com

    def get_ui(self, path, device=None):
        s = self.devices(device)
        os.popen('adb {} shell uiautomator dump /sdcard/ui.xml'.format(s))  # 获得屏幕控件信息
        re = os.popen(r'adb {} pull /sdcard/ui.xml {}+ui.xml'.format(s, path))  # 获得屏幕控件信息
        return re
