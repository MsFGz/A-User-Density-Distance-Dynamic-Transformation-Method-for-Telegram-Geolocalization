# coding = utf-8
import logging
import re
import time
from typing import Tuple

from appium import webdriver
from appium.webdriver.webelement import WebElement
from appium.webdriver.common.appiumby import AppiumBy as Aby
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

import Utility as Util
from FusedLocal import BSInfo, Coord


class App:
    """
        App Option Module
    """

    def __init__(self, app_name: str, device_name: str = "be47afa6", host: str = Util.TARGET_HOST, port: int = 4723) -> None:
        """Init Webdriver with appname (and device name)

            Args::
                app_name: Application name, str, like "org.lsposed.manager"

                device_name: Device name str, default = "be47afa6"

                host: target host ip, str, default = "http://127.0.0.1"

                port: app controllor port, int, default = 4723
            Usage::
                app = App(app_name) or app = App(app_name, device_name)
                ...
        """
        global INIT_PORT
        self.app_name = app_name
        self.app_package, self.app_activity = self.getAppInfo(app_name)
        desired_caps = {
            'platformName': 'Android',
            'deviceName': device_name,
            'appPackage': self.app_package,
            'appActivity': self.app_activity,
            'udid': device_name,
            'mockLocationApp': 'null',
            'noReset': True
        }
        self.driver = webdriver.Remote(f"{host}:{port}/wd/hub", desired_caps)

    @staticmethod
    def getAppInfo(app_name: str) -> tuple:
        """Gets app package and activity with name.

            Usage::
                getInfo(app_name)
            Return::
                (app_package, app_activity)
        """
        return Util.APP_INFO[app_name]

    def getSize(self) -> tuple:
        """Gets the width and height of the current window.

            Usage::
                app.getSize()
            Return::
                (width, height)
        """
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)

    def swipeUp(self, t: int = 500) -> None:
        """Swipe up, for an optional duration.

            Args::
                t: time to take the swipe in ms, default is 500, int.
            Usage::
                device.swipeUp(1000)
        """
        l = self.getSize()
        x1 = int(l[0] * 0.5)  # x坐标
        y1 = int(l[1] * 0.5)  # 起始y坐标
        y2 = int(l[1] * 0.75)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    def swipeDown(self, t: int = 500) -> None:
        """Swipe down, for an optional duration.

            Args::
                t: time to take the swipe in ms, default is 500, int.
            Usage::
                device.swipeDown(1000)
        """
        l = self.getSize()
        x1 = int(l[0] * 0.5)  # x坐标
        y1 = int(l[1] * 0.75)  # 起始y坐标
        y2 = int(l[1] * 0.75 - 450)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    def swipLeft(self, t: int = 500) -> None:
        """Swipe left, for an optional duration.

            Args::
                t: time to take the swipe in ms, default is 500, int.
            Usage::
                device.swipeLeft(1000)
        """
        l = self.getSize()
        x1 = int(l[0] * 0.05)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.75)
        self.driver.swipe(x1, y1, x2, y1, t)

    def swipRight(self, t: int = 500) -> None:
        """Swipe right, for an optional duration.

            Args::
                t: time to take the swipe in ms, default is 500, int.
            Usage::
                device.swipeRight(1000)
        """
        l = self.getSize()
        x1 = int(l[0] * 0.75)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.05)
        self.driver.swipe(x1, y1, x2, y1, t)

    def getElement(self, type: str, name: str) -> WebElement:
        """Get element by name with type.

            Args::
                type: AppiumBy, str.
                name: Element name, str
            Usage::
                element = app.getElement(AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text('NearBy')")
            Return:: 
                WebElement
        """
        return self.driver.find_element(type, name)

    def getElements(self, type: str, name: str) -> list:
        """Get elements by name with type.

            Args::
                type: AppiumBy, str.
                name: Element name, str
            Usage::
                list = app.getElements(AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text('NearBy')")
            Return:: 
                List of WebElement
        """
        return self.driver.find_elements(type, name)

    def getContent(self, type: str, name: str) -> str:
        """Get element text by name with type.

            Args::
                type: AppiumBy, str.
                name: Element name, str
            Usage::
                app.getContent(AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text('NearBy')")
            Return:: 
                Content text as str
        """
        return self.getElement(type, name).text

    def getContentFromItem(self, type: str, name: str, item: WebElement) -> str:
        return item.find_element(type, name).text

    def getState(self, type: str, name: str) -> bool:
        """Get switch state by name with type.

            Args::
                type: AppiumBy, str.
                name: Element name, str
            Usage::
                app.getState(AppiumBy.CLASSNAME, "android.widget.Switch")
            Return:: 
                True or False (Checked or Not Checked)
        """
        return self.driver.find_element(type, name).get_attribute('checked') == 'true'

    def input(self, type: str, name: str, content) -> None:
        """Input content to EditText

            Args::
                type: AppiumBy, str

                name: Element name, str

                content: Something will be inputed

            Usage::
                app.input(AppiumBy.ID, "com.silversliver.fakelocation.debug:id/value_tac", 4122)

        """
        edit_text = self.getElement(type, name)
        edit_text.clear()
        edit_text.send_keys(str(content))

    def click(self, type: str, name: str, wait_time: int = 5) -> None:
        """Click element by name with type.

            Args::
                type: AppiumBy, str
                name: Element name, str
            Usage::
                app.click(AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text('NearBy')")
        """
        try:
            self.elementWait(type, name, wait_time)
            self.getElement(type, name).click()
        except:
            pass
        finally:
            time.sleep(2)

    def back(self) -> None:
        """Goes one step backward in the browser history.

            Usage::
                app.back()
        """
        self.driver.back()
        self.implicitlyWait(5)

    def closeApp(self) -> None:
        """Stop the running application, specified in the desired capabilities, on
        the device.

            Usage::
                app.closeApp()
        """
        self.driver.close_app()

    def launchApp(self) -> None:
        """Start on the device the application specified in the desired capabilities.

            Usage::
                app.launchApp()
        """
        self.driver.launch_app()

    def elementWait(self, type: str, name: str, time: int = 20) -> None:
        """Wait element until appear.

            Args::
                type: AppiumBy, str
                name: Element name, str
            Usage::
                app.click(AppiumBy.ANDROID_UIAUTOMATOR, Util.WECHAT_DISCOVER)
        """
        WebDriverWait(self.driver, time, 3).until(
            lambda x: self.getElements(type, name))

    def implicitlyWait(self, time: int = 10) -> None:
        """Start on the device the application specified in the desired capabilities.

            Args::
                t: time (s), int, default is 10
            Usage::
                app.implicitlyWait(11)
        """
        self.driver.implicitly_wait(time)

    def exit(self) -> None:
        """End webdriver lifecircle

            Usage::
                app.exit()
        """
        self.driver.quit()


