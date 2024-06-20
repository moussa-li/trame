from constantsymbol import Constant
from model import Model
import os
import csv
from pathlib import Path

__all__ = [
    "RightModel"
]

class RightModel(Model):
    def __init__(self, server, dir):
        super().__init__(server)
        self.dir = dir

        self.infoGroup = {}
        self.UpdateModel()

    def UpdateModel(self):
        """
        读取dir路径下的文件并更新
        """
        self.infoGroup.clear()
        for root, dirs, files in os.walk(self.dir):
            # 只遍历根目录
            if root != str(self.dir):
                break

            for file in files:
                path = self.dir / file

                # 文件名
                fileName = file.split('.')[0]

                # 文件中的字符串列表
                example = open('.\work_dir\\right\curveData.csv')
                exampleReader = csv.reader(example)
                exampleData = list(exampleReader)
                length_zu = len(exampleData)
                length_yuan = len(exampleData[0])  # 得到每行长度
                data = list()
                for i in range(0, length_zu):  # 从第1行开始读取
                    data.append(float(exampleData[i][0]))

                # 保存
                self.infoGroup[fileName] = data

        # 更新信号
        self.SignalUpdate()