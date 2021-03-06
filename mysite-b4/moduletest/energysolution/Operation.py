from .OperatingStrategy01 import 运行策略


class 全年运行方案:
	def __init__(self, 数据, 设备列表):
		self.数据 = 数据
		self.设备列表 = 设备列表
		self.发电机总满负荷运行小时数 = 0
		self.全年产蒸汽方案 = []
		self.发电机运行列表 = []
		self.发电机发电量列表 = []
		self.燃气锅炉运行列表 = [0] * 8760
		self.备用燃气锅炉运行列表 = [0] * 8760
		self.运行收益列表 = []

		for time in range(8760):
			当前运行策略 = 运行策略(设备列表, 数据, time, self.发电机总满负荷运行小时数)
			最优产蒸汽方案 = 当前运行策略.opt_产蒸汽方案
			self.全年产蒸汽方案.append(最优产蒸汽方案)
			self.运行收益列表.append(当前运行策略.opt_value)
			for i, 设备 in enumerate(设备列表):
				if 设备.名称 == "燃气锅炉":
					if 设备.是否为备用锅炉 == True:
						self.备用燃气锅炉运行列表[time] = 最优产蒸汽方案[i]
					else:
						self.燃气锅炉运行列表[time] = 最优产蒸汽方案[i]
			发电机产汽量 = 0
			发电机发电量 = 0

			for i, 设备 in enumerate(self.设备列表):
				设备.设备实时量['产汽量'][time] = 最优产蒸汽方案[i]
				if 设备.名称 == '燃气轮机' or 设备.名称 == '燃气内燃机':
					self.发电机总满负荷运行小时数 += 设备.设备实时量['产汽量'][time] / 设备.锅炉额定产汽量
					发电机产汽量 += 设备.设备实时量['产汽量'][time]
					发电机发电量 += 设备.设备实时量['产汽量'][time] / 设备.锅炉额定产汽量 * 设备.发电机规模
			self.发电机运行列表.append(发电机产汽量)
			self.发电机发电量列表.append(发电机发电量)

		self.生成全年运行情况列表()

	def 生成全年运行情况列表(self):
		发电机发电量列表 = self.发电机发电量列表
		发电机运行列表 = self.发电机运行列表
		燃气锅炉运行列表 = self.燃气锅炉运行列表
		备用燃气锅炉运行列表 = self.备用燃气锅炉运行列表
		运行收益列表 = self.运行收益列表

		for i in range(8760):
			self.数据.数据索引['蒸汽负荷'][i] = round(self.数据.数据索引['蒸汽负荷'][i], 2)
			发电机发电量列表[i] = round(发电机发电量列表[i], 2)
			发电机运行列表[i] = round(发电机运行列表[i], 2)
			燃气锅炉运行列表[i] = round(燃气锅炉运行列表[i], 2)
			备用燃气锅炉运行列表[i] = round(备用燃气锅炉运行列表[i], 2)
			运行收益列表[i] = round(运行收益列表[i], 2)

		时刻列表 = [i + 1 for i in range(8760)]
		self.全年运行情况列表 = zip(时刻列表, self.数据.数据索引['蒸汽负荷'], self.数据.数据索引['电负荷'], 发电机发电量列表, self.数据.数据索引['市政电价'],
							self.数据.数据索引['上网电价'], self.数据.数据索引['内部售电价'], 发电机运行列表,
							燃气锅炉运行列表, 备用燃气锅炉运行列表, 运行收益列表)