class TelegramControl:
    '''
        Telegram App Control Module
    '''

    def __init__(self, target_name: str, device_name: str = Util.EMU_DEVICE, host: str = Util.TARGET_HOST, port: int = 4723) -> None:
        '''Init control stream

            Args::
                target_name: geolocation target name, str

                device_name: name of controlled device, str, default = "127.0.0.1"

                host: target host ip, str, default = "http://127.0.0.1"

                port1: main app controllor port, int, default = 62001

            Usage::
                ctrl = Control(target_name)
                or
                ctrl = Control(target_name, device_name)
            ...
        '''
        self.target_name = target_name
        self.device_name = device_name
        self.host = host
        self.port = port
        self.telegram = App(Util.TELEGRAM, self.device_name, self.host, self.port)

    def clearPosition(self) -> None:  #清除位置
        '''Clear the position and exit

            Usage::
                ctrl.clearPosition()
        '''
        self.telegram.click(Aby.XPATH, Util.TELEGRAM_STOPSM) 
        self.telegram.click(Aby.ACCESSIBILITY_ID, Util.TELEGRAM_GOBACK)

    def getNearByList(self) -> list:  #获得附近的人列表
        '''Return list of Current display NearBy list

            Usage::
                ctrl.getNearByList()

            Return::
                list of WebElement
        '''
        return self.telegram.getElements(Aby.XPATH, Util.TELEGRAM_NEARBY_LIST) #附近的人列表

    def goNearByPage(self) -> None: #进行一系列的操作然后到附近的人界面（点击的按键需要修改）
        '''Click a series of buttons to go to a list of nearby people

            Usage::
                ctrl.goNearByList()
        '''
        self.telegram.click(Aby.ACCESSIBILITY_ID, Util.TELEGRAM_NAVIGATION_MENU)
        self.telegram.click(Aby.XPATH, Util.TELEGRAM_PEOPLE_NEARBY)
        '''
        try:
            self.telegram.click(Aby.ANDROID_UIAUTOMATOR, Util.WECHAT_START_CHECK) #改
        except:
            pass
        '''
        self.telegram.elementWait(Aby.XPATH, Util.TELEGRAM_NEARBY_LIST) #等几秒再获取people nearby list

    def pickupDistance(self) -> float: #获取探针与目标用户之间的距离
        """Get current report distance between probe and target

            Usage::
                ctrl.pickupDistance()

            Return
        """
        self.find_element(Aby.ACCESSIBILITY_ID, Util.TELEGRAM_NAVIGATION_MENU).click()
        self.implicitly_wait(6)
        self.find_element(Aby.XPATH, Util.TELEGRAM_PEOPLE_NEARBY).click()
        self.implicitly_wait(6)
        self.find_element(Aby.XPATH, Util.TELEGRAM_SHOWMORE).click() #应该判断是否有
        dis = -1
        state = True
        # 定义两个空列表用于存储符合条件的元素文本
        distance = []
        name = []
        # 定义一个标志变量用于判断是否提取到指定元素
        flag = False
        # 创建一个空集合，用于存储已读取过的用户名，避免重复读取
        seen_names = set()
        # 获取当前屏幕大小
        size = self.get_window_size()
        width = size['width']
        height = size['height']
        # 循环滚动并提取元素文本，直到提取到指定元素或者滚动到底部
        while not flag:
            # 获取当前屏幕上所有的FrameLayout元素
            frames = self.find_elements(Aby.XPATH, Util.TELEGRAM_NEARBY_LIST)
            #print(frames[0].find_element(Aby.CSS_SELECTOR,'.android.widget.TextView:nth-child(2)').text) 获取指定列表中的元素下的元素
            
            # 遍历每个FrameLayout元素
            for frame in frames:
                # 尝试获取该FrameLayout下的第一个TextView和第二个TextView元素
                try:
                    text1 = frame.find_element(Aby.CSS_SELECTOR,'.android.widget.TextView:nth-child(1)')
                    text2 = frame.find_element(Aby.CSS_SELECTOR,'.android.widget.TextView:nth-child(2)')
                except:
                    # 如果没有找到，则跳过该FrameLayout元素
                    continue
                
                # 获取两个TextView元素的文本内容
                text1_value = text1.text
                
                text2_value = text2.text
                
                
                # 判断第二个TextView的文本是否包含'away'字符串
                if 'away' in text2_value:
                    
                    
                    # 判断第二个TextView的文本是否同时包含'away'和'members'字符串，如果是，则说明已经提取到指定元素，将标志变量设为True，并跳出循环
                    if 'members' in text2_value:
                        flag = True
                        break
                # 如果包含，则将其添加到distance列表中，并将第一个TextView的文本添加到name列表中
                    if text1_value not in seen_names:  # 如果name不在seen_names集合中，则继续执行以下代码，否则跳过该元素
                        seen_names.add(text1_value)  # 将name添加到seen_names集合中，避免重复读取
                        distance.append(text2_value)
                        name.append(text1_value)

            # 如果还没有提取到指定元素，则继续滚动屏幕，从下往上滑动（假设屏幕大小是1080*1920）
            if not flag:
                # 定义滚动起点和终点的坐标（以屏幕中心为基准）
                start_x = width / 2
                start_y = height * 0.95
                end_x = start_x
                end_y = height * 0.17
                self.swipe(start_x, start_y, end_x, end_y, 1000)
        if self.target_name in name:
            i = name.index(self.target_name)
            dis_num = distance[i]
            unit_state = dis_num.find(Util.UNIT_KM) != -1
            unit = (dis_num.find(Util.UNIT_KM), 1000) if unit_state \
                else (dis_num.find(Util.UNIT_M), 1)
            dis_num = float(dis_num[0:unit[0]]) * unit[1]
            dis = dis_num
        else: dis = 0
            
        return dis


        
    

    # def pickupDistance(self) -> float: #获取探针与目标用户之间的距离
    #     """Get current report distance between probe and target

    #         Usage::
    #             ctrl.pickupDistance()

    #         Return
    #     """
    #     dis = -1
    #     state = True
    #     self.telegram.implicitlyWait(10)
    #     self.telegram.click(Aby.XPATH, Util.TELEGRAM_SHOWMORE)
    #     while state:
    #         near_by = self.getNearByList() #是NearByList
    #         if len(near_by) < 8: 
    #             continue
    #         for item in near_by:
    #             # Try catch to avoid exceptions
    #             try:
    #                 name = self.telegram.getContentFromItem(
    #                     Aby.ID, Util.TELEGRAM_USERNAME1, item)
    #                 # User's distance from us
    #                 dis_txt = self.telegram.getContentFromItem(
    #                     Aby.ID, Util.TELEGRAM_DISTANCE1, item)
    #                 unit_state = dis_txt.find(Util.UNIT_KMC) != -1
    #                 unit = (dis_txt.find(Util.UNIT_KMC), 1000) if unit_state \
    #                     else (dis_txt.find(Util.UNIT_MC), 1)
    #                 dis_num = float(dis_txt[0:unit[0]]) * unit[1]
    #                 if name == self.target_name or dis_num >= 3000:
    #                     state = not name == self.target_name
    #                     dis = dis_num if name == self.target_name else 0
    #                     break
    #             except:
    #                 pass
    #         self.wechat.swipeDown()
    #     return dis



    def refreshLocal(self) -> None:
        """Refresh Location by reopen page

            Usage::
                ctrl.refreshLocal()
        """
        self.telegram.back()
        self.goNearByPage()

    def refreshLocal(self) -> None:
        """Refresh Location by reload

            Usage::
                ctrl.refreshLocal()
        """
        tantan = App(Util.TANTAN, self.device_name, self.host, self.port)
        tantan.implicitlyWait(10)
        try:
            tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.TANTAN_SWIPETOCHECK)
        except NoSuchElementException:
            pass
        try:
            tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.TANTAN_CANCEL)
        except NoSuchElementException:
            pass
        tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.TANTAN_MY)
        tantan.click(Aby.ID, Util.TANTAN_SETTING)
        tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.TANTAN_LOCAL)
        tantan.implicitlyWait(5)
        tantan.exit()

    # def changeModuleState(self, state: bool) -> None: 不需要此函数
    #     """Enable or Disable Module

    #         Args:
    #             state: bool, true means checked
    #         Usage::
    #             ctrl.changeModuleState(True)
    #     """
    #     lsp = App(Util.LSP, self.device_name,
    #               self.host, self.port)
    #     lsp.implicitlyWait(10)
    #     lsp.click(Aby.ANDROID_UIAUTOMATOR, Util.LSP_MODULE)
    #     lsp.click(Aby.ANDROID_UIAUTOMATOR, Util.LSP_MODULE_NAME)
    #     cur_state = lsp.getState(Aby.CLASS_NAME, Util.SWITCH)
    #     if not(state and cur_state):
    #         lsp.click(Aby.CLASS_NAME, Util.SWITCH)
    #     lsp.exit()

    def changeLocation(self, latlon) -> None: #改过
            """Change Current app location

             Args::
                    coord: Coord, Coordinate of GPS
                Usage::
                    ctrl.changeModuleState(True)
            """
            self.implicitly_wait(10)
            self.back()
            self.implicitly_wait(10)
            self.back()
            self.find_element(Aby.ACCESSIBILITY_ID, value="Fake GPS").click()
            self.find_element(Aby.ACCESSIBILITY_ID, Util.FAKEGPS_NAVIGATION_DRAWER).click()
            self.find_element(Aby.XPATH, Util.FAKEGPS_GOTO).click()
            self.implicitly_wait(10)
            edit_text = self.find_element(Aby.XPATH, Util.FAKEGPS_LATLON)
            edit_text.clear()
            print(latlon)
            edit_text.send_keys(latlon)
            #self.input(Aby.ANDROID_UIAUTOMATOR, Util.FAKEGPS_LATLON)  #格式：(纬度,经度)
            self.find_element(Aby.ANDROID_UIAUTOMATOR, Util.FAKEGPS_OK).click()
            self.find_element(Aby.ID, Util.FAKEGPS_START).click()
            el2 = self.find_element(Aby.ACCESSIBILITY_ID, value="Telegram")
            el2.click()



    '''
    def changeLocation(self, bsInfo: BSInfo, coord: Coord) -> None: #改过
        """Change Current app location

            Args::
                bsInfo: BSInfo, Storage BS infos
                coord: Coord, Coordinate of GPS
            Usage::
                ctrl.changeModuleState(True)
        """
        self.back()
        el1 = self.find_element(Aby.ACCESSIBILITY_ID, value="Fake GPS")
        el1.click()
        fg = App(Util.FAKEGPS, self.device_name, self.host, self.port)
        fg.find_element(Aby.ACCESSIBILITY_ID, Util.FAKEGPS_NAVIGATION_DRAWER).click()
        fg.find_element(Aby.XPATH, Util.FAKEGPS_GOTO).click()
        fg.implicitly_wait(10)
        edit_text = fg.find_element(Aby.ANDROID_UIAUTOMATOR, Util.FAKEGPS_LATLON)
        edit_text.clear()
        edit_text.send_keys(Coord)
        #fg.input(Aby.ANDROID_UIAUTOMATOR, Util.FAKEGPS_LATLON)  #格式：(纬度,经度)
        fg.find_element(Aby.ANDROID_UIAUTOMATOR, Util.FAKEGPS_OK).click()
        fg.find_element(Aby.ID, Util.FAKEGPS_START).click()
        el2 = fg.find_element(Aby.ACCESSIBILITY_ID, value="Telegram")
        el2.click()
        '''
        # fg = App(Util.FAKEGPS, self.device_name,
        #          self.host, self.port)
        # fg.implicitlyWait(10)
        # fg.click(Aby.ANDROID_UIAUTOMATOR, Util.text(
        #     Util.APP_INFO[Util.FAKEGPS][0]))
        # fg.click(Aby.ACCESSIBILITY_ID, Util.FAKEGPS_NAVIGATION_DRAWER)
        # fg.click(Aby.ID, Util.FAKEGPS_GOTO)
        # fg.input(Aby.ANDROID_UIAUTOMATOR, Util.FAKEGPS_LATLON)  #格式：(纬度,经度)
        # fg.click(Aby.ANDROID_UIAUTOMATOR, Util.FAKEGPS_OK)
        # fg.click(Aby.ID, Util.FAKEGPS_START)
        # fg.exit()

    '''
        修改前的代码
        fl.click(Aby.ANDROID_UIAUTOMATOR, Util.FAKELOCAL_CHANGE)
        fl.input(Aby.ID, Util.FAKELOCAL_TAC, bsInfo.tac)
        fl.input(Aby.ID, Util.FAKELOCAL_CI, bsInfo.ci)
        fl.input(Aby.ID, Util.FAKELOCAL_PCI, bsInfo.pci)
        fl.input(Aby.ID, Util.FAKELOCAL_MCC, bsInfo.mcc)
        fl.input(Aby.ID, Util.FAKELOCAL_MNC, bsInfo.mnc)
        fl.input(Aby.ID, Util.FAKELOCAL_LON, coord.lon)
        fl.input(Aby.ID, Util.FAKELOCAL_LAT, coord.lat)
        fl.click(Aby.ID, Util.FAKELOCAL_SAVE)
        fl.exit()
        '''
    
    def closeApp(self) -> None:
        '''Close App and Appium Session

            Usage::
                ctrl.closeApp()
        '''
        self.telegram.exit()




