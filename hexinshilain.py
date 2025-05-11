import time

import keyboard

import utils
from mapiing import ACTION_MAPPING


class Flag:
    run_flag = True


def stop_program():
    print("暂停程序...")
    Flag.run_flag = False


keyboard.add_hotkey('ctrl+q', stop_program)

static_pos = utils.set_game_pos()

select_skill_orders = [
    ACTION_MAPPING.skill_gun,

    ACTION_MAPPING.skill_dianci,

    ACTION_MAPPING.skill_car,

    ACTION_MAPPING.skill_wenyadan,
]
actions = [
    ACTION_MAPPING.hexin_start,
    ACTION_MAPPING.hexin_enter_game,
    ACTION_MAPPING.return_main,
    ACTION_MAPPING.skill_dianta,
]

while True:
    if not Flag.run_flag:
        break
    for ac in actions:
        pos = utils.find_image(ac.img)
        if pos:
            utils.click(pos)
            print(f"find {ac.name} {pos}")
            time.sleep(0.5)
    if utils.find_image(ACTION_MAPPING.double_select_start.img):
        print("select double skills")
        utils.click(utils.Point(1980, 700))
        utils.click(utils.Point(2150, 700))
        utils.click(utils.find_image(ACTION_MAPPING.double_select_end.img))
    pos = utils.find_image(ACTION_MAPPING.select_skill.img)
    if pos:
        for order in select_skill_orders:
            skill_pos = utils.find_image(order.img)
            if skill_pos:
                utils.click(skill_pos)
                print(f"find skill {order.name} {pos}")
                break
        else:
            utils.click(pos)
    for pos in static_pos:
        utils.click(pos)

    time.sleep(1)
