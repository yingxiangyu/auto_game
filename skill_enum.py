# encoding:utf-8

from typing import Optional

from enum import Enum


class Skill(Enum):
    """技能类型枚举"""
    wen_ya_dan = '温压弹'
    gan_bing_dan = '干冰弹'
    dian_ci_chuan_ci = '电磁穿刺'
    zhuang_jia_che = '装甲车'
    gao_neng_she_xian = '高能射线'
    zhi_dao_ji_guang = '制导激光'
    bing_bao_fa_sheng_qi = '冰暴发生器'
    yue_qian_dian_zi = '跃迁电子'
    xuan_feng = '旋风加农'
    kong_tou_hong_zha = '空投轰炸'
    ya_suo_qi_ren = '压缩气刃'
    ran_you_dan = '燃油弹'
    wu_ren_ji = '无人机冲击'
    dian_ji_zhu = '电极柱'
    duo_wei_dan_zhu = '多维弹珠'
    shi_kong_lie_xi = '时空裂隙'
    gun = '枪'
    better = '优先技能'


class Action(Enum):
    play_game = '开始游戏'
    fight = '战斗'
    chose_skills = '选择技能'
    refresh = '刷新'
    goback = '返回'
    challenge = '挑战'
    confirm = '确定'


def detect_skills(text: str) -> Optional[Skill]:
    skill_keywords = [
        ((
             '急冻子弹', '弹道数量', '分裂冰片',
             '子弹伤害', '学习装甲车', '子弹爆炸',
             '学习冰暴发生器', '学习温压弹', '冰暴扩张','连环冰暴',
             '出击次数', '射击连发数', '分裂子弹',
             '分裂子弹四射', '爆炸扩散', '焦土',
         ), Skill.better),
        (('温压弹',), Skill.wen_ya_dan),
        (('冰弹',), Skill.gan_bing_dan),
        (('电磁',), Skill.dian_ci_chuan_ci),
        (('装甲车', '坦克'), Skill.zhuang_jia_che),
        (('高能射线',), Skill.gao_neng_she_xian),
        (('制导激光',), Skill.zhi_dao_ji_guang),
        (('冰暴',), Skill.bing_bao_fa_sheng_qi),
        (('跃迁', '电离爆炸'), Skill.yue_qian_dian_zi),
        (('旋风加农', '龙卷风'), Skill.xuan_feng),
        (('轰炸',), Skill.kong_tou_hong_zha),
        (('气刃',), Skill.ya_suo_qi_ren),
        (('燃油弹', '灼烧', '点燃', '快速装填'), Skill.ran_you_dan),
        (('无人机',), Skill.wu_ren_ji),
        (('电极',), Skill.dian_ji_zhu),
        (('弹珠',), Skill.duo_wei_dan_zhu),
        (('时空裂隙',), Skill.shi_kong_lie_xi),
        (('子弹', '射速', '连发数'), Skill.gun),

    ]

    for keywords, skill in skill_keywords:
        for keyword in keywords:
            if keyword in text:
                return skill
    return None


def detect_action(text: str) -> Optional[Action]:
    for name, ac in Action.__dict__['_member_map_'].items():
        if ac.value in text:
            return ac
    return None


if __name__ == '__main__':
    print(detect_skills('连续出击'))
    print(detect_action('开始游戏'))
    print(detect_action('1/2确定'))
