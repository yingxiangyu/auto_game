import os
import time
from pynput import mouse
from PIL import ImageGrab


class ScreenshotTool:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.listener = None

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            self.start_x, self.start_y = x, y
        elif button == mouse.Button.left and not pressed:
            self.end_x, self.end_y = x, y
            return False  # 停止监听

    def select_area(self):
        print("请按住鼠标左键并拖动选择截图区域（松开左键完成选择）")
        with mouse.Listener(on_click=self.on_click) as self.listener:
            self.listener.join()

        # 确保选择的区域有效
        if None in (self.start_x, self.start_y, self.end_x, self.end_y):
            print("未正确选择区域，请重新运行")
            return None

        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        return (x1, y1, x2, y2)

    def take_screenshot(self, bbox):
        return ImageGrab.grab(bbox=bbox)

    def save_screenshot(self, image):
        save_path = input("请输入保存路径（留空则保存到当前目录）：").strip()
        if not save_path:
            save_path = os.path.join(os.getcwd(), 'images')

        filename = input("请输入文件名（不带扩展名）：").strip()
        if not filename:
            filename = f"screenshot_{int(time.time())}"

        os.makedirs(save_path, exist_ok=True)
        filepath = os.path.join(save_path, f"{filename}.png")
        image.save(filepath)
        print(f"截图已保存到：{filepath}")


def main():
    tool = ScreenshotTool()
    bbox = tool.select_area()
    if bbox:
        screenshot = tool.take_screenshot(bbox)
        tool.save_screenshot(screenshot)


if __name__ == "__main__":
    main()
