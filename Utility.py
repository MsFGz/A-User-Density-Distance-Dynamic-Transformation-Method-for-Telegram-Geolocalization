# coding = utf-8
import subprocess
from typing import Tuple

import numpy as np
from numpy import inf
from scipy import optimize

from FusedLocal import BSInfo, Coord
from Graph import Cirque


def text(content: str) -> str:
    return f'new UiSelector().text("{content}")'


def descriptionContains(content: str) -> str:
    return f'new UiSelector().descriptionContains("{content}")'

def accessibility_id(content: str) -> str:
    return f'new UiSelector().'


# App name
TANTAN = "tantan"
WECHAT = "wechat"
MOMO = 'momo'
TELEGRAM = 'telegram'
LINE = "line"
'''
FAKELOCAL = "fakelocation"
'''
FAKEGPS = "fakegps"
LSP = "lsposed"
# App infos
APP_INFO = {
    TANTAN: ('com.p1.mobile.putong', '.ui.splash.SplashProxyAct'),
    WECHAT: ('com.tencent.mm', '.ui.LauncherUI'),
    MOMO: ('com.immomo.momo', '.maintab.MaintabActivity'),
    # FAKELOCAL: ('com.silversliver.fakelocation.debug', 'com.silversliver.fakelocation.ui.activity.MainActivity'),
    FAKEGPS: ('com.lexa.fakegps','com.lexa.fakegps.ui.Main'),
    LSP: ('org.lsposed.manager', ".ui.activity.MainActivity"),
    TELEGRAM: ('org.telegram.messenger','org.telegram.ui.LaunchActivity'),
    LINE: ('jp.naver.line.android','jp.naver.line.android.activity.SplashActivity')
}
TARGET_HOST = "http://127.0.0.1"
# UI class
SWITCH = "android.widget.Switch"
# Fake GPS UI
FAKEGPS_NAVIGATION_DRAWER = "Open navigation drawer"
FAKEGPS_GOTO = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/androidx.appcompat.widget.LinearLayoutCompat[3]/android.widget.CheckedTextView'
FAKEGPS_LATLON = '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.EditText'    #text("latitude, longitude")在这里输入经纬度
  # FAKEGPS_LATLON = f"//*[@resource-id='android:id/custom']/android.widget.EditText"
FAKEGPS_OK = text("确定")
  # FAKEGPS_OK = f"android:id/button1"
FAKEGPS_START = f"{APP_INFO[FAKEGPS][0]}:id/action_start"
'''
# Fake Location UI
FAKELOCAL_CI = f"{APP_INFO[FAKELOCAL][0]}:id/value_ci"
FAKELOCAL_LON = f"{APP_INFO[FAKELOCAL][0]}:id/value_lon"
FAKELOCAL_LAT = f"{APP_INFO[FAKELOCAL][0]}:id/value_lat"
FAKELOCAL_MCC = f"{APP_INFO[FAKELOCAL][0]}:id/value_mcc"
FAKELOCAL_MNC = f"{APP_INFO[FAKELOCAL][0]}:id/value_mnc"
FAKELOCAL_PCI = f"{APP_INFO[FAKELOCAL][0]}:id/value_pci"
FAKELOCAL_TAC = f"{APP_INFO[FAKELOCAL][0]}:id/value_tac"
FAKELOCAL_SAVE = f"{APP_INFO[FAKELOCAL][0]}:id/save"
FAKELOCAL_CHANGE = text("修改")
'''
# Tantan UI
TANTAN_SETTING = f"{APP_INFO[TANTAN][0]}.core:id/setting_fram"
TANTAN_USER_EXT = f"{APP_INFO[TANTAN][0]}.feed:id/user_extend"
TANTAN_CANCEL = text("取消")
TANTAN_FOLLOW = text("关注")
TANTAN_LOCAL = text("位置")
TANTAN_MY = text("我")
TANTAN_PACLAGE_NAME = text(APP_INFO[TANTAN][0])
TANTAN_SWIPETOCHECK = text("滑卡查看")
# LSP UI
LSP_MODULE = descriptionContains("模块")
LSP_MODULE_NAME = text("越")

