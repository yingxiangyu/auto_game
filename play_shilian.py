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

    Skill.dian_ci_chuan_ci,
    Skill.ran_you_dan,
    Skill.wen_ya_dan,
    #
    # Skill.bing_bao_fa_sheng_qi,
    # Skill.gan_bing_dan,
    # Skill.zhi_dao_ji_guang,

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


def combin_skills(ocr_skills):
    # 先按照 x 坐标排序，便于后续分组
    ocr_skills.sort(key=lambda item: item[1].x)

    groups = []
    for ock_sk, pos in ocr_skills:
        if not groups:
            # 第一组直接添加
            groups.append([[ock_sk, pos]])
        else:
            last_group = groups[-1]
            last_pos = last_group[0][1]
            # 判断当前技能是否与上一组的中心 x 在 50 范围内
            if abs(pos.x - last_pos.x) < 50:
                # 属于当前组
                groups[-1].append([ock_sk, pos])
            else:
                # 新建一个组
                groups.append([[ock_sk, pos]])

    # 从每组中选择一个最优技能
    ret = []
    for group in groups:
        # 优先选择 Skill.better
        better_skill = next((item for item in group if item[0] == Skill.better), None)
        if better_skill:
            ret.append(better_skill)
        else:
            # 否则选择第一个
            ret.append(group[0])

    return ret


def play(game):
    print('start')
    game.init_points()
    skill_count = 0
    while True:
        time.sleep(1)
        if not Flag.run_flag:
            continue
        screen = game.get_window_img()
        ocr = utils.ocr(screen)
        ocr_skills = []
        confirm_pos = None
        for o in ocr:
            action = detect_action(o.text)
            if action:
                if action == Action.confirm:
                    logging.info(f"find {action.value} {o.point}")
                    confirm_pos = game.client_to_screen(o.point)
                    continue
                if action in [
                    Action.goback,
                    Action.challenge,
                    Action.play_game
                ]:
                    logging.info(f"find {action.value} {o.point}")
                    pos = game.client_to_screen(o.point)
                    utils.click(pos)
                    skill_count = 0
            skill = detect_skills(o.text)
            if skill:
                ocr_skills.append([skill, game.client_to_screen(o.point)])
        if ocr_skills:
            ocr_skills = combin_skills(ocr_skills)
            if confirm_pos:
                click_his = []
                for ock_sk, pos in ocr_skills:
                    if ock_sk == Skill.better:
                        click_his.append(pos)
                        logging.info(f"find {ock_sk.value}  {pos}")
                        utils.click(pos)
                for skill in skill_order:
                    for ock_sk, pos in ocr_skills:
                        if pos in click_his:
                            continue
                        if skill == ock_sk:
                            logging.info(f"find {skill.value}  {pos}")
                            click_his.append(pos)
                            utils.click(pos)
                else:
                    for ock_sk, pos in ocr_skills:
                        if pos in click_his:
                            continue
                        skill = ock_sk
                        logging.info(f"find {skill}  {pos}")
                        utils.click(pos)
                utils.click(confirm_pos)
            else:
                match_skills(ocr_skills, game)
                skill_count += 1
        # utils.click(game.static_pos)
        if skill_count > 0 and skill_count % 2 == 0:
            utils.click(game.jiguang_point)
        if skill_count == 3:
            utils.click(game.jijia_point)


if __name__ == '__main__':
    games = utils.new_set_game_pos()
    for tt in games:
        t = Thread(target=play, args=(tt,))
        t.daemon = True
        t.start()
    while True:
        time.sleep(1)
