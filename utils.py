# coding=utf-8
"""
Author: yuyingxiang@baidu.com
Date: 2025/4/2 15:47 
Description: 
"""
import base64
import time
from dataclasses import dataclass
from io import BytesIO

import cv2
import numpy as np
import pyautogui
import pydirectinput  # 需安装：pip install pydirectinput
import requests
import win32con
import win32gui

from skill_enum import detect_action
from skill_enum import Action


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
    x = 1900
    click_pos = []
    for hwnd in hwnd_list:
        set_window_pos(hwnd, x, 0, width, height)
        click_pos.append(Point(x + width // 2 + 60, height + 130))
        x = x + width
    return click_pos


@dataclass
class Point:
    x: int
    y: int


def click(p: Point):
    move_to(p)
    pydirectinput.click()
    time.sleep(0.1)


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


def find_resized_template(template_path, scale_factor=1.0):
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    template = cv2.resize(template, None, fx=scale_factor, fy=scale_factor)
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= 0.8:  # 置信度阈值
        return max_loc[0], max_loc[1], template.shape[1], template.shape[0]
    return None


def find_image_resized(image_path):
    # 示例：假设原图需要放大 1.5 倍
    start = 0.6
    while start <= 1:
        result = find_resized_template(image_path, scale_factor=start)
        if result is not None:
            return Point(int(result[0] + result[2] // 2), int(result[1] + result[3] // 2))
        start += 0.1


class Game:

    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.screen_left = None
        self.screen_top = None
        self.static_pos = self.find_static_pos()

    def get_window_img(self):
        client_left, client_top, client_right, client_bottom = win32gui.GetClientRect(self.hwnd)

        # 获取客户区左上角在屏幕中的位置
        (screen_left, screen_top) = win32gui.ClientToScreen(self.hwnd, (client_left, client_top))

        width = client_right - client_left
        height = client_bottom - client_top

        # 使用pyautogui截图
        screen = pyautogui.screenshot(region=(screen_left, screen_top, width, height))
        screen.save('window_screenshot.png')
        self.screen_left = screen_left
        self.screen_top = screen_top
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

    def find_static_pos(self):
        screen = self.get_window_img()
        tt = ocr(screen)
        for o in tt:
            action = detect_action(o.text)
            if action == Action.fight:
                return self.client_to_screen(o.point)


def new_set_game_pos():
    hwnd_list = find_window('向僵尸开炮')
    width = 500
    height = 1000
    x = 1900
    games = []
    for hwnd in hwnd_list:
        set_window_pos(hwnd, x, 0, width, height)
        games.append(Game(hwnd))
        x = x + width
    return games


@dataclass
class OcrRet:
    text: str
    point: Point


def ocr(image):
    image_bytes = BytesIO()
    image.save(image_bytes, format=image.format or 'PNG')  # 可根据需要选择格式，例如 'JPEG'
    encoded_string = base64.b64encode(image_bytes.getvalue()).decode("utf-8")

    uri = 'http://192.168.1.112:1224/api/ocr'
    data = {
        "base64": encoded_string,
        "options": {
            "ocr.language": "models/config_chinese.txt",
            "ocr.cls": True,
            "data.format": "string"
        }
    }
    rets = []
    for i in requests.post(uri, json=data).json()['data']:
        box = i['box']
        text = i['text']
        top_x = box[0][0]
        top_y = box[0][1]
        width = box[1][0] - box[0][0]
        high = box[2][1] - box[0][1]
        point_x = top_x + width // 2
        point_y = top_y + high // 2
        rets.append(OcrRet(text, Point(point_x, point_y)))
    return rets
