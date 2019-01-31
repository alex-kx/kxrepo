from .Data import 数据类
from .Technology_base import 技术路线类

class 燃气锅炉类(技术路线类):
    def __init__(self ,名称,数据, 锅炉额定产汽量=0):
        super().__init__(名称, 数据, 锅炉额定产汽量)
        self.是否为备用锅炉 = False
        self.厂家型号 = ''
        self.耗水率 = self.数据.数据索引['锅炉耗水率']
        self.满负荷运行小时数限制 = self.数据.数据索引['燃气锅炉满负荷运行小时数限制']
        self.锅炉单位产汽耗电量 = self.数据.数据索引['燃气锅炉单位产汽耗电量']
        self.锅炉效率 = self.数据.数据索引['燃气锅炉效率']
        self.最低产汽运行负荷 = self.锅炉额定产汽量 * self.数据.数据索引['燃气锅炉最低运行负荷比例']
        self.安装费占设备费比例 = self.数据.数据索引['其他工艺安装费占设备费比例']
        self.锅炉单位造价 = self.数据.数据索引['燃气锅炉单位造价']
        self.计算额定耗气量()

    def 计算设备价格(self):
        self.设备价格 = self.锅炉单位造价 * self.锅炉额定产汽量

    def 计算额定耗气量(self):
        self.额定耗气量 = (self.数据.数据索引['水蒸气焓差'] * self.锅炉额定产汽量 * 1000) / (self.锅炉效率 * self.数据.数据索引['燃气热值'] * 4.186)

    # 设备安装费计算待进一步完善
    def 计算设备安装费(self):
        self.设备安装费 = self.设备价格 * self.安装费占设备费比例