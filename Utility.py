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
TELEGRAM = 'telegram'
'''
'''
FAKEGPS = "fakegps"
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
