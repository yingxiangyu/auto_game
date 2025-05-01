# coding=utf-8
"""
Author: yuyingxiang@baidu.com
Date: 2025/4/2 14:26 
Description: 
"""
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(base_dir, 'images')

all_images = os.listdir(image_dir)
all_action = [i[:-4] for i in all_images]


class ActionImg:
    def __init__(self, name, img, action=None):
        self.img = img
        self.action = action
        self.name = name


class ACTION_MAPPING:
    play_game = ActionImg('play_game', os.path.join(image_dir, 'play_game' + '.png'))
    return_main = ActionImg('return_main', os.path.join(image_dir, 'return_main' + '.png'))
    select_skill = ActionImg('select_skill', os.path.join(image_dir, 'select_skill' + '.png'))

    skill_jijia= ActionImg('skill_jijia', os.path.join(image_dir, 'skill', 'jijia' + '.png'))
    skill_jijia2= ActionImg('skill_jijia2', os.path.join(image_dir, 'skill', 'jijia2' + '.png'))
    skill_gun = ActionImg('skill_gun', os.path.join(image_dir, 'skill', 'gun' + '.png'))
    skill_dianta= ActionImg('skill_dianta', os.path.join(image_dir, 'skill', 'dianta' + '.png'))


    skill_wurenji = ActionImg('skill_wurenji', os.path.join(image_dir, 'skill', 'wurenji' + '.png'))
    skill_car= ActionImg('skill_car', os.path.join(image_dir, 'skill', 'car' + '.png'))
    skill_feiji = ActionImg('skill_feiji', os.path.join(image_dir, 'skill', 'feiji' + '.png'))

    skill_dianci = ActionImg('skill_dianci', os.path.join(image_dir, 'skill', 'dianci' + '.png'))
    skill_dianzi= ActionImg('skill_dianzi', os.path.join(image_dir, 'skill', 'dianzi' + '.png'))

    skill_ganbingdan= ActionImg('skill_ganbingdan', os.path.join(image_dir, 'skill', 'ganbingdan' + '.png'))
    skill_bingbao = ActionImg('skill_bingbao', os.path.join(image_dir, 'skill', 'bingbao' + '.png'))

    skill_xuanfeng = ActionImg('skill_xuanfeng', os.path.join(image_dir, 'skill', 'xuanfeng' + '.png'))
    skill_fengren = ActionImg('skill_fengren', os.path.join(image_dir, 'skill', 'fengren' + '.png'))

    skill_shexian = ActionImg('skill_shexian', os.path.join(image_dir, 'skill', 'shexian' + '.png'))
    skill_jiguang= ActionImg('skill_jiguang', os.path.join(image_dir, 'skill', 'jiguang' + '.png'))

    skill_ranyoudan= ActionImg('skill_ranyoudan', os.path.join(image_dir, 'skill', 'ranyoudan' + '.png'))
    skill_wenyadan= ActionImg('skill_wenyadan', os.path.join(image_dir, 'skill', 'wenyadan' + '.png'))


for ac in all_action:
    setattr(ACTION_MAPPING, ac, ActionImg(ac, os.path.join(image_dir, ac + '.png')))
