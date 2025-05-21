import logging
import time
from threading import Thread

import keyboard
import utils
from skill_enum import detect_action
from skill_enum import detect_skills
from skill_enum import Skill
from skill_enum import Action

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Flag:
    run_flag = True


def stop_program():
    print("暂停程序...")
    Flag.run_flag = False


def start_program():
    print("开始程序...")
    Flag.run_flag = True


keyboard.add_hotkey('ctrl+q', stop_program)
keyboard.add_hotkey('ctrl+e', start_program)

skill_order = [
    Skill.better,

    Skill.gun,
    Skill.zhuang_jia_che,



    Skill.bing_bao_fa_sheng_qi,
    Skill.gan_bing_dan,
    Skill.zhi_dao_ji_guang,

    Skill.dian_ci_chuan_ci,
    Skill.ran_you_dan,
    Skill.wen_ya_dan,
    Skill.zhuang_jia_che
]


def match_skills(ocr_skills, game):
    for skill in skill_order:
        for ock_sk, pos in ocr_skills:
            if skill == ock_sk:
                logging.info(f"find {skill.value}  {pos}")
                utils.click(pos)
                return
    else:
        skill, pos = ocr_skills[0]
        logging.info(f"find {skill}  {pos}")
        utils.click(pos)


def play(game):
    game.init_points()
    skill_count = 0
    while True:
        time.sleep(1)
        if not Flag.run_flag:
            continue
        screen = game.get_window_img()
        ocr = utils.ocr(screen)
        ocr_skills = []
        for o in ocr:
            action = detect_action(o.text)
            if action:
                logging.info(f"find {action.value} {o.point}")
                if action in [
                    Action.goback,
                    Action.play_game
                ]:
                    pos = game.client_to_screen(o.point)
                    utils.click(pos)
                    skill_count = 0
                    break
            skill = detect_skills(o.text)
            if skill:
                logging.info(f"find {skill.value}  {o.point}")
                ocr_skills.append([skill, game.client_to_screen(o.point)])
        if ocr_skills:
            match_skills(ocr_skills, game)
            skill_count += 1
        utils.click(game.static_pos)
        if skill_count > 0 and skill_count % 3 == 0:
            utils.click(game.jiguang_point)
        if skill_count == 4:
            utils.click(game.jijia_point)


if __name__ == '__main__':
    games = utils.new_set_game_pos()
    for tt in games:
        t = Thread(target=play, args=(tt,))
        t.daemon = True
        t.start()
    while True:
        time.sleep(1)