# Wechat UI
WECHAT_DISCOVER = text("发现")
WECHAT_PEOPLE_NEARBY = text("附近的人")
WECHAT_START_CHECK = text("开始查看")
WECHAT_CLEATANDEXIST = text("清除位置并退出")
WECHAT_OK = text("确定")
WECHAT_NEARBY_LIST = f"//*[@resource-id='{APP_INFO[WECHAT][0]}:id/dz7']/android.widget.LinearLayout" #怎么选的，是选的附近的人第一个还是整个附近的人列表
WECHAT_USERNAME = f"{APP_INFO[WECHAT][0]}:id/dz8"
WECHAT_DISTANCE = f"{APP_INFO[WECHAT][0]}:id/dz3"
WECHAT_MORE = f"{APP_INFO[WECHAT][0]}:id/cj"
WECHAT_DISDICT = {
    100: (0, 175),
    200: (35, 260),
    300: (115, 405),
    400: (220, 535),
    500: (335, 585),
    600: (430, 713),
    700: (495, 805),
    800: (630, 945),
    900: (675, 1055)
}

# Momo UI
MOMO_HOMEPAGE = text('首页')
MOMO_MESSAGE = text('消息')
MOMO_DISTANCE = f"{APP_INFO[MOMO][0]}:id/tv_time_distance"
MOMO_SETTING_PROFILE = f"{APP_INFO[MOMO][0]}:id/chat_menu_profile"
MOMO_USER_PROFILE = f"{APP_INFO[MOMO][0]}:id/layout_profile"
MOMO_PROFILE_EDIT = f"{APP_INFO[MOMO][0]}:id/menu_edit"
MOMO_UNFOLLOW = f"{APP_INFO[MOMO][0]}:id/setting_btn_unfollow"
MOMO_OK = text("确认")
MOMO_HIDING = "隐身"

# Telegram UI
TELEGRAM_NAVIGATION_MENU = "Open navigation menu"
TELEGRAM_PEOPLE_NEARBY = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[4]/android.widget.FrameLayout/android.widget.FrameLayout[3]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[4]"
# TELEGRAM_PEOPLE_NEARBY = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[4]/android.widget.FrameLayout/android.widget.FrameLayout[1]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[5]"
#TELEGRAM_PEOPLE_NEARBY = f"//*[@content-desc='New Message']/../android.widget.FrameLayout[2]/android.recyclerview.widget.RecyclerView/android.view.ViewGroup[4]"
TELEGRAM_GOBACK = "Go back"
#TELEGRAM_NEARBY_LIST = f"//*[@content-desc='Go bcak']/../../android.recyclerview.widget.RecyclerView/"
TELEGRAM_NEARBY_LIST = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[3]/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout"
TELEGRAM_USERNAME = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[3]/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.TextView[1]"
'''
TELEGRAM_USERNAME1 = f"//*[@content-desc='Go bcak']/../../android.recyclerview.widget.RecyclerView/android.widget.FrameLayout[4]/android.widget.TextView[1]"
TELEGRAM_USERNAME2 = 'TELEGRAM_USERNAME1路径中加1变为android.widget.FrameLayout[5]'
TELEGRAM_USERNAME3
...
'''
TELEGRAM_DISTANCE = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[3]/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.TextView[2]"
'''
TELEGRAM_DISTANCE1 = f"//*[@content-desc='Go bcak']/../../android.recyclerview.widget.RecyclerView/android.widget.FrameLayout[4]/android.widget.TextView[2]"
TELEGRAM_DISTANCE2 = 'TELEGRAM_DISTANCE1路径中加1变为android.widget.FrameLayout[5]'
TELEGRAM_DISTANCE3
...
'''
#TELEGRAM_SHOWMORE = f"//*[@content-desc='Go bcak']/../../android.recyclerview.widget.RecyclerView/android.widget.FrameLayout[9]" #加不加 /android.widget.TextView 都可
TELEGRAM_SHOWMORE = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[3]/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[9]"
TELEGRAM_STOPSM = f"//*[@content-desc='Go bcak']/../../android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[3]/android.widget.TextView"
#TELEGRAM_SETTING = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[3]/android.widget.FrameLayout/android.widget.FrameLayout[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[7]"
TELEGRAM_SETTING = f"//*[@content-desc='New Message']/../../android.widget.FrameLayout[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[7]"
TELEGRAM_CLEATANDEXIST = text("清除位置并退出")
TELEGRAM_OK = text("确定")
# Line UI

