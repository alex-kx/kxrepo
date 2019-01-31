import copy
import math
class 运行策略:
	def __init__(self, 设备列表, 数据, time, 发电机总满负荷运行小时数):

		self.发电机总满负荷运行小时数 = 发电机总满负荷运行小时数
		self.数据 = 数据
		蒸汽负荷 = self.数据.数据索引['蒸汽负荷'][time]
		self.设备产蒸汽量方案列表 = []
		self.设备供蒸汽方案(数据, 蒸汽负荷, 设备列表, time = time)
		self.优化函数(self.设备产蒸汽量方案列表, 设备列表, time = time)



	def 设备供蒸汽方案(self, 数据, 蒸汽负荷, 设备列表, time):
		发电机台数 = 0
		燃气锅炉列表 = []
		发电机列表 = []
		for 设备 in 设备列表:
			if 设备.名称 == '燃气轮机' or 设备.名称 == '燃气内燃机':
				发电机台数 += 1
				发电机列表.append(设备)
			elif 设备.名称 == '燃气锅炉':
				燃气锅炉列表.append(设备)

		if 发电机台数 == 0:
			self.发电机产蒸汽量方案列表 = []
		else:
			蒸汽负荷 = self.数据.数据索引['蒸汽负荷'][time]
			电负荷 = self.数据.数据索引['电负荷'][time]
			发电机 = 设备列表[0]
			电负荷对应的蒸汽产量 = min(电负荷 / 发电机.发电机规模 * 发电机.锅炉额定产汽量, 发电机台数 * 发电机.锅炉额定产汽量)

			self.发电机产蒸汽量方案列表 = [
				[0] * 发电机台数
			]

			已运行小时数 = self.发电机总满负荷运行小时数 / 发电机台数
			if 发电机.名称 == '燃气轮机':
				运行小时数限制 = 数据.数据索引['燃气轮机满负荷运行小时数限制']
			if 发电机.名称 == '燃气内燃机':
				运行小时数限制 = 数据.数据索引['燃气内燃机满负荷运行小时数限制']

			if 已运行小时数 >= 运行小时数限制:
				pass
			else:

				单台产汽量1, 开启台数1 = self.不大于某蒸汽负荷的最大开启方案(蒸汽负荷, 发电机, 发电机台数)
				flag1 = self.设备运行约束(开启台数1, 单台产汽量1, 发电机, time)
				if flag1 is True and 单台产汽量1 > 0:
					self.发电机产蒸汽量方案列表.append([单台产汽量1] * 开启台数1 + [0] * (发电机台数 - 开启台数1))
				# print('发电机台数', 发电机台数, 单台产汽量1, 开启台数1,'flag1',flag1)

				单台产汽量2, 开启台数2 = self.不大于某蒸汽负荷的最大开启方案(电负荷对应的蒸汽产量, 发电机, 发电机台数)
				flag2 = self.设备运行约束(开启台数2, 单台产汽量2, 发电机, time)
				if flag2 is True and 单台产汽量2 > 0:
					self.发电机产蒸汽量方案列表.append([单台产汽量2] * 开启台数2 + [0] * (发电机台数 - 开启台数2))
				# print(单台产汽量2, 开启台数2,'flag2', flag2)

				单台产汽量3, 开启台数3 = self.不小于某蒸汽负荷的最小开启方案(电负荷对应的蒸汽产量, 发电机, 发电机台数)
				flag3 = self.设备运行约束(开启台数3, 单台产汽量3, 发电机, time)
				if flag3 is True and 单台产汽量3 > 0:
					self.发电机产蒸汽量方案列表.append([单台产汽量3] * 开启台数3 + [0] * (发电机台数 - 开启台数3))
				# print(单台产汽量3, 开启台数3, 'flag3', flag3)



		if self.发电机产蒸汽量方案列表 == []:
			temp_list = []
			待解决蒸汽负荷 = 蒸汽负荷
			for 燃气锅炉 in 燃气锅炉列表:
				if 待解决蒸汽负荷 < 燃气锅炉.锅炉额定产汽量:
					temp_list.append(待解决蒸汽负荷)
					待解决蒸汽负荷 = 0
				else:
					temp_list.append(燃气锅炉.锅炉额定产汽量)
					待解决蒸汽负荷 -= 燃气锅炉.锅炉额定产汽量
			self.设备产蒸汽量方案列表.append(temp_list)

		else:
			for 发电机产蒸汽量方案 in self.发电机产蒸汽量方案列表:
				发电机发电总产汽量 = sum(发电机产蒸汽量方案)
				待解决蒸汽负荷 = 蒸汽负荷 - 发电机发电总产汽量
				temp_list = []
				for 燃气锅炉 in 燃气锅炉列表:


					if 待解决蒸汽负荷 < 燃气锅炉.锅炉额定产汽量:
						temp_list.append(待解决蒸汽负荷)
						待解决蒸汽负荷 = 0
					else:
						temp_list.append(燃气锅炉.锅炉额定产汽量)
						待解决蒸汽负荷 -= 燃气锅炉.锅炉额定产汽量
				self.设备产蒸汽量方案列表.append(发电机产蒸汽量方案 + temp_list)


	def 设备运行约束(self, 开启台数, 单台产汽量, 发电机, time):
		产汽量 = 开启台数 * 单台产汽量
		flag = True
		if 产汽量 > self.数据.数据索引['蒸汽负荷'][time]:
			flag = False
		elif self.数据.数据索引['并网模式'] == '自发自用':
			if 单台产汽量 / 发电机.锅炉额定产汽量 * 发电机.发电机规模 * 开启台数  > self.数据.数据索引['电负荷'][time]:
				flag = False
		return flag

	def 不大于某蒸汽负荷的最大开启方案(self, 某蒸汽负荷, 设备, 发电机台数):
		if 设备.名称 == '燃气轮机':
			最小开启比例 = self.数据.数据索引['燃气轮机最低运行负荷比例']
		if 设备.名称 == '燃气内燃机':
			最小开启比例 = self.数据.数据索引['燃气内燃机最低运行负荷比例']

		for i in range(发电机台数):
			发电机开启台数 = i + 1
			if 某蒸汽负荷 >= 发电机开启台数 * 最小开启比例 * 设备.锅炉额定产汽量 and 某蒸汽负荷 <= 发电机开启台数 * 设备.锅炉额定产汽量:
				return (某蒸汽负荷 / 发电机开启台数, 发电机开启台数)

		开启台数 = min(int(某蒸汽负荷 / 设备.锅炉额定产汽量), 发电机台数)
		return (设备.锅炉额定产汽量, 开启台数)

	def 不小于某蒸汽负荷的最小开启方案(self, 某蒸汽负荷, 设备, 发电机台数):
		if 设备.名称 == '燃气轮机':
			最小开启比例 = self.数据.数据索引['燃气轮机最低运行负荷比例']
		if 设备.名称 == '燃气内燃机':
			最小开启比例 = self.数据.数据索引['燃气内燃机最低运行负荷比例']

		for i in range(发电机台数):
			发电机开启台数 = i + 1
			if 某蒸汽负荷 >= 发电机开启台数 * 最小开启比例 * 设备.锅炉额定产汽量 and 某蒸汽负荷 <= 发电机开启台数 * 设备.锅炉额定产汽量:
				return (某蒸汽负荷 / 发电机开启台数, 发电机开启台数)

		开启台数 = min(int(某蒸汽负荷 / (设备.锅炉额定产汽量 * 最小开启比例)), 发电机台数)
		return (设备.锅炉额定产汽量 * 最小开启比例, 开启台数)

	def 目标函数(self, 设备列表, 产蒸汽方案, time):
		燃气成本 = 0
		自耗电成本 = 0
		水成本 = 0
		蒸汽收入 = 0
		供电收入 = 0
		总发电量 = 0
		for i, 设备 in enumerate(设备列表):
			发电量 = 产蒸汽方案[i] * (设备.发电机规模 / 设备.锅炉额定产汽量)
			总发电量 += 发电量

			燃气成本 += 产蒸汽方案[i] * (设备.额定耗气量 / 设备.锅炉额定产汽量) * self.数据.数据索引['燃气价格']
			水成本 += 产蒸汽方案[i] * self.数据.数据索引['水价格'] * 设备.耗水率
			蒸汽收入 += 产蒸汽方案[i] * self.数据.数据索引['蒸汽价格']
			自耗电成本 += (发电量 * 设备.自耗电比例 + 产蒸汽方案[i] * 设备.锅炉单位产汽耗电量) * self.数据.数据索引['市政电价'][time]
		if self.数据.数据索引['并网模式'] == '全额上网':
			供电收入 = 总发电量 * self.数据.数据索引['上网电价'][time]
		elif self.数据.数据索引['并网模式'] == '自发自用':
			供电收入 = 总发电量 * self.数据.数据索引['内部售电价'][time]
		elif self.数据.数据索引['并网模式'] == '自发自用余电上网':
			自发自用电量 = min(self.数据.数据索引['电负荷'][time], 总发电量)
			上网电量 = 总发电量 - 自发自用电量
			供电收入 = 自发自用电量 * self.数据.数据索引['内部售电价'][time] + 上网电量 * self.数据.数据索引['上网电价'][time]

		运行收益 = 蒸汽收入 + 供电收入 - 燃气成本 - 自耗电成本 - 水成本
		return 运行收益

	def 优化函数(self, 设备产蒸汽量方案列表, 设备列表, time):
		self.opt_value = -10000000
		for 产蒸汽方案 in 设备产蒸汽量方案列表:
			运行收益 = self.目标函数(设备列表 = 设备列表, 产蒸汽方案 = 产蒸汽方案, time=time)
			if 运行收益 > self.opt_value:
				self.opt_value = 运行收益
				self.opt_产蒸汽方案 = 产蒸汽方案