# class TantanControl:
#     '''
#         Tantan App Control Module
#     '''

#     def __init__(self, target_name: str, device_name: str = "be47afa6", host: str = Util.TARGET_HOST, port: int = 4723, debug: bool = False) -> None:
#         '''Init control stream

#             Args::
#                 target_name: geolocation target name, str

#                 device_name: name of controlled device, str, default = "be47afa6"

#                 host: target host ip, str, default = "http://127.0.0.1"

#                 port: main app controllor port, int, default = 4723

#             Usage::
#                 ctrl = Control(target_name)
#                 or
#                 ctrl = Control(target_name, device_name)
#             ...
#         '''
#         self.target_name = target_name
#         self.device_name = device_name
#         self.host = host
#         self.port = port
#         # self.port2 = port2

#     def pickupDistance(self) -> tuple:
#         """Get current report distance between probe and target

#             Usage::
#                 ctrl.pickupDistance()
#             Return::
#                 (Location, distance(as int))
#         """
#         tantan = App(Util.TANTAN, self.device_name, self.host, self.port)
#         tantan.implicitlyWait(10)
#         try:
#             tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.TANTAN_SWIPETOCHECK)
#         except NoSuchElementException:
#             pass
#         try:
#             tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.TANTAN_CANCEL)
#         except NoSuchElementException:
#             pass
#         tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.TANTAN_MY)
#         tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.TANTAN_FOLLOW)
#         tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.text(self.target_name))
#         user_info = tantan.getContent(
#             Aby.ID, Util.TANTAN_USER_EXT).split('  •  ')