#LINE_PEOPLE_NEARBY = "People Nearby"
LINE_PEOPLE_NEARBY = """//android.widget.RelativeLayout[@content-desc="People Nearby"]"""
#LINE_NEARBYLIST = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView"
LINE_NEARBYLIST = f"{APP_INFO[LINE][0]}:id/nearby_list_recyclerview" 
LINE_USER = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout"
#LINE_USER = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout"
LINE_NAMEANDDIS = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.LinearLayout"
#LINE_USERNAME = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.LinearLayout/android.widget.TextView[1]"
LINE_USERNAME = f"{APP_INFO[LINE][0]}:id/nearby_location_text"
#LINE_DISTANCE = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.LinearLayout/android.widget.TextView[2]"
LINE_DISTANCE = f"{APP_INFO[LINE][0]}:id/nearby_name_text"


#JOYRUN UI
JOYRUN_IMAGE = "//android.widget.ImageView[@content-desc=\"悦跑圈\"]"
JOYRUN_START_ADS = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.appcompat.widget.LinearLayoutCompat/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ImageView"  # 刚打开悦跑圈时的弹窗广告
JOYRUN_COMMUNITY = text("社区")
JOYRUN_ADDFRIEND = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ImageView[1]"  # 添加用户按钮
JOYRUN_PEOPLE_NEARBY = text("附近")
JOYRUN_FALSE = text("获取定位失败，请尝试开启定位")
JOYRUN_NEARBY = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager"   # 附近用户界面
# JOYRUN_NEARBY_LIST = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.widget.TextView[1]"  # 附近的人用户列表
JOYRUN_NEARBY_LIST = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup"
JOYRUN_NEARBY_LIST_1 = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]"  # 附近用户列表第一个
JOYRUN_NEARBY_DYNAMIC = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[3]/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout"   # 附近动态列表
JOYRUN_NEARBY_DYNAMIC_1 = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[3]/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]"   # 附近动态列表第一个动态
JOYRUN_USERNAME = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.TextView[1]"# 个人主页用户昵称
JOYRUN_IMAGE_DYNAMIC = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[3]/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView"   # 附近动态用户头像列表
JOYRUN_USERNAME_DYNAMIC = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[3]/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.view.ViewGroup/android.widget.TextView"   # 附近动态里的用户昵称
JOYRUN_LOCATION_DYNAMIC = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[3]/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.TextView"   # 附近动态用户地址
JOYRUN_TIME_DYNAMIC = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[3]/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.TextView[1]"   # 动态发布时间
JOYRUN_DISTANCE_DYNAMIC = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[3]/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.TextView[2]"   # 附近动态的用户距离
# JOYRUN_END_DYNAMIC = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[3]/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout"   # 此标志出现表示以及滑动到动态的最后
JOYRUN_TAP_DYNAMIC = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[3]/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout"   # 一个用户的动态内容过大，需上划获取用户相对距离，此时无法点击用户头像跳转到用户主页，此时先点击发布日期和相对距离所在一栏跳转到动态页
JOYRUN_IMAGE_PERSON = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.ImageView"   # 动态详情页头像，点击即可进入用户主页
JOYRUN_END_DYNAMIC = text("没有更多了～")
JOYRUN_SEX = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.ImageView[2]"  # 个人主页用户性别
JOYRUN_LOCATION = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.TextView[2]"  # 个人主页用户资料所在地（不一定是当前位置所在地）
JOYRUN_LEVEL = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.TextView[3]"  # 个人主页用户等级
JOYRUN_SIGNATURE = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.TextView[4]"  # 个人主页用户个性签名
JOYRUN_DISTANCE = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.widget.TextView[3]"  # 列表页用户距离
JOYRUN_NAME = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.widget.TextView[1]"  # 列表页用户名
JOYRUN_TOTAL_MILEAGE = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.TextView[1]"  # 个人主页用户跑步总里程数
JOYRUN_FOLLOW_USERS_NUMBER = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.TextView[1]"  # 个人主页用户关注其他用户的数量
JOYRUN_FOLLOWERS_NUMBER = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.TextView[1]"  # 个人主页用户粉丝数
JOYRUN_SETTINGS = "设置"  # 用户个人主页设置按钮
JOYRUN_ID = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[2]"# 用户ID
JOYRUN_BACKSTAGE = "//android.widget.FrameLayout[@content-desc=\"悦跑圈,未加锁\"]/android.view.View"  # 悦跑圈后台元素

