# encoding: utf-8

"""
基于python模拟原神抽卡过程并生成图表的语法练习作.
作者: relifenoxiao
时间: 2024/02/09
"""

# import collection 优化掉了
from tqdm import *
from decimal import Decimal
import simplejson as json  # 代替 import json
import os

# import sys

# sys.path.append(r"C:\Users\27161\Desktop\python_work\genshin_prac")

from draw.draw_4 import draw_4
from draw.draw_5 import draw_5

"""
输入模拟抽取次数，返回一个字典,包含绘图所有需要的数据
包括：
获取绘制出up的频数图的数据
draw_result_dict = {
      "up_5": 出限定五星的抽取次数分布
      "up_5_pc": 出限定五星的抽取次数分布（占比）
      "up_5_lj": 出限定五星的累计概率
      "_5": 出五星的抽取次数分布
      "_5_pc": 出五星的抽取次数分布（占比）
      "_5_lj": 出五星的累计概率
      "_4": 三个限定四星的抽取结果分布
      "_4_lj_sum": 限定四星出现的累计概率
      "_3": 三星的数量
      "_4_up": 某一个限定四星的数量
  }
"""

script_dir = os.path.dirname(__file__)  # 脚本所在目录
output_file = os.path.join(script_dir, "digital.json")  # 输出文件路径


