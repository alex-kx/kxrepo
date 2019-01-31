from .Steam_solutions import 供蒸汽方案
from .Sample import 设备样本类
from .Machine_factory import 设备对象工厂
from .Configuration_combinations import 配置组合类

class 量化筛选类:
	def __init__(self, 数据):

		self.数据 = 数据
		self.设备样本库 = 设备样本类(self.数据)
		self.技术路线列表 = self.数据.数据索引['技术路线列表']
		self.蒸汽负荷峰值 = max(self.数据.数据索引['蒸汽负荷'])
		self.配置组合 = 配置组合类(数据, self.蒸汽负荷峰值, self.技术路线列表)
		self.配置方案列表 = self.配置组合.配置方案列表
		self.方案列表 = []
		self.生成供蒸汽方案()

	def 生成供蒸汽方案(self):
		for 设备配置 in self.配置方案列表:
			设备列表 = []
			for 设备样本 in 设备配置:
				if 设备样本['锅炉额定产汽量'] > 0:
					设备 = 设备对象工厂(self.数据, 设备样本)
					设备列表.append(设备)
			if len(设备列表) > 1:
				设备列表[-1].是否备用锅炉 = True
			方案 = 供蒸汽方案(self.数据, 设备列表)
			self.方案列表.append(方案)