#         user_local = (re.match(r'(.*?)\((.*?)\)(.*?)', user_info[1]).group(1).strip(), re.match(r'(.*?)\((.*?)\)(.*?)', user_info[1]).group(2)) if "(" in user_info[1] \
#             else ("", user_info[1])
#         # print(user_local)
#         local, dis = user_local
#         unit = dis.find(Util.UNIT_KM) == -1
#         dis = int(dis[0:dis.find(Util.UNIT_M if unit else Util.UNIT_KM)]) * \
#             (1 if unit else 1000)
#         tantan.exit()
#         return (local, dis)

#     def refreshLocal(self) -> None:
#         """Refresh Location by reload

#             Usage::
#                 ctrl.refreshLocal()
#         """
#         tantan = App(Util.TANTAN, self.device_name, self.host, self.port)
#         tantan.implicitlyWait(10)
#         try:
#             tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.TANTAN_SWIPETOCHECK)
#         except NoSuchElementException:
#             pass
#         try:
#             tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.TANTAN_CANCEL)
#         except NoSuchElementException:
#             pass
#         tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.TANTAN_MY)
#         tantan.click(Aby.ID, Util.TANTAN_SETTING)
#         tantan.click(Aby.ANDROID_UIAUTOMATOR, Util.TANTAN_LOCAL)
#         tantan.implicitlyWait(5)
#         tantan.exit()

