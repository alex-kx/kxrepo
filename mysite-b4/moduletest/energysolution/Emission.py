class 节能减排指标类():
	def  __init__(self, 燃气锅炉耗气量 = 0, 燃气轮机耗气量 = 0, 燃气内燃机耗气量 = 0, 总耗气量 = 0):
		self.售电量 = 2781.346

		self.供电煤耗 = 312
		self.燃气锅炉_耗气量 = 燃气锅炉耗气量/10000
		self.燃气轮机_耗气量 = 燃气轮机耗气量/10000
		self.内燃机_耗气量 = 燃气内燃机耗气量/10000
		self.年合计耗气量 = 总耗气量/10000

		# 电网排放因子计算
		self.CO2电网排放因子 = 0.9489
		self.SO2电网排放因子 = 0.02847
		self.NOX电网排放因子 = 0.01428
		self.粉尘电网排放因子 = 0.0096

		# 过量空气系数的取值
		self.过量空气系数α_燃气锅炉 = 1.200
		self.过量空气系数α_燃气轮机 = 3.500
		self.过量空气系数α_内燃机 = 1.313

		# 下列两个参数的取值需要进一步完善
		self.单位天然气CO2排放量 = 1.8653
		self.单位天然气SO2排放量 = 700

		# NOX指标暂时取为定值
		self.NOX指标_燃气锅炉 = 200
		self.NOX指标_燃气轮机 = 80
		self.NOX指标_内燃机 = 500

		# 脱硝率人为设定?
		self.脱硝率_燃气锅炉 = 0
		self.脱硝率_燃气轮机 = 0
		self.脱硝率_内燃机 = 0

		# 下列参数根据烟气含氧量确定, 需进一步完善
		self.粉尘指标_燃气锅炉 = 20
		self.粉尘指标_燃气轮机 = 6.857
		self.粉尘指标_内燃机 = 18.282


		self.燃气锅炉系统排放量_系统能源消耗量 = 14270.576
		self.燃气锅炉系统排放量_相同基准实际能源消耗量 = 14270.576
		self.燃气锅炉系统排放量_CO2 = 20443.529
		self.燃气锅炉系统排放量_SO2 = 23.677
		self.燃气锅炉系统排放量_NOX = 32.849
		self.燃气锅炉系统排放量_粉尘 = 4.405

		self.计算原煤替代量()
		self.计算电力污染物排放量()
		self.计算天然气排放量()
		self.计算总排放量()
		self.计算能耗污染物排放量()

		print('CO2排放量', self.天然气CO2排放量)
		print('SO2排放量', self.天然气SO2排放量)
		print('NOX排放量', self.天然气NOX排放量)
		print('粉尘排放量', self.天然气粉尘排放量)

	def 计算原煤替代量(self):
		self.用电量 = -1 * self.售电量
		self.折算标准煤 = self.用电量 * self.供电煤耗 / pow(10,6) * pow(10,4)
		self.原煤替代量 = self.折算标准煤 * 7000 / 5500

	def 计算电力污染物排放量(self):
		self.CO2电网排放量 = self.用电量 * self.CO2电网排放因子 * 10
		self.SO2电网排放量 = self.用电量 * self.SO2电网排放因子 * 10
		self.NOX电网排放量 = self.用电量 * self.NOX电网排放因子 * 10
		self.粉尘电网排放量 = self.折算标准煤 * self.粉尘电网排放因子

	def 计算天然气排放量(self):
		# 烟气排放量的计算
		self.燃气锅炉_烟气量 = self.燃气锅炉_耗气量 / 293.15 * 273.15 * (1 + 2 / 0.21 * self.过量空气系数α_燃气锅炉)
		self.燃气轮机_烟气量 = self.燃气轮机_耗气量 / 293.15 * 273.15 * (1 + 2 / 0.21 * self.过量空气系数α_燃气轮机)
		self.内燃机_烟气量 = self.内燃机_耗气量 / 293.15 * 273.15 * (1 + 2 / 0.21 * self.过量空气系数α_内燃机)

		self.烟气总量 = self.燃气锅炉_烟气量 + self.燃气轮机_烟气量
		self.天然气CO2排放量 = self.年合计耗气量  *  self.单位天然气CO2排放量 * 10000 / 1000
		self.天然气SO2排放量 = self.年合计耗气量  *  self.单位天然气SO2排放量 * 10000 / 1000000000
		self.天然气NOX排放量 = (self.燃气锅炉_烟气量 * self.NOX指标_燃气锅炉 * (1 - self.脱硝率_燃气锅炉) + self.燃气轮机_烟气量 *
								self.NOX指标_燃气轮机 * (1 - self.脱硝率_燃气轮机) + self.内燃机_烟气量 * self.NOX指标_内燃机 * (1 - self.脱硝率_内燃机)) * 10000 / 1000000000
		self.天然气粉尘排放量 = (self.燃气锅炉_烟气量 * self.粉尘指标_燃气锅炉 + self.燃气轮机_烟气量 * self.粉尘指标_燃气轮机 + self.内燃机_烟气量
								 * self.粉尘指标_内燃机) * 10000 / 1000000000

	def 计算总排放量(self):
		self.CO2排放总量 = self.CO2电网排放量 + self.天然气CO2排放量
		self.SO2排放总量 = self.SO2电网排放量 + self.天然气SO2排放量
		self.NOX排放总量 = self.NOX电网排放量 + self.天然气NOX排放量
		self.粉尘排放总量 = self.粉尘电网排放量 + self.天然气粉尘排放量

	def f1(self):
		if(self.售电量 > 0):
			message = self.年合计耗气量 * 1.33 * 10
		else:
			message = self.年合计耗气量 * 1.33 * 10 + self.售电量 * (-1) * 0.1229 * 10
		return message

	def f2(self):
		if(self.用电量 > 0):
			message = self.f1()
		else:
			message = self.f1() + self.用电量 * self.供电煤耗 / 1000 * 10
		return message

	def 计算能耗污染物排放量(self):
		self.减排量_系统能源消耗量 = self.燃气锅炉系统排放量_系统能源消耗量 - self.f1()
		self.减排量_相同基准实际能源消耗量 = self.燃气锅炉系统排放量_相同基准实际能源消耗量 - self.f2()
		self.减排量_CO2 = self.燃气锅炉系统排放量_CO2 - self.CO2排放总量
		self.减排量_SO2 = self.燃气锅炉系统排放量_SO2 - self.SO2排放总量
		self.减排量_NOX = self.燃气锅炉系统排放量_NOX - self.NOX排放总量
		self.减排量_粉尘 = self.燃气锅炉系统排放量_粉尘 - self.粉尘排放总量