def draw_card(cnt):

    # 创建两个字典存储对象出货时的抽数
    _5star_cnt = {
        "up": {},
        "other_5": {},
        "up_record": {},
    }  # up_record记录从上次up到这个up所用的抽数
    _4star_cnt = {"up1": {}, "up2": {}, "up3": {}, "other_4": 0, "other_3": 0}
    # 初始化字典
    for i in range(1, 181):
        _5star_cnt["up_record"][i] = 0
    for i in range(1, 91):
        _5star_cnt["up"][i] = 0
        _5star_cnt["other_5"][i] = 0
    for i in range(
        1, 23
    ):  # 由于可能存在保底被五星占用的情况，这里保证连续三金及以下不会出错
        _4star_cnt["up1"][i] = 0
        _4star_cnt["up2"][i] = 0
        _4star_cnt["up3"][i] = 0

    # 创建判断 5，4星是否保底使用的flag,以及计数器
    flag5 = False
    flag4 = False
    i5 = 1
    i4 = 1

    up_record = 0  # 记录出up时所用的抽数
    i4_record = 1
    # 依据权重进行抽取,并将抽取结果计入字典中
    for i in trange(cnt):
        # 执行一次抽卡，先判定是否为五星
        card_5 = draw_5(i5, flag5)
        up_record += 1

        # 如果未出五星
        if card_5 == None:
            # 记录本次抽取
            i5 += 1
            # 继续判定是否会出四星
            card_4 = draw_4(i4, flag4)
            # 如果没出，计数器加一，并记录抽取到了other。反之记录抽到的up，记录并初始化i4计数器,
            if card_4 == "other_3":
                _4star_cnt["other_3"] += 1
                i4 += 1
                i4_record += 1
            # 如果没出限定四星,记录，并获得四星up保底
            elif card_4 == "other_4":
                _4star_cnt["other_4"] += 1
                flag4 = True
                i4 = 1
                i4_record += 1
            # 如果出了限定四星,记录此时的抽数，并失去四星up保底，初始化抽取次数
            else:
                _4star_cnt[card_4][i4_record] += 1
                i4 = 1
                i4_record = 1
                flag4 = False

        # 如果歪了，则获得保底,记录本次抽取结果,初始化计数器i5,i4
        elif card_5 == "other_5":
            flag5 = True
            _5star_cnt["other_5"][i5] += 1
            i5 = 1

        # 如果出了5星up，则清除保底，记录本次抽取结果,初始化计数器i5,i4,清除
        else:
            flag5 = False
            _5star_cnt["up"][i5] += 1
            _5star_cnt["up_record"][up_record] += 1
            up_record = 0
            i5 = 1

    # 1.获取绘制出up的频数图的数据
    # 获得up_record中每个元素的个数，生成字典{次数：个数，...}，依据个数降序排列
    x_up_list = []
    y_up_list = []
    for key in _5star_cnt["up_record"]:
        x_up_list.append(key)
        y_up_list.append(_5star_cnt["up_record"][key])

    # 2.获取绘制出up按百分比分布图的数据,单位是百分之
    # 3.累计概率图
    y_up_percent_list = []
    y_up_lj_list = []
    # 计算所有的五星up总数
    all_sum = 0
    for item in y_up_list:
        all_sum += item

    pro_cnt = 0
    for item in y_up_list:
        Proportion = item / all_sum * 100
        pro_cnt += Proportion
        y_up_percent_list.append(
            Decimal(Proportion).quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
        )
        y_up_lj_list.append(
            Decimal(pro_cnt).quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
        )

    # 4，5，6. 获取出五星的频数图/占比图/累积概率图的数据
    x_5_list = []  # x轴的数据1 - 90
    y_5_list = []  # 频数
    y_5_pc_list = []  # 占比
    y_5_lj_list = []  # 累计概率

    all_sum = 0
    # 计算所有的五星总数
    for key in _5star_cnt["other_5"]:
        x_5_list.append(key)
        y_5_list.append(_5star_cnt["other_5"][key] + _5star_cnt["up"][key])
        all_sum += y_5_list[key - 1]

    pro_cnt = 0
    for item in y_5_list:
        Proportion = item / all_sum * 100
        pro_cnt += Proportion
        y_5_pc_list.append(
            Decimal(Proportion).quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
        )
        y_5_lj_list.append(
            Decimal(pro_cnt).quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
        )

    # 计算累计概率
    all_sum = 0
    for item in y_5_pc_list:
        all_sum += item
        y_5_lj_list.append(all_sum)

    # 7.获取出四星的占比图的数据
    # 8.获取出四星的累计概率图的数据
    x_4_list = []  # x轴的数据
    y_4_up1_pc_list = []  # 频数
    y_4_up2_pc_list = []
    y_4_up3_pc_list = []

    y_4_up_lj_list = []

    all_sum = 0  # 所有的up四星的总数

    for key in _4star_cnt["up1"]:
        all_sum += (
            _4star_cnt["up1"][key] + _4star_cnt["up2"][key] + _4star_cnt["up3"][key]
        )
    _4_up_cnt = 0  # 记录某个up四星的数量
    # 分别计算三个限定四星的抽取结果分布
    # 限定四星出现的累计概率
    pro_cnt = 0

    for key in _4star_cnt["up1"]:

        x_4_list.append(key)

        value = _4star_cnt["up1"][key]

        _4_up_cnt += value
        Proportion = value / all_sum * 100
        pro_cnt += Proportion
        y_4_up1_pc_list.append(
            Decimal(Proportion).quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
        )

        value = _4star_cnt["up2"][key]
        Proportion = value / all_sum * 100
        pro_cnt += Proportion
        y_4_up2_pc_list.append(
            Decimal(Proportion).quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
        )

        value = _4star_cnt["up3"][key]
        Proportion = value / all_sum * 100
        pro_cnt += Proportion
        y_4_up3_pc_list.append(
            Decimal(Proportion).quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
        )

        y_4_up_lj_list.append(
            Decimal(pro_cnt).quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
        )

    # 返回抽卡模块的结果
    draw_result_dict = {
        "up_5": [x_up_list, y_up_list],
        "up_5_pc": [x_up_list, y_up_percent_list],
        "up_5_lj": [x_up_list, y_up_lj_list],
        "_5": [x_5_list, y_5_list],
        "_5_pc": [x_5_list, y_5_pc_list],
        "_5_lj": [x_5_list, y_5_lj_list],
        "_4_pc": [x_4_list, y_4_up1_pc_list, y_4_up2_pc_list, y_4_up3_pc_list],
        "_4_lj_sum": [x_4_list, y_4_up_lj_list],
        "_3": _4star_cnt["other_3"],
        "_4_up": _4_up_cnt,
    }

    return draw_result_dict


if __name__ == "__main__":
    cnt = int(1e8)

    result_dict = draw_card(cnt)
    # 将模拟结果写入当前目录下的result.json中
    with open(output_file, "w", encoding="UTF-8") as f:
        json.dump(result_dict, f)

    print("succeed")
    _3_record = result_dict["_3"]

    Proportion = 100 - 1.605 - float(_3_record) / cnt * 100
    print(f"获得四星物品的综合概率{Proportion}%")

    _4_up_cnt = result_dict["_4_up"]
    _4_pc = 1 / (_4_up_cnt / cnt)
    print(f"获得某个up四星的期望为: {_4_pc}")

    print(result_dict["_4_pc"])
