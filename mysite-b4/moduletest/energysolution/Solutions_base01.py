import operator
from .Investment_assessment import 投资估算类
from .economic import 技经计算类
from .Emission import 节能减排指标类
from .Operation import 全年运行方案
from .Input_Output import 能源投入产出类

class 能源解决方案类:
	def __init__(self, 数据,设备列表):
		self.数据 = 数据
		self.设备列表 = 设备列表
		self.系统实时量 = dict()
		self.系统全年量 = dict()
		self.发电机总满负荷运行小时数 = 0
		self.投入产出量索引列表 = ['发电量', '产汽量', '制冷量', '自耗电量', '耗气量', '耗水量']
		self.能源购售量索引列表 = ['售汽量', '售电量', '外购电量']

		# 成本收入

		# 设备价格及安装费
		self.总设备价格 = 0
		self.总设备安装费 = 0
		self.发电机设备及安装投资 = 0

		self.燃气轮机发电量 = 0
		self.燃气内燃机发电量 = 0

		self.是否有电力接入费 = False

	def 执行计算过程(self):
		self.生成方案标识字符串()
		self.全年运行方案 = 全年运行方案(self.数据, self.设备列表)
		self.能源投入产出  = 能源投入产出类(self.数据, self.设备列表)
		self.计算等效满负荷运行小时数()
		self.成本收入索引 = self.能源投入产出.成本收入索引
		self.系统实时量 = self.能源投入产出.系统实时量
		self.系统全年量 = self.能源投入产出.系统全年量
		self.计算设备及安装费用()
		self.计算发电机设备发电量()

		# 投资估算
		self.判断是否有电力接入费()
		self.投资估算 = 投资估算类(热力系统总设备价格 = self.总设备价格, 热力系统总设备安装费 = self.总设备安装费, 数据 = self.数据, 是否有电力接入费 = self.是否有电力接入费)

		self.计算维修费用()

		# 指标
		self.技经计算 = 技经计算类(
			数据 = self.数据,
			成本收入索引 = self.成本收入索引,
			工程费用索引 = self.投资估算.工程费用索引,
			工程建设其他费用索引 = self.投资估算.工程建设其他费用索引,
			基本预备费 = self.投资估算.基本预备费,
			收购费用 = self.投资估算.收购费用,
			建设投资 = self.投资估算.建设投资,
			维修费 = self.维修费_全年量,
		)
		kwargs1 = dict()
		kwargs1['总耗气量'] = self.系统全年量['耗气量']
		for 设备 in self.设备列表:
			try:
				kwargs1[设备.名称 + '耗气量'] += 设备.设备全年量['耗气量']
			except KeyError:
				kwargs1[设备.名称 + '耗气量'] = 设备.设备全年量['耗气量']
		self.排放量 = 节能减排指标类(**kwargs1)
		self.生成指标索引()
		self.生成结果列表()

	def 计算等效满负荷运行小时数(self):
		for time in range(8760):
			for 设备 in self.设备列表:
				设备.满负荷运行小时数 += 设备.设备实时量['产汽量'][time] / 设备.锅炉额定产汽量

		self.满负荷运行小时数listStr = ''
		for 设备 in self.设备列表:
			self.满负荷运行小时数listStr += 设备.名称 + ':' + str(int(设备.满负荷运行小时数)) + '(h)' + '; '



	def 判断是否有电力接入费(self):
		for 设备 in self.设备列表:
			if 设备.名称 == '燃气轮机' or 设备.名称 == '燃气内燃机':
				self.是否有电力接入费 = True


	def 计算设备及安装费用(self):
		for 设备 in self.设备列表:
			设备.计算设备价格()
			设备.计算设备安装费()
			self.总设备价格 += 设备.设备价格
			self.总设备安装费 += 设备.设备安装费

	def 计算发电机设备发电量(self):
		for 设备 in self.设备列表:
			if 设备.名称 == '燃气轮机':
				self.燃气轮机发电量 += 设备.设备全年量['发电量']
			elif 设备.名称 == '燃气内燃机':
				self.燃气内燃机发电量 += 设备.设备全年量['发电量']


	def 计算发电机设备及安装投资(self):
		for 设备 in self.设备列表:
			if 设备.名称 == '燃气轮机':
				self.发电机设备及安装投资 += (设备.设备价格 + 设备.设备安装费)
			elif 设备.名称 == '燃气内燃机':
				self.发电机设备及安装投资 += (设备.设备价格 + 设备.设备安装费)

	def 计算维修费用(self):
		发电机设备及安装投资 = self.总设备价格 + self.总设备安装费
		热力系统工程投资 = self.投资估算.热力系统['总值']
		辅助设施投资 = self.投资估算.辅助设施['总值']
		电力工程系统投资 = self.投资估算.工程费用索引['电气系统']['总值']
		智能控制系统 = self.投资估算.工程费用索引['自控系统']['总值']
		管网投资 = self.投资估算.工程费用索引['室外管网']['总值']
		燃气轮机发电量 = self.燃气轮机发电量
		燃气内燃机发电量 =self.燃气内燃机发电量

		除发电机以外热力系统投资 = 热力系统工程投资 - 发电机设备及安装投资
		self.维修费_全年量 = (
			除发电机以外热力系统投资 * self.数据.数据索引['其他工艺设备维修费占比']
			+ 辅助设施投资 * self.数据.数据索引['辅助设施维修费占比']
			+ 电力工程系统投资 * self.数据.数据索引['电气工程维修费占比']
			+ 智能控制系统 * self.数据.数据索引['智能控制系统维修费占比']
			+ 管网投资 * self.数据.数据索引['管网维修费占比']
			+ 燃气轮机发电量 * self.数据.数据索引['燃气轮机单位发电维修费']
			+ 燃气内燃机发电量 * self.数据.数据索引['燃气内燃机单位发电维修费']
		)

	def 生成方案标识字符串(self):
		self.方案标识 = ''
		for 设备 in self.设备列表:
			if 设备.名称 == '燃气轮机':
				self.方案标识 += 'GT' + ':' + str(int(设备.未修正前发电机规模)) + 'kW '
			elif 设备.名称 == '燃气内燃机':
				self.方案标识 += 'IE' + ':' + str(int(设备.发电机规模)) + 'kW '
			elif 设备.产蒸汽 is True:
				self.方案标识 += 设备.名称 + ':' + str(round(设备.锅炉额定产汽量,1)) + 't/h '
			else:
				self.方案标识 += 设备.名称 + ':' + str(int(设备.额定制冷量)) + 'kW '

		self.设备配置str = []
		self.设备配置string = ""

		for i, 设备 in enumerate(self.设备列表):
			if 设备.名称 == '燃气轮机':
				temp_str = str(int(设备.未修正前发电机规模)) + 'kW ' + 设备.名称 + '(' + 设备.厂家型号 + ')' \
						   + ' 余热锅炉产汽量: ' + str(round(设备.锅炉额定产汽量, 2)) + 't/h' + ';'
				self.设备配置str.append(temp_str)
				self.设备配置string += temp_str

			if 设备.名称 == '燃气内燃机':
				temp_str = str(int(设备.发电机规模)) + 'kW ' + 设备.名称 + '(' + 设备.厂家型号 + ')' \
						   + ' 余热锅炉产汽量: ' + str(round(设备.锅炉额定产汽量, 2)) + 't/h' + ';'
				self.设备配置str.append(temp_str)
				self.设备配置string += temp_str

			elif 设备.名称 == '燃气锅炉':
				temp_str = str(round(设备.锅炉额定产汽量, 2)) + 't/h ' + 设备.名称 + ';'
				self.设备配置str.append(temp_str)
				self.设备配置string += temp_str


