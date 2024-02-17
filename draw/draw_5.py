# encoding: utf-8
"""
draw_5 模块用于执行可能出现5星的抽取
draw_5()返回None ,"up", "other_5",中的一个。分别对应没抽到，限定和常驻五星
单独运行draw_5可获得:
限定五星占总抽卡数的值为: 1.07%, 获得一个限定五星期望为: 93.5次
5星占总抽卡数的值为: 1.6%, 获得一个五星期望为: 62.3次
"""
import random
import collections
from tqdm import *


# 定义draw_5函数来进行抽取操作的五星部分判断
# 传入参数为flag5用于判断是否大保底，抽取次数i5判断出金概率
# 返回None ,"up", "other_5",中的一个对应没抽到，限定和常驻五星
def draw_5(i, flag):
    # 依据抽取次数判断出五星的概率
    if i <= 73:
        possibility = 0.006
    elif i < 90:
        possibility = 0.006 + 0.06 * (i - 73)
    else:
        possibility = 1

    # 创建元组和列表来判断是否出金
    judge_tuple = (True, False)
    weights_list = [possibility, 1 - possibility]
    # 判断本次抽卡是否出金
    result = random.choices(judge_tuple, weights=weights_list)[0]

    # 如果没抽到返回None
    if result == False:
        return None
    # 反之则为抽到，此时判断是否为up角色
    if flag:
        return "up"  # 如果已经保底
    else:
        item_tuple = ("up", "other_5")
        result = random.choices(item_tuple, weights=[0.5, 0.5])[0]
        return result


# 本部分的功能是进行模拟抽卡，统计出货时的抽数，并计算抽取到up角色所需要的抽数。
# 记录抽取次数，以及抽取到的up数。
if __name__ == "__main__":

    up_star_5 = 0
    _star_5 = 0
    count = 0
    # 创建一个flag用于判断是否触发大保底。
    flag = False
    # 创建一个空列表用于接收抽取结果
    results_list = []
    # 模拟出金cnt次
    cnt = int(1e6)
    for j in trange(cnt):
        # 初始化抽取次数i为1
        i = 1
        while True:
            # 进行抽取操作
            result = draw_5(i, flag)
            # 若是up则清除大保底，记录并结束本次循环。
            if result == "up":
                flag = False
                up_star_5 += 1
                break
            # 若是other_5则获得大保底并结束本次循环。
            if result == "other_5":
                flag = True
                _star_5 += 1
                break
            # 继续下一次抽取
            i += 1
        # 记录本次出金所用抽数，并将其添加到列表results_list中
        count += i
        results_list.append(i)

    _star_5 += up_star_5
    # 获得列表中每个元素的个数，生成字典{元素：个数，...}，依据个数降序排列
    result_dict = collections.Counter(results_list)
    print(result_dict)

    # 计算up角色占总抽数的百分比，同时计算期望
    Proportion = float(up_star_5) / count * 100
    Proportion1 = float(_star_5) / count * 100

    print(
        f"限定五星占总抽卡数的值为: {Proportion}%, 获得一个限定五星期望为：{100.0 / Proportion }次"
    )
    print(
        f"5星占总抽卡数的值为: {Proportion1}%, 获得一个五星期望为：{100.0 / Proportion1 }次"
    )
