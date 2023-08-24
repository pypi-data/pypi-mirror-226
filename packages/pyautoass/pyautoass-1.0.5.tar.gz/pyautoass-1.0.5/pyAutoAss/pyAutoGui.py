import win32gui,win32api,win32con,win32ui,win32clipboard
import cv2

class PyAutoGui:
    def __init__(self):
        ...

    # 截屏并保存到文件
    def screenShotSaveFile(self,file_path:str="./screenshot.png"):
        """截屏
        :param file_path -- 截图保存位置

        :var hdesktop -- 虚拟桌面
        :var hd_width -- 虚拟屏幕宽度
        :var hd_height -- 虚拟屏幕高度
        :var desktop_dc -- 设备描述表
        :var img_dc -- 设备描述表
        :var mem_dc -- 创建内存描述表
        :var screentshot -- 位图对象

        :return: None
        """
        # 获取桌面
        hdesktop = win32gui.GetDesktopWindow()
        # 获取屏幕参数
        hd_width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        hd_height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        # 创建设备描述表
        desktop_dc = win32gui.GetWindowDC(hdesktop)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)
        # 创建内存设备描述表
        mem_dc = img_dc.CreateCompatibleDC()
        # 创建位图
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(img_dc,hd_width,hd_height)
        mem_dc.SelectObject(screenshot)
        # 截图保存到内存设备描述表
        mem_dc.BitBlt((0,0),(hd_width,hd_height),img_dc,(0,0),win32con.SRCCOPY)
        # 保存位图到文件
        screenshot.SaveBitmapFile(mem_dc,file_path)
        # 释放内存
        mem_dc.DeleteDC()
        win32gui.DeleteObject(screenshot.GetHandle())