# coding=utf-8
"""
Author: yuyingxiang@baidu.com
Date: 2025/4/2 15:47 
Description: 
"""
import logging
import time
from dataclasses import dataclass

import pyautogui
import pydirectinput  # 需安装：pip install pydirectinput

import win32gui
import win32con


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


def set_game_pos():
    hwnd_list = find_window('向僵尸开炮')
    width = 500
    height = 1000
    x = 1500
    click_pos = []
    for hwnd in hwnd_list:
        set_window_pos(hwnd, x, 0, width, height)
        click_pos.append(Point(x + width // 2 + 60, height + 70))
        x = x + width
    return click_pos


@dataclass
class Point:
    x: int
    y: int


def click(p: Point):
    move_to(p)
    pydirectinput.click()


def double_click(p: Point):
    pydirectinput.doubleClick(p.x, p.y)


def move_to(p: Point):
    pydirectinput.moveTo(p.x, p.y)


def find_image(image_path, count=1) -> Point | None:
    try:
        for _ in range(count):
            tt = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if tt is not None:
                return Point(int(tt.left + tt.width // 2), int(tt.top + tt.height // 2))
            time.sleep(0.2)
    except Exception as e:
        pass