# Fake Location UI
FAKE_LOCATION_IMAGE = f"//android.widget.ImageView[@content-desc=\"Fake Location\"]"  # 主页里Fake Location图标
FAKE_LOCATION_BS_TEXT = text("基站模拟")  # 基站模拟文字，若出现，则按一下空白位置，再开始修改位置
FAKE_LOCATION_ADD = "com.lerist.fakelocation:id/fab"  # 添加模拟位置的按钮
FAKE_LOCATION_SELECT = text("选择位置")  # 选择位置按钮
FAKE_LOCATION_SEARCH = "//android.widget.Button[@content-desc=\"Search\"]"  # 点击搜索按钮
FAKE_LOCATION_INPUT = "com.lerist.fakelocation:id/l_search_panel_et_input"  # 输入框文本
FAKE_LOCATION_OK = "com.lerist.fakelocation:id/a_map_btn_done"  # 确定模拟位置按钮
FAKE_LOCATION_BS = "com.lerist.fakelocation:id/f_fakeloc_btn_cell"  # 点击基站按钮
FAKE_LOCATION_BS_LIST = "com.lerist.fakelocation:id/d_settings_mock_cell_ll_cells"  # 基站列表按钮，点击可刷新并开启基站模拟
FAKE_LOCATION_COORD = "com.lerist.fakelocation:id/f_fakeloc_tv_current_latlong"  # 模拟位置的经纬度
FAKE_LOCATION_STATE = text("启动模拟")  #检测fake location 状态，是否开启
FAKE_LOCATION_START = "com.lerist.fakelocation:id/f_fakeloc_tv_service_switch"  # 启动模拟按钮
FAKE_LOCATION_CLOSE = "com.lerist.fakelocation:id/f_fakeloc_tv_service_switch"  # 关闭模拟
# FAKE_LOCATION_CURRENT_LOCATION = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.TextView[2]"  #  当前坐标
FAKE_LOCATION_BS_STATE = text("开启")  # 检测基站模拟是否成功开启
FAKE_LOCATION_UPDATE = "com.lerist.fakelocation:id/parentPanel"  # 检测fake location更新弹窗是否出现
FAKE_LOCATION_NO_UPDATE = "android:id/button2"  # fake location暂不更新按钮，点击关闭更新弹窗



# Unit
UNIT_KM = "km"
UNIT_M = "m"
UNIT_KMC = "公里"
UNIT_MC = "米"

# Define
EMU_DEVICE = "127.0.0.1:52001"


def get_BS_info(coord: Coord) -> BSInfo:
    '''Get BS info according to coordinate 

        Usage::
            Utility.getBSInfo(coord)
        Return::
            BSInfo()
    '''
    # pass
    return BSInfo(4101, 21919747, 460, 0)