#     def changeModuleState(self, state: bool) -> None:
#         """Enable or Disable Module

#             Args:
#                 state: bool, true means checked
#             Usage::
#                 ctrl.changeModuleState(True)
#         """
#         lsp = App(Util.LSP, self.device_name,
#                   self.host, self.port)
#         lsp.implicitlyWait(10)
#         lsp.click(Aby.ANDROID_UIAUTOMATOR, Util.LSP_MODULE)
#         lsp.click(Aby.ANDROID_UIAUTOMATOR, Util.LSP_MODULE_NAME)
#         cur_state = lsp.getState(Aby.CLASS_NAME, Util.SWITCH)
#         if not(state and cur_state):
#             lsp.click(Aby.CLASS_NAME, Util.SWITCH)
#         lsp.exit()

#     def changeLocation(self, bsInfo: BSInfo, coord: Coord) -> None:
#         """Change Current app location

#             Args::
#                 bsInfo: BSInfo, Storage BS infos
#                 coord: Coord, Coordinate of GPS
#             Usage::
#                 ctrl.changeModuleState(True)
#         """
#         fl = App(Util.FAKELOCAL, self.device_name,
#                  self.host, self.port)
#         fl.implicitlyWait(10)
#         fl.click(Aby.ANDROID_UIAUTOMATOR, Util.text(
#             Util.APP_INFO[Util.TANTAN][0]))
#         fl.click(Aby.ANDROID_UIAUTOMATOR, Util.FAKELOCAL_CHANGE)
#         fl.input(Aby.ID, Util.FAKELOCAL_TAC, bsInfo.tac)
#         fl.input(Aby.ID, Util.FAKELOCAL_CI, bsInfo.ci)
#         fl.input(Aby.ID, Util.FAKELOCAL_PCI, bsInfo.pci)
#         fl.input(Aby.ID, Util.FAKELOCAL_MCC, bsInfo.mcc)
#         fl.input(Aby.ID, Util.FAKELOCAL_MNC, bsInfo.mnc)
#         fl.input(Aby.ID, Util.FAKELOCAL_LON, coord.lon)
#         fl.input(Aby.ID, Util.FAKELOCAL_LAT, coord.lat)
#         fl.click(Aby.ID, Util.FAKELOCAL_SAVE)
#         fl.exit()


