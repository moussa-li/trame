import numpy as np
import matplotlib.pyplot as plt
import csv

from trame.app import get_server
from trame.widgets import trame, matplotlib
from trame_vuetify.widgets import vuetify


__all__ = [
    "RightWidget"
]

def DotsandPoints():
    fig, ax = plt.subplots()
    example = open('.\work_dir\\right\curveData.csv')
    exampleReader = csv.reader(example)
    exampleData = list(exampleReader)
    length_zu = len(exampleData)
    length_yuan = len(exampleData[0])  # 得到每行长度
    data = list()
    for i in range(0, length_zu):  # 从第1行开始读取
        data.append(float(exampleData[i][0]))
    ax.plot(
        data,
        "-o",
        alpha=0.5,
        color="black",
        linewidth=5,
        markerfacecolor="green",
        markeredgecolor="lightgreen",
        markersize=20,
        markeredgewidth=10,
    )
    ax.grid(True, color="#EEEEEE", linestyle="solid")
    ax.set_xlim(-2, 22)
    ax.set_ylim(-0.1, 1.1)

    return fig

class RightWidget:
	def __init__(self, container, ):
		with container:
			html_figure = matplotlib.Figure(style="height:100%;")
			html_figure.update(DotsandPoints())