def dis_Cir(type: str, dis: float) -> Tuple:
    if type == WECHAT:
        return WECHAT_DISDICT.get(dis, ((dis - 50, dis + 50), (dis - 1000, dis))[dis == 1000])
    else:
        return (dis - (1000, 100)[dis > 1000], dis)


def save_as_file(type: str, target: str, coord: Coord) -> None:
    '''Save result to file

        Args::
            type: IM platform as (wechat, momo, tantan), str
            target: 
        Usage::
            Utility.save_as_file()
    '''
    with open(f"./txt/{type}/{target}.txt", 'w') as f:
        f.write(f"{coord.lon},{coord.lat}")


def trilateration_shpl(coo0: Tuple[float, float], dis0: Tuple[int, int], coo1: Tuple[float, float], dis1: Tuple[int, int], coo2: Tuple[float, float], dis2: Tuple[int, int]) -> Tuple[float, float]:
    p = Cirque(coo0[0], coo0[1], dis0[0], dis0[1]).graph\
        .intersection(Cirque(coo1[0], coo1[1], dis1[0], dis1[1]).graph) \
        .intersection(Cirque(coo2[0], coo2[1], dis2[0], dis2[1]).graph) \
        .centroid.coords[0]
    return (p[0], p[1])


def trilateration_opt(coo0: Coord, dis0: int, coo1: Coord, dis1: int, coo2: Coord, dis2: int) -> Coord:
    x1 = (coo1.lon+coo2.lon)/2
    x2 = (coo1.lat+coo2.lat)/2
    x = np.array([x1, x2])

    def f1(T: Tuple[float, float]):
        err = (coo0.getDistance(T) - dis0) ** 2 \
            + (coo1.getDistance(T) - dis1) ** 2 \
            + (coo2.getDistance(T) - dis2) ** 2
        return err
    ll = optimize.minimize(
        f1,
        x,
        args=(),
        method='BFGS',
        jac=False,
        tol=None,
        callback=None,
        options={
            'gtol': 1e-05,
            'norm': inf,
            'eps': 1.4901161193847656e-08,
            'maxiter': 300,
            'disp': False,
            'return_all': True,
            'finite_diff_rel_step': None
        })
    return Coord(ll.x[0], ll.x[1])


def change_location(coord: Coord, emu_name: str = "Probe1") -> None:
    '''Change geolocation in Emu
        Args::
            coord: the geolocation need be change, Coord
            emu_name: the emu name which will be operated, Default is "Probe1", str
        Usage::
            Utility.change_coords(coord)
    '''
    cmds = [
        f"NoxConsole.exe action -name:{emu_name} -key:call.locate -value:{coord.lon},{coord.lat}\n",
        "exit",
    ]
    obj = subprocess.Popen("powershell.exe", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    obj.communicate(("\n".join(cmds) + "\n").encode('utf-8'))


def close_app(app_name: str, emu_name: str = "Probe1") -> None:
    '''Close app in Emu
        Args::
            app_name: the app package name which will be operated, str
            emu_name: the emu name which will be operated, Default is "Probe1", str
        Usage::
            Utility.close_app(app_name)
    '''
    cmds = [
        f"NoxConsole.exe killapp -name:{emu_name} -packagename:{app_name}",
        "exit",
    ]
    obj = subprocess.Popen("powershell.exe", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    obj.communicate(("\n".join(cmds) + "\n").encode('utf-8'))


def start_app(app_name: str, emu_name: str = "Probe1") -> None:
    '''Start app in Emu
        Args::
            app_name: the app package name which will be operated, str
            emu_name: the emu name which will be operated, Default is "Probe1", str
        Usage::
            Utility.close_app(app_name)
    '''
    cmds = [
        f"NoxConsole.exe runapp -name:{emu_name} -packagename:{app_name}",
        "exit",
    ]
    obj = subprocess.Popen("powershell.exe", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    obj.communicate(("\n".join(cmds) + "\n").encode('utf-8'))
