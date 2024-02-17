# encoding: utf-8

"""
基于python模拟原神抽卡过程并生成图表的语法练习作.
作者: relifenoxiao
时间: 2024/02/12
"""


import simplejson as json
from pyecharts.commons.utils import JsCode
from tqdm import *
from pyecharts.charts import *
from pyecharts.options import *
import os

# 练习
# import sys
# sys.path.append(r"C:\Users\27161\Desktop\python_work\genshin_prac")
from draw_card import *


def get_output_file(name):
    # 使用当前工作目录作为基准
    cwd = os.getcwd()
    # 使用期望输出的目录和输出文件的名称拼接
    output_file = os.path.join(cwd, "genshin_prac\\result", name)
    return output_file


def draw_pic():
    with open(r"genshin_prac\digital.json", "r", encoding="UTF-8") as f:
        digital = f.read()

    digital_dict = json.loads(digital)

    """
    得到了如下数据：
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
    需要绘制：
    1. up 5星出卡时抽数的频数分布图
    2. up 5五星的抽取次数分布(占比)
    3. up 5星每抽的累进概率图
    4. 5星出卡时抽数的频数分布图
    5. 5五星的抽取次数分布(占比)
    6. 5星每抽的累进概率图
    7. up 4星每抽出现的占比分布图 _4_pc
    8. up 4星在每一抽的累进概率图 _4_lj_sum
    """
    # 删去不需要的"_3"，"_4_up"
    digital_dict.pop("_3")
    digital_dict.pop("_4_up")
    # 将所有x轴中的数据转换成字符串,从而绘图

    for key in digital_dict:
        # 使用 map 方法将列表中的元素转换为字符串
        digital_dict[key][0] = list(map(str, digital_dict[key][0]))
    opts = InitOpts(width="1920px", height="1080px", theme="white")

    # 1. up 5星出卡时抽数的频数分布图

    # 创建折线图
    up5_num = Line(opts)
    xaxis = digital_dict["up_5"][0]
    yaxis = digital_dict["up_5"][1]
    # 添加x轴数据：被抽取的对象，y轴数据
    up5_num.add_xaxis(xaxis)
    up5_num.add_yaxis("在第n抽出up的频数", yaxis, is_smooth=True)

    # 配置全局信息
    up5_num.set_global_opts(
        title_opts=TitleOpts(
            title="up 5星出卡时抽数的频数分布图", pos_left="center", pos_bottom="0%"
        ),
        legend_opts=LegendOpts(is_show=True),
        # 转换折线图和柱状图
        toolbox_opts=ToolboxOpts(is_show=True),
        visualmap_opts=VisualMapOpts(
            dimension=0,
            is_show=True,
            is_piecewise=True,
            pieces=[
                {"min": 1, "max": 49, "label": "1~50", "color": "#40AAEA"},
                {"min": 50, "max": 99, "label": "50~100", "color": "#29CF31"},
                {"min": 100, "max": 150, "label": "100~150", "color": "#ECA647"},
                {
                    "min": 150,
                    "max": 160,
                    "label": "150~160",
                    "color": "#EC8147",
                },  # 这里必须上下数据重复才不会间断，weird
                {
                    "min": 160,
                    "max": 180,
                    "label": "只因你实在是太霉(160 >)",
                    "color": "#C70039",
                },
            ],
        ),
    )

    path = get_output_file("1. up 5星出卡时抽数的频数分布图.html")
    up5_num.render(path)

    # 2. up 5五星的抽取次数分布(占比)

    # 创建折线图
    up_5_pc = Line(opts)
    xaxis = digital_dict["up_5_pc"][0]
    yaxis = digital_dict["up_5_pc"][1]
    # 添加x轴数据：被抽取的对象，y轴数据
    up_5_pc.add_xaxis(xaxis)
    up_5_pc.add_yaxis("落在第n抽概率", yaxis, is_smooth=True)

    # 使数据显示百分比
    up_5_pc.set_series_opts(
        label_opts=LabelOpts(
            formatter=JsCode("function (params) {return params.value[1] + '%'}")
        )
    )

    # 配置全局信息
    up_5_pc.set_global_opts(
        title_opts=TitleOpts(
            title="up 5星出卡时抽数分布图", pos_left="center", pos_bottom="0%"
        ),
        legend_opts=LegendOpts(is_show=True),
        # 转换折线图和柱状图
        toolbox_opts=ToolboxOpts(is_show=True),
        yaxis_opts=AxisOpts(axislabel_opts=LabelOpts(formatter="{value} %")),
        visualmap_opts=VisualMapOpts(
            dimension=0,
            is_show=True,
            is_piecewise=True,
            pieces=[
                {"min": 1, "max": 49, "label": "1~49", "color": "#40AAEA"},
                {"min": 50, "max": 100, "label": "50~99", "color": "#29CF31"},
                {"min": 100, "max": 149, "label": "100~149", "color": "#ECA647"},
                {"min": 149, "max": 160, "label": "149~160", "color": "#EC8147"},
                {
                    "min": 160,
                    "label": "只因你实在是太霉(160 >)",
                    "color": "#C70039",
                },
            ],
        ),
    )
    # 绘图
    path = get_output_file("2. up 5星出卡时抽数分布图(占比).html")
    up_5_pc.render(path)

    # "up_5_lj": 出限定五星的累计概率
    # 3. up 5星每抽的累进概率图

    # 创建折线图
    up5_lj = Line(opts)
    xaxis = digital_dict["up_5_lj"][0]
    yaxis = digital_dict["up_5_lj"][1]
    # 添加x轴数据：被抽取的对象，y轴数据
    up5_lj.add_xaxis(xaxis)
    up5_lj.add_yaxis(
        "在第n抽时的累进概率",
        yaxis,
        is_smooth=True,
        label_opts=LabelOpts(is_show=False),
    )

    # 使数据显示百分比
    up5_lj.set_series_opts(
        label_opts=LabelOpts(
            formatter=JsCode("function (params) {return params.value[1] + '%'}")
        )
    )

    # 配置全局信息
    up5_lj.set_global_opts(
        title_opts=TitleOpts(
            title="up 5星出卡时抽数的频数分布图", pos_left="center", pos_bottom="0%"
        ),
        legend_opts=LegendOpts(is_show=True),
        # 转换折线图和柱状图
        toolbox_opts=ToolboxOpts(is_show=True),
        yaxis_opts=AxisOpts(axislabel_opts=LabelOpts(formatter="{value} %")),
        visualmap_opts=VisualMapOpts(is_show=True),
    )

    path = get_output_file("3. up 5星出现的累进概率图.html")
    up5_lj.render(path)

    # 4. 5星出卡时抽数的频数分布图:  "_5"

    # 创建折线图
    _5_num = Line(opts)
    xaxis = digital_dict["_5"][0]
    yaxis = digital_dict["_5"][1]
    # 添加x轴数据：被抽取的对象，y轴数据
    _5_num.add_xaxis(xaxis)
    _5_num.add_yaxis("在第n抽出金的频数", yaxis, is_smooth=True)

    # 配置全局信息
    _5_num.set_global_opts(
        title_opts=TitleOpts(
            title="5星出卡时抽数的频数分布图", pos_left="center", pos_bottom="0%"
        ),
        legend_opts=LegendOpts(is_show=True),
        # 转换折线图和柱状图
        toolbox_opts=ToolboxOpts(is_show=True),
        visualmap_opts=VisualMapOpts(
            dimension=0,
            is_show=True,
            is_piecewise=True,
            pieces=[
                {"min": 1, "max": 74, "label": "1~73", "color": "#29CF31"},
                {"min": 74, "max": 80, "label": "74~79", "color": "#ECA647"},
                {"min": 80, "max": 85, "label": "80~85", "color": "#EC8147"},
                {"min": 86, "label": "只因你实在是太霉(> 85)", "color": "#C70039"},
            ],
        ),
    )

    path = get_output_file("4. 5星出卡时抽数的频数分布图.html")
    _5_num.render(path)

    # 5. 5五星的抽取次数分布(占比)  _5_pc

    # 创建折线图
    _5_pc = Line(opts)
    xaxis = digital_dict["_5_pc"][0]
    yaxis = digital_dict["_5_pc"][1]
    # 添加x轴数据：被抽取的对象，y轴数据
    _5_pc.add_xaxis(xaxis)
    _5_pc.add_yaxis(
        "落在第n抽的概率",
        yaxis,
        is_smooth=True,
        label_opts=LabelOpts(is_show=False),
    )

    # 使数据显示百分比
    _5_pc.set_series_opts(
        label_opts=LabelOpts(
            formatter=JsCode("function (params) {return params.value[1] + '%'}")
        )
    )

    # 配置全局信息
    _5_pc.set_global_opts(
        title_opts=TitleOpts(
            title="5星出卡时抽数分布图", pos_left="center", pos_bottom="0%"
        ),
        legend_opts=LegendOpts(is_show=True),
        # 转换折线图和柱状图
        toolbox_opts=ToolboxOpts(is_show=True),
        yaxis_opts=AxisOpts(axislabel_opts=LabelOpts(formatter="{value} %")),
        visualmap_opts=VisualMapOpts(
            dimension=0,
            is_show=True,
            is_piecewise=True,
            pieces=[
                {"min": 1, "max": 74, "label": "1~73", "color": "#29CF31"},
                {"min": 74, "max": 80, "label": "74~79", "color": "#ECA647"},
                {"min": 80, "max": 86, "label": "80~85", "color": "#EC8147"},
                {"min": 86, "label": "只因你实在是太霉(> 85)", "color": "#C70039"},
            ],
        ),
    )

    path = get_output_file("5. 5星出卡时抽数分布图(占比).html")
    _5_pc.render(path)

    # 6. 5星每抽的累进概率图  _5_lj

    # 创建折线图
    _5_lj = Line(opts)
    xaxis = digital_dict["_5_lj"][0]
    yaxis = digital_dict["_5_lj"][1]
    # 添加x轴数据：被抽取的对象，y轴数据
    _5_lj.add_xaxis(xaxis)
    _5_lj.add_yaxis(
        "落在第n抽的累进概率",
        yaxis,
        is_smooth=True,
        label_opts=LabelOpts(is_show=False),
    )

    # 使数据显示百分比
    _5_lj.set_series_opts(
        label_opts=LabelOpts(
            formatter=JsCode("function (params) {return params.value[1] + '%'}")
        )
    )

    # 配置全局信息
    _5_lj.set_global_opts(
        title_opts=TitleOpts(
            title="5星每抽的累进概率", pos_left="center", pos_bottom="0%"
        ),
        legend_opts=LegendOpts(is_show=True),
        yaxis_opts=AxisOpts(axislabel_opts=LabelOpts(formatter="{value} %")),
        # 转换折线图和柱状图
        toolbox_opts=ToolboxOpts(is_show=True),
        visualmap_opts=VisualMapOpts(
            dimension=0,
            is_show=True,
            is_piecewise=True,
            pieces=[
                {"min": 0, "max": 74, "label": "1~74", "color": "#29CF31"},
                {"min": 74, "max": 80, "label": "74~79", "color": "#ECA647"},
                {"min": 80, "max": 86, "label": "80~85", "color": "#EC8147"},
                {"min": 86, "label": "只因你实在是太霉(> 85)", "color": "#C70039"},
            ],
        ),
    )

    path = get_output_file("6. 5星每抽的累进概率图(占比).html")
    _5_lj.render(path)

    # 7. up 4星每抽出现的占比图 _4_pc

    # 创建折线图
    _4_pc = Line(opts)
    xaxis = digital_dict["_4_pc"][0]
    yaxis1 = digital_dict["_4_pc"][1]
    yaxis2 = digital_dict["_4_pc"][2]
    yaxis3 = digital_dict["_4_pc"][3]
    # 添加x轴数据：被抽取的对象，y轴数据
    _4_pc.add_xaxis(xaxis)
    _4_pc.add_yaxis("4星up1每抽出现的占比", yaxis1)
    _4_pc.add_yaxis("4星up2每抽出现的占比", yaxis2)
    _4_pc.add_yaxis("4星up3每抽出现的占比", yaxis3)

    _4_pc.set_series_opts(
        label_opts=LabelOpts(
            formatter=JsCode("function (params) {return params.value[1] + '%'}")
        )
    )
    # 配置全局信息
    _4_pc.set_global_opts(
        title_opts=TitleOpts(
            title="up 4星每抽出现的占比图", pos_left="center", pos_bottom="0%"
        ),
        legend_opts=LegendOpts(is_show=True),
        # 转换折线图和柱状图
        toolbox_opts=ToolboxOpts(is_show=True),
        yaxis_opts=AxisOpts(axislabel_opts=LabelOpts(formatter="{value} %")),
    )

    path = get_output_file("7. up 4星每抽出现的占比图.html")
    _4_pc.render(path)

    # 8. up 4星在第n抽的累进概率图 _4_lj_sum

    # 创建折线图
    _4_lj_sum = Line(opts)
    xaxis = digital_dict["_4_lj_sum"][0]
    yaxis = digital_dict["_4_lj_sum"][1]

    # 添加x轴数据：被抽取的对象，y轴数据
    _4_lj_sum.add_xaxis(xaxis)
    _4_lj_sum.add_yaxis(
        "up 4星在第n抽的累进概率", yaxis, label_opts=LabelOpts(is_show=True)
    )

    _4_lj_sum.set_series_opts(
        label_opts=LabelOpts(
            formatter=JsCode("function (params) {return params.value[1] + '%'}")
        )
    )
    # 配置全局信息
    _4_lj_sum.set_global_opts(
        title_opts=TitleOpts(
            title="up 4星每抽出现的占比图", pos_left="center", pos_bottom="0%"
        ),
        legend_opts=LegendOpts(is_show=True),
        # 转换折线图和柱状图
        toolbox_opts=ToolboxOpts(is_show=True),
        yaxis_opts=AxisOpts(axislabel_opts=LabelOpts(formatter="{value} %")),
        visualmap_opts=VisualMapOpts(is_show=True),
    )

    path = get_output_file("8. up 4星在第n抽的累进概率图.html")
    _4_lj_sum.render(path)


if __name__ == "__main__":
    draw_pic()