# class WechatControl:
#     '''
#         Wechat App Control Module
#     '''

#     def __init__(self, target_name: str, device_name: str = Util.EMU_DEVICE, host: str = Util.TARGET_HOST, port: int = 4723) -> None:
#         '''Init control stream

#             Args::
#                 target_name: geolocation target name, str

#                 device_name: name of controlled device, str, default = "127.0.0.1"

#                 host: target host ip, str, default = "http://127.0.0.1"

#                 port1: main app controllor port, int, default = 62001

#             Usage::
#                 ctrl = Control(target_name)
#                 or
#                 ctrl = Control(target_name, device_name)
#             ...
#         '''
#         self.target_name = target_name
#         self.device_name = device_name
#         self.host = host
#         self.port = port
#         self.wechat = App(Util.WECHAT, self.device_name, self.host, self.port)

#     def clearPosition(self) -> None:
#         '''Clear the position and exit

#             Usage::
#                 ctrl.clearPosition()
#         '''
#         self.wechat.click(Aby.ID, Util.WECHAT_MORE)
#         self.wechat.click(Aby.ANDROID_UIAUTOMATOR, Util.WECHAT_CLEATANDEXIST)
#         self.wechat.click(Aby.ANDROID_UIAUTOMATOR, Util.WECHAT_OK)

