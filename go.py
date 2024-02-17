# encoding: utf-8

"""
基于python模拟原神抽卡过程并生成图表的语法练习作.
作者: relifenoxiao
时间: 2024/02/13
"""

from draw_card import draw_card
from drawing import draw_pic


# re_data用于
def re_data(cnt):
    """用于重新获得抽卡结果,结果会自动写入digital.json中

    Args:
        cnt (int): 希望执行的抽卡次数(建议不大于1e8)
    """
    draw_card(cnt)


draw_pic()
