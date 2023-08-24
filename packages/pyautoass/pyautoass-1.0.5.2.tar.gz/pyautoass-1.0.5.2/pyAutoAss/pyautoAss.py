"""
    name: pyautoAss
    author: awiseking
    version: 1.0.5.2
    des: 基于键鼠、图片定位的自动化gui工作套件。
        
"""
import cv2 as cv
from .utils.Utils import *
from .pyclipboard import PyClipboard
from .pyAutoKeyboard import PyAutoKeyboard
from .pyAutoMouse import PyAutoMouse
from .pyAutoGui import PyAutoGui

__version__ = "1.0.5.2"

class AutoOperation(PyAutoKeyboard,PyAutoMouse,PyAutoGui):

    def __init__(self,app_name:str="app") -> None:
        """自动化套件
        初始化自动化套件所需组件，自动进行数据处理等工作。
        :param app_name -- 应用名

        :var self.app_name -- 应用名
        :var self.pclip -- 剪贴板控件

        :return: None
        """
        super().__init__()

        self.app_name = app_name
        self.pclip = PyClipboard()
    
    # 暂停
    def wait(self):
        """暂停
        在当前位置停下

        Keyword arguments:
        Return: None
        """
        
        ...

    # 获取图片所在坐标
    def getXY(self, img_path:str="./input/pic/template.png",screenshot_img_path="./input/pic/screenshot.png"):
        """
        图片中心在屏幕坐标
        :param img_path: 图片路径
        :return avg: 图片中心在屏幕坐标
        """
        self.screenShotSaveFile(screenshot_img_path)

        screenshot_img = cv.imread(screenshot_img_path)
        template_img = cv.imread(img_path)

        # 获取图片宽高
        height, width, channel = template_img.shape

        # 使用matchTemplate进行模板匹配（标准平方差匹配）
        result = cv.matchTemplate(
            screenshot_img, template_img, cv.TM_SQDIFF_NORMED)
        # 解析出匹配区域的左上角图标
        upper_left = cv.minMaxLoc(result)[2]
        # 计算出匹配区域右下角图标（左上角坐标加上模板的长宽即可得到）
        lower_right = (upper_left[0] + width, upper_left[1] + height)
        # 计算坐标的平均值并将其返回
        avg = (int((upper_left[0] + lower_right[0]) / 2),
               int((upper_left[1] + lower_right[1]) / 2))
        return avg

    # 识别图片左击
    def autoORCLeftClick(self, img_path):
        """
        识别图片后进行左击单击
        :param img_path: 图片路径
        :return: None
        """
        xy = self.getXY(img_path)
        self.moveClick(*xy)

    # 识别图片右击
    def autoORCRightClick(self, img_path):
        """
        识别图片后进行右击单击
        :param img_path: 图片路径
        :return: None
        """
        xy = self.getXY(img_path)
        self.moveClick(*xy,about="right")

    # 记录当前数据
    def recordData(self):
        self.record_data = self.paste()

    #  取出当前记录数据
    def getRecordData(self):
        self.pclip.copy(self.record_data)

    # 记录当前备注
    def recordNote(self):
        self.note = self.paste()

    #  取出当前记录备注
    def getRecordNote(self):
        self.pclip.copy(self.note)