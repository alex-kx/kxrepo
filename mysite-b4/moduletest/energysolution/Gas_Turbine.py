from .Data import 数据类
from .Technology_base import 技术路线类

class 燃气轮机类(技术路线类):
    def __init__(self ,名称, 数据, 燃气轮机样本, 锅炉额定产汽量=0, 额定制冷量=0):
        super().__init__(名称, 数据, 锅炉额定产汽量, 额定制冷量)
        
        self.燃气轮机样本 = 燃气轮机样本
        self.厂家型号 = self.燃气轮机样本['公司型号']
        self.发电效率 = self.燃气轮机样本['发电效率']
        self.发电机规模 = self.燃气轮机样本['发电功率']
        self.未修正前发电机规模 = self.发电机规模 / self.数据.数据索引['燃气轮机发电功率修正']
        self.烟气热量 = self.燃气轮机样本['烟气热量']
        self.剩余余热可产汽量 = [self.锅炉额定产汽量 for i in range(8760)]
        self.单位制冷耗蒸汽量 = (3600 / self.数据.数据索引['蒸汽型溴冷机COP']) / (self.数据.数据索引['水蒸气焓差'] * 1000)

        self.自耗电比例 = self.数据.数据索引['燃气轮机自耗电比例']
        self.耗水率 = self.数据.数据索引['锅炉耗水率']
        self.满负荷运行小时数限制 = self.数据.数据索引['燃气轮机满负荷运行小时数限制']
        self.锅炉单位产汽耗电量 = self.数据.数据索引['余热锅炉单位产汽耗电量']
        self.锅炉效率 = self.数据.数据索引['余热锅炉效率']
        # self.发电机单位造价 = self.数据.数据索引['燃气轮机单位造价']
        self.发电机单位造价 = self.确定燃气轮机单位造价()
        self.锅炉单位造价 = self.数据.数据索引['余热锅炉单位造价']
        self.COP = self.数据.数据索引['溴冷机COP']
        self.制冷机单位造价 = self.数据.数据索引['溴冷机单位造价']
        self.单位制冷耗电量 = self.数据.数据索引['溴冷机单位制冷耗电量']
        self.最低产汽运行负荷 = self.锅炉额定产汽量 * self.数据.数据索引['燃气轮机最低运行负荷比例']
        self.最低制冷运行负荷 = self.额定制冷量 * self.数据.数据索引['燃气轮机最低运行负荷比例']

        self.余热锅炉装机规模 = 0
        self.溴冷机装机规模 = 0

        self.计算额定耗气量()

    def 确定燃气轮机单位造价(self):
        燃气轮机造价 = 0
        if self.未修正前发电机规模 <= 6350:
            燃气轮机造价 = 5000
        elif self.未修正前发电机规模 <= 7900:
            燃气轮机造价 = 4800
        elif self.未修正前发电机规模 <= 10000:
            燃气轮机造价 = 4000
        elif self.未修正前发电机规模 <= 15000:
            燃气轮机造价 = 3650
        elif self.未修正前发电机规模 <= 20000:
            燃气轮机造价 = 3500
        elif self.未修正前发电机规模 <= 30000:
            燃气轮机造价 = 3300
        else:
            燃气轮机造价 = 3000
        return 燃气轮机造价


    def 计算额定耗气量(self):
        self.额定耗气量 = self.发电机规模 / self.发电效率 * 3600 / (self.数据.数据索引['燃气热值'] * 4.186)

    def 计算设备价格(self):
        self.设备价格 = self.发电机单位造价 * self.未修正前发电机规模 + self.锅炉单位造价 * self.余热锅炉装机规模 + self.溴冷机装机规模 * self.制冷机单位造价

    # 设备安装费计算待进一步完善
    def 计算设备安装费(self):
        self.设备安装费 = self.发电机单位造价 * self.未修正前发电机规模 * self.数据.数据索引['燃气轮机安装费占设备费比例'] + (self.锅炉单位造价 * self.余热锅炉装机规模 + self.溴冷机装机规模 * self.制冷机单位造价) * self.数据.数据索引['其他工艺安装费占设备费比例']

