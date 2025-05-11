import base64
import json
import time
from io import BytesIO

import requests

import utils

games = utils.new_set_game_pos()
image = games[0].get_window_img()
image.save('window_screenshot.png')
image_bytes = BytesIO()
image.save(image_bytes, format=image.format or 'PNG')  # 可根据需要选择格式，例如 'JPEG'
encoded_string = base64.b64encode(image_bytes.getvalue()).decode("utf-8")

t0 = time.time()
uri = 'http://192.168.1.112:1224/api/ocr'
data = {
    "base64": encoded_string,
    "options": {
        "ocr.language": "models/config_chinese.txt",
        "ocr.cls": True,
        # "ocr.limit_side_len": 4320,
        # "tbpu.parser": "multi_none",
        "data.format": "string"
    }
}
print(time.time() - t0)
for i in requests.post(uri, json=data).json()['data']:
    print(i['box'])
    print(i['text'])
