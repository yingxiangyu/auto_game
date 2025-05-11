# coding=utf-8
"""
Author: yuyingxiang@baidu.com
Date: 2025/4/2 15:47 
Description: 
"""
import logging
import time

import keyboard

import utils
from mapiing import ACTION_MAPPING

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Flag:
    run_flag = True
    exit_flag = False



def stop_program():
    print("暂停程序...")
    Flag.run_flag = False

keyboard.add_hotkey('ctrl+q', stop_program)




actions = [
    [ACTION_MAPPING.play_game, 3],
    [ACTION_MAPPING.return_main, 1],
    [ACTION_MAPPING.skill_dianta, 1],
    # [ACTION_MAPPING.next_lvl, 1],
    # [ACTION_MAPPING.skill_jijia, 1],
]

select_skill_orders = [
    ACTION_MAPPING.skill_gun,
    # ACTION_MAPPING.skill_bingbao,
    #
    # ACTION_MAPPING.skill_ranyoudan,
    #
    # ACTION_MAPPING.skill_jiguang,
    #
    # ACTION_MAPPING.skill_ganbingdan,

    # ACTION_MAPPING.skill_wenyadan,
    ACTION_MAPPING.skill_dianci,
    ACTION_MAPPING.skill_car,
    ACTION_MAPPING.skill_wenyadan,
    # ACTION_MAPPING.skill_dianji,
]

static_pos = utils.set_game_pos()
while True:
    time.sleep(1)
    if not Flag.run_flag:
        continue
    if Flag.exit_flag:
        break
    for ac, counts in actions:
        pos = utils.find_image(ac.img, counts)
        logging.info(f"find {ac.name} {pos}")
        if pos:
            utils.click(pos)
            logging.info(f"find {ac.name} {pos}")
            time.sleep(1)
    pos = utils.find_image(ACTION_MAPPING.select_skill.img)
    if pos:
        for order in select_skill_orders:
            skill_pos = utils.find_image(order.img)
            if skill_pos:
                utils.click(skill_pos)
                logging.info(f"find skill {order.name} {pos}")
                break
        else:
            utils.click(pos)
    for pos in static_pos:
        utils.click(pos)