#     def getNearByList(self) -> list:
#         '''Return list of Current display NearBy list

#             Usage::
#                 ctrl.getNearByList()

#             Return::
#                 list of WebElement
#         '''
#         return self.wechat.getElements(Aby.XPATH, Util.WECHAT_NEARBY_LIST)

#     def goNearByPage(self) -> None:
#         '''Click a series of buttons to go to a list of nearby people

#             Usage::
#                 ctrl.goNearByList()
#         '''
#         self.wechat.click(Aby.ANDROID_UIAUTOMATOR, Util.WECHAT_DISCOVER)
#         self.wechat.click(Aby.ANDROID_UIAUTOMATOR, Util.WECHAT_PEOPLE_NEARBY)
#         try:
#             self.wechat.click(Aby.ANDROID_UIAUTOMATOR, Util.WECHAT_START_CHECK)
#         except:
#             pass
#         self.wechat.elementWait(Aby.XPATH, Util.WECHAT_NEARBY_LIST)

#     def pickupDistance(self) -> float:
#         """Get current report distance between probe and target

#             Usage::
#                 ctrl.pickupDistance()

#             Return
#         """
#         dis = -1
#         state = True
        # while state:
        #     near_by = self.getNearByList()
        #     if len(near_by) < 8:
        #         continue
        #     for item in near_by:
        #         # Try catch to avoid exceptions
        #         try:
        #             name = self.wechat.getContentFromItem(
        #                 Aby.ID, Util.WECHAT_USERNAME, item)
        #             # User's distance from us
        #             dis_txt = self.wechat.getContentFromItem(
        #                 Aby.ID, Util.WECHAT_DISTANCE, item)
        #             unit_state = dis_txt.find(Util.UNIT_KMC) != -1
        #             unit = (dis_txt.find(Util.UNIT_KMC), 1000) if unit_state \
        #                 else (dis_txt.find(Util.UNIT_MC), 1)
        #             dis_num = float(dis_txt[0:unit[0]]) * unit[1]
        #             if name == self.target_name or dis_num >= 3000:
        #                 state = not name == self.target_name
        #                 dis = dis_num if name == self.target_name else 0
        #                 break
        #         except:
        #             pass
        #     self.wechat.swipeDown()
        # return dis

#     def refreshLocal(self) -> None:
#         """Refresh Location by reopen page

