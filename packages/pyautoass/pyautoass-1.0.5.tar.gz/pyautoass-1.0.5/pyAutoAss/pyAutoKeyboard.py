import win32con,win32api
from time import sleep
from .utils.VKCODE import vk_code as VKC

class PyAutoKeyboard:

        # 转换按键为按键码
    def VK_CODE(self,char:str):
        """转换按键为按键码
        
        Keyword arguments:
        char -- 按键值
        Return: 按键码
        """
        char = str(char).lower()
            
        char_dict = VKC
        return char_dict[char]

    # 暂停
    def wait(self):
        """暂停
        在当前位置停下

        Keyword arguments:
        Return: None
        """
        
        ...

    # 键盘按下
    def keyDown(self,*chars):
        """键盘按下
        
        Keyword arguments:
        chars -- 按键值
        Return: None
        """
        for char in chars:
            win32api.keybd_event(self.VK_CODE(char),0,0,0)

    # 键盘松开
    def keyUp(self,*chars):
        """键盘松开
        
        Keyword arguments:
        chars -- 按键值
        Return: None
        """
        for char in chars:
            win32api.keybd_event(self.VK_CODE(char),win32con.KEYEVENTF_KEYUP,0,0)

    # 键盘输入
    def keyInput(self,strings):
        """键盘输入
        
        Keyword arguments:
        strings -- 字符串
        Return: None
        """

        for char in strings:
            self.keyDown(char)

    # 粘贴
    def kPaste(self):
        self.keyDown("ctrl","v")
        sleep(0.2)

    # 全选
    def kSelecAll(self):
        
        self.keyDown("ctrl","a")
        sleep(0.2)

    # 删除
    def kDel(self):
        
        self.keyDown("del")
        sleep(0.2)

    # 回车
    def kEnter(self):
        
        self.keyDown("enter")
        sleep(0.2)
