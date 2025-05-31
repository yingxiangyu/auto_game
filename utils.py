# coding=utf-8
"""
Author: yuyingxiang@baidu.com
Date: 2025/4/2 15:47 
Description: 
"""
import time
from dataclasses import dataclass
from threading import Lock

import pyautogui
import pydirectinput  # 需安装：pip install pydirectinput
import win32con
import win32gui

# 全局窗口大小设置
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 1200


def set_window_pos(hwnd, x, y, width, height):
    """
    设置窗口位置和大小
    :param hwnd: 窗口句柄
    :param x: 左上角X坐标
    :param y: 左上角Y坐标
    :param width: 宽度
    :param height: 高度
    """
    # 参数说明：
    # hWnd: 窗口句柄
    # hWndInsertAfter: 窗口Z序（如置顶用win32con.HWND_TOPMOST）
    # X, Y, cx, cy: 位置和尺寸
    # uFlags: 选项标志（SWP_NOZORDER表示保持当前Z序）
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOP,  # 保持窗口在当前Z序（非置顶）
        x, y,
        width, height,
        win32con.SWP_NOZORDER
    )


# 示例：设置记事本窗口
def find_window(key_word):
    hwnd_list = []
    hwnd = win32gui.FindWindow(None, key_word)
    while hwnd:
        hwnd_list.append(hwnd)
        hwnd = win32gui.FindWindowEx(None, hwnd, None, key_word)
    return hwnd_list


@dataclass
class Point:
    x: int
    y: int


lock = Lock()


def click(p: Point):
    with lock:
        move_to(p)
        pydirectinput.click()
        time.sleep(0.1)


def double_click(p: Point):
    pydirectinput.doubleClick(p.x, p.y)


def move_to(p: Point):
    pydirectinput.moveTo(p.x, p.y)


class Game:

    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.screen_left = None
        self.screen_top = None
        self.screen_right = None
        self.screen_bottom = None
        self.static_pos = None
        self.jijia_point = None
        self.jiguang_point = None
        self.next_stage = None
        self.exit_point = None

    def get_window_img(self):
        width = self.screen_right - self.screen_left
        height = self.screen_bottom - self.screen_top
        # 使用pyautogui截图
        screen = pyautogui.screenshot(region=(self.screen_left, self.screen_top, width, height))
        screen.save('window_screenshot.png')
        return screen

    def client_to_screen(self, point):
        """
        将窗口坐标转换为屏幕坐标
        """
        screen_x = self.screen_left + point.x
        screen_y = self.screen_top + point.y
        return Point(screen_x, screen_y)

    def screen_to_client(self, point):
        """
        将屏幕坐标转换为窗口坐标
        """
        client_x = point.x - self.screen_left
        client_y = point.y - self.screen_top
        return Point(client_x, client_y)

    def init_points(self):
        client_left, client_top, client_right, client_bottom = win32gui.GetClientRect(self.hwnd)

        # 获取客户区左上角在屏幕中的位置
        (screen_left, screen_top) = win32gui.ClientToScreen(self.hwnd, (client_left, client_top))
        (client_right, client_bottom) = win32gui.ClientToScreen(self.hwnd, (client_right, client_bottom))
        self.screen_left = screen_left
        self.screen_top = screen_top
        self.screen_right = client_right
        self.screen_bottom = client_bottom

        # self.static_pos = self.client_to_screen(Point(300, 1150))
        # self.jijia_point = self.client_to_screen(Point(530, 850))
        # self.jiguang_point = self.client_to_screen(Point(530, 950))

        self.static_pos = self.client_to_screen(Point(int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.95)))
        self.jijia_point = self.client_to_screen(Point(int(WINDOW_WIDTH * 0.88), int(WINDOW_HEIGHT * 0.71)))
        self.jiguang_point = self.client_to_screen(Point(int(WINDOW_WIDTH * 0.88), int(WINDOW_HEIGHT * 0.79)))
        self.next_stage = self.client_to_screen(Point(int(WINDOW_WIDTH * 0.79), int(WINDOW_HEIGHT * 0.45)))
        self.exit_point = self.client_to_screen(Point(int(WINDOW_WIDTH * 0.08), int(WINDOW_HEIGHT * 0.08)))


def set_game_pos():
    hwnd_list = find_window('向僵尸开炮')
    hwnd_list = sorted(hwnd_list)
    x = 1300
    games = []
    for hwnd in hwnd_list:
        set_window_pos(hwnd, x, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        games.append(Game(hwnd))
        x += WINDOW_WIDTH  # 递增 X 坐标    return games
    return games
