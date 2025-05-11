import logging
import time

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
    Skill.gun,
    Skill.dian_ci_chuan_ci,
    Skill.zhuang_jia_che,
    Skill.ran_you_dan,
    Skill.wen_ya_dan,
]


def match_skills(ocr_skills, game):
    for skill in skill_order:
        for ock_sk, pos in ocr_skills:
            if skill == ock_sk:
                logging.info(f"find {skill.value}  {pos}")
                utils.click(pos)
                return
    else:
        skill,pos = ocr_skills[0]
        logging.info(f"find {skill}  {pos}")
        utils.click(pos)


def play(game):
    while True:
        time.sleep(1)
        if not Flag.run_flag:
            continue
        screen = game.get_window_img()
        ocr = utils.ocr(screen)
        ocr_skills = []
        for o in ocr:
            action = detect_action(o.text)
            if action and action in [
                Action.fight,
                Action.goback,
                Action.play_game
            ]:
                logging.info(f"find {action.name} {o.point}")
                pos = game.client_to_screen(o.point)
                utils.click(pos)
                break
            skill = detect_skills(o.text)
            if skill:
                ocr_skills.append([skill, game.client_to_screen(o.point)])
        print(ocr_skills)
        if ocr_skills:
            match_skills(ocr_skills, game)


if __name__ == '__main__':
    games = utils.new_set_game_pos()
    play(games[0])
