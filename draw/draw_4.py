# encoding: utf-8

"""
draw_4 模块用于执行可能出现4星的抽取
draw_4()返回None ,"up1","up2" ,"up3", "other",对应：没抽到，三个限定，和其他四星物品
"""


import random
from tqdm import *


# 定义draw_4函数来进行抽取操作的五星部分判断
# 传入参数为flag4用于判断是否保底，抽取次数i4判断出紫概率
# "up1","up2" ,"up3", "other_4", "other_3"
# 分别对应:三个up四星角色，其他四星物品, 三星
def draw_4(i, flag):
    # 创建元组和列表来判断是否出紫
    judge_tuple = ("up1", "up2", "up3", "other_4", "other_3")
    # 如果上次祈愿获取的4星物品非本期4星UP角色，则获得保底
    if flag == True:
        if i < 9:
            # 获取的4星物品必定为本期4星UP角色,4星物品基础概率为5.100%
            possibility = 0.051 / 3
            weights_list = [
                possibility,
                possibility,
                possibility,
                0,
                1 - possibility * 3,
            ]
        elif i == 9:
            # 获取的4星物品必定为本期4星UP角色,第九抽时4星物品概率陡增为56.1%
            possibility = 0.561 / 3
            weights_list = [
                possibility,
                possibility,
                possibility,
                0,
                1 - possibility * 3,
            ]
        else:
            possibility = 1 / 3
            weights_list = [possibility, possibility, possibility, 0, 0]
    else:
        if i < 9:
            possibility = 0.051 / 6
            weights_list = [
                possibility,
                possibility,
                possibility,
                possibility * 3,
                1 - possibility * 6,
            ]
        elif i == 9:
            possibility = 0.561 / 6
            weights_list = [
                possibility,
                possibility,
                possibility,
                possibility * 3,
                1 - possibility * 6,
            ]
        else:
            possibility = 0.5 / 3
            weights_list = [possibility, possibility, possibility, 0.5, 0]

    # 判断本次抽卡的结果并返回
    result = random.choices(judge_tuple, weights=weights_list)[0]
    return result


if __name__ == "__main__":

    flag4 = False
    i4 = 1
    _4star_cnt = {"up1": {}, "up2": {}, "up3": {}, "other_4": 0, "other_3": 0}
    for i in range(1, 12):
        _4star_cnt["up1"][i] = 0
        _4star_cnt["up2"][i] = 0
        _4star_cnt["up3"][i] = 0
    cnt = int(1e6)

    _up1_cnt = 0

    for i in trange(cnt):
        card_4 = draw_4(i4, flag4)
        # 如果没出，计数器加一，并记录抽取到了other。反之记录抽到的up，记录并初始化i4计数器,
        if card_4 == "other_3":
            _4star_cnt["other_3"] += 1
            i4 += 1
        # 如果没出限定四星,记录，并获得四星up保底
        elif card_4 == "other_4":
            _4star_cnt["other_4"] += 1
            flag4 = True
            i4 = 1
        # 如果出了限定四星,记录此时的抽数，并失去四星up保底，初始化抽取次数
        else:
            _4star_cnt[card_4][i4] += 1
            i4 = 1
            flag4 = False
            if card_4 == "up1":
                _up1_cnt += 1

    pc = 1 / (_up1_cnt / cnt)
    print(f"在剔除五星的情况下,获得某个限定四星的期望抽数是{pc}")
