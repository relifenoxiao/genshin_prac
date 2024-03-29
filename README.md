
# 原神抽卡全过程模拟及其其结果可视化

## 动机

前些阶段，略微学习了python以及基于pyecharts的数据可视化，正好缺乏练习。  

~~由于我的数学功底不行,~~ 🤣
我没法通过数学方法计算出带有保底的前提下原神出卡的期望值.  
但是我正好学习了上述的技能，所以我刚好准备借此机会来练手。

## 结果

### 图表部分

最终绘图结果如下:

1. up_5星出卡时抽数的频数分布图
2. up_5五星的抽取次数分布(占比)
3. up_5星出现的累进概率图
4. 5星出卡时抽数的频数分布图
5. 5五星的抽取次数分布(占比)
6. 5星每抽的累进概率图
7. up_4星每抽出现的占比分布图
8. up_4星在每一抽的累进概率图

文件存放在`result`文件夹中  
tip. 值得一提的是，图表中的颜色没有任何数学意义，只是我为了练习和好看设置的。

### [数值部分]

具体见: [文章](result.md)

此外，也有大佬通过数学方法计算了相关内容。  
以及还提出了一些有趣的内容，例如欧气值的计算。感兴趣的可以去[看看](https://zhuanlan.zhihu.com/p/522246996)

## 参考资料

抽卡概率的设定来自文章：[这就是抽卡机制？](https://m.miyoushe.com/ys?channel=miyousheluodi/#/article/40811276)  

我个人对于规则详细总结参见:[文章](result.md)

## issue

我在使用pyecharts的set_global_opts的时候发现visualmap_opts，中用prices指定上下限的范围会发生浮动。
具体来说例如：`"min": 1, "max": 49`。此时运行,从结果上来看所指范围是`"1 or 2 ~ 49 or 50 or 51"`这个bug在有些图里出现有些又没有.
这个bug是我把运行结果用 `simplejson` 转换成json再去读取它之后出现的.  