#             Usage::
#                 ctrl.refreshLocal()
#         """
#         self.wechat.back()
#         self.goNearByPage()

#     def closeApp(self) -> None:
#         '''Close App and Appium Session

#             Usage::
#                 ctrl.closeApp()
#         '''
#         self.wechat.exit()

# class MomoControl:
#     '''
#         Momo App Control Module
#     '''

#     def __init__(self, target_name: str, device_name: str = Util.EMU_DEVICE, host: str = Util.TARGET_HOST, port: int = 4723) -> None:
#         '''Init control stream

#             Args::
#                 target_name: geolocation target name, str

#                 device_name: name of controlled device, str, default = "127.0.0.1:62001"

#                 host: target host ip, str, default = "127.0.0.1:62001"

#                 port1: main app controllor port, int, default = 4723

#             Usage::
#                 ctrl = Control(target_name)
#                 or
#                 ctrl = Control(target_name, device_name)
#         '''
#         self.target_name = target_name
#         self.device_name = device_name
#         self.host = host
#         self.port = port
#         self.momo = App(Util.MOMO, self.device_name, self.host, self.port)

#     def backToLastPage(self) -> None:
#         '''Back to last page

#             Usage::
#                 ctrl.backToLastPage()
#         '''
#         self.momo.back()
#         time.sleep(0.5)

#     def goMessagePage(self) -> None:
#         """Open Message page for main page

#             Usage::
#                 ctrl.goMessagePage()
#         """
#         try:
#             self.momo.click(Aby.ANDROID_UIAUTOMATOR, Util.MOMO_MESSAGE)
#         except:
#             self.momo.back()
#             self.momo.click(Aby.ANDROID_UIAUTOMATOR, Util.MOMO_MESSAGE)

#     def pickupDistance(self) -> float:
#         """Get current report distance between probe and target

#             Usage::
#                 ctrl.getDistance()
#             Return::
#                 distance(as float)
#         """
#         try:
#             # Click the list of messages for the target user
#             self.momo.click(Aby.ANDROID_UIAUTOMATOR,
#                             Util.text(self.target_name))
#         except:
#             exit()
#         # Gets the user distance text
#         text = self.momo.getContent(Aby.ID, Util.MOMO_DISTANCE)

#         try:
#             dis_text = text.split("·")[1]
#             # dis = float(distext.split("k")[0]) * 1000
#             dis = float(dis_text.split("k")[0]) * 1000
#         except:
#             if text == Util.MOMO_HIDING:
#                 self.unfollowTargetUser()
#             else:
#                 dis = 99999999
#         return dis

#     def refreshLocal(self) -> None:
#         """Refresh Location by reload

#             Usage::
#                 ctrl.refreshLocal()
#         """
#         Util.close_app(self.momo.app_package)
#         time.sleep(3)
#         Util.start_app(self.momo.app_package)
#         time.sleep(4)
#         self.momo.click(Aby.ANDROID_UIAUTOMATOR, Util.MOMO_HOMEPAGE)
#         self.momo.swipeUp(100)
#         time.sleep(4)

#     def unfollowTargetUser(self) -> None:
#         '''Unfollow to get user location when at Target Chat Page

#             Usage::
#                 ctrl.unfollowTargetUser()
#         '''
#         # Go to the user's setting page
#         self.momo.click(Aby.ID, Util.MOMO_SETTING_PROFILE)
#         # Click current user information
#         self.momo.click(Aby.ID, Util.MOMO_USER_PROFILE)
#         # Go to edit page
#         self.momo.click(Aby.ID, Util.MOMO_PROFILE_EDIT)
#         # Click unfollow button
#         self.momo.click(Aby.ID, Util.MOMO_UNFOLLOW)
#         # click ok button
#         self.momo.click(Aby.ID, Util.MOMO_OK)
#         # return the profile page
#         self.backToLastPage()
#         # Return current user message Settings page
#         self.backToLastPage()
#         # return chatting window
#         self.backToLastPage()
#         # Return the chat list page
#         self.backToLastPage()

#     def closeApp(self) -> None:
#         '''Close App and Appium Session

#             Usage::
#                 ctrl.closeApp()
#         '''
#         self.momo.exit()


