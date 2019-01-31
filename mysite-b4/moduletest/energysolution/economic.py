import numpy as np
import copy


class 技经计算类:
	def __init__(self, 数据, 成本收入索引, 工程费用索引, 工程建设其他费用索引, 基本预备费, 收购费用, 建设投资, 维修费):
		# ==========================
		self.数据 = 数据
		self.成本收入索引 = 成本收入索引
		self.工程费用索引 = 工程费用索引
		self.工程建设其他费用索引 = 工程建设其他费用索引
		self.维修费_全年量 = self.成本收入取值(维修费, self.数据.数据索引['维修费_设定值'])
		self.基本预备费 = 基本预备费
		self.收购费用 = 收购费用

		self.供冷收入_税前 = self.成本收入取值(self.成本收入索引['供冷收入'], self.数据.数据索引['供冷收入_设定值'])
		self.供蒸汽收入_税前 = self.成本收入取值(self.成本收入索引['蒸汽收入'], self.数据.数据索引['供蒸汽收入_设定值'])
		self.发电收入_税前 = self.成本收入取值(self.成本收入索引['售电收入'], self.数据.数据索引['发电收入_设定值'])
		self.供热收入_税前 = self.成本收入取值(self.成本收入索引['供热收入'], self.数据.数据索引['供热收入_设定值'])
		self.光伏发电收入_税前 = self.成本收入取值(self.成本收入索引['光伏发电收入'], self.数据.数据索引['光伏发电收入_设定值'])
		self.天然气销售收入_税前 = self.数据.数据索引['额外天然气销售年总收入']
		self.供冷配套费收入_税前 = self.成本收入取值(0, self.数据.数据索引['供冷配套费收入_设定值'])
		self.供热配套费收入_税前 = self.成本收入取值(0, self.数据.数据索引['供冷配套费收入_设定值'])

		self.工资支出_全年量 = self.成本收入索引['工资及福利']
		self.光伏运维成本_全年量 = self.成本收入取值(0, self.数据.数据索引['光伏运维成本_设定值'])
		self.天然气支出_税前 = self.成本收入取值(self.成本收入索引['燃气费'] + self.数据.数据索引['额外天然气销售年总成本'], self.数据.数据索引['天然气支出_设定值'])
		self.水支出_税前 = self.成本收入取值(self.成本收入索引['水费'] , self.数据.数据索引['水支出_设定值'])
		self.电支出_税前 = self.成本收入取值(self.成本收入索引['电费'] , self.数据.数据索引['电支出_设定值'])
		self.变压器容量费_税前 = self.数据.数据索引['变压器容量费']
		self.系统备用容量费_税前 = self.数据.数据索引['系统备用容量费']
		self.土地租金_全年量_税前 = self.数据.数据索引['土地租金']
		self.设备租金_全年量_税前 = self.数据.数据索引['设备租金']

		#
		self.建筑费用 = 工程费用索引['工程费用']['建筑']
		self.设备费用 = 工程费用索引['工程费用']['设备']
		self.安装费用 = 工程费用索引['工程费用']['安装']
		self.工程建设其他费用总和 = self.工程建设其他费用索引['工程建设其他费用合计']
		# 土地费用
		self.土地费用 = self.工程建设其他费用索引['土地费']
		self.土地购置费投资 = self.工程建设其他费用索引['土地费']
		self.无形资产投资 = 0

		self.建设投资 = 建设投资
		self.借款 = self.建设投资 * self.数据.数据索引['借款比例']
		self.建设期利息 = self.借款 * self.数据.数据索引['借款利率'] * 1.1/2

		# 等于工资一半
		self.其他管理费用_全年量 = self.工资支出_全年量 * self.数据.数据索引['其他管理费用占工资比例']

		self.达产率 = self.数据.数据索引['达产率']

		# ========一级目录==========
		self.现金流入dict = {}
		self.现金流出dict = {}
		self.现金流入 = [0] * 21
		self.现金流出 = [0] * 21

		# ========二级目录=========
		self.销售收入 = {}
		self.补贴收入 = [0] * 21
		self.回收固定资产余值 = 0
		self.回收流动资金 = 0
		self.增值税销项税额 = {}

		self.增值税进项税额 = dict()
		self.增值税 = [0] * 21
		self.流动资金 = {}
		self.经营成本 = {}
		# self.销售税金及附加 = {}
		# self.所得税 = {}
		# self.利用原有固定资产 = {}
		# self.特种基金 = {}

		# ========三级目录=========
		# 销售收入
		self.供冷收入 = [0] * 21
		self.供热收入 = [0] * 21
		self.发电收入 = [0] * 21
		self.光伏发电收入 = [0] * 21
		self.供蒸汽收入 = [0] * 21
		self.天然气销售收入 = [0] * 21
		self.供冷配套费收入 = [0] * 21
		self.供热配套费收入 = [0] * 21
		self.销售收入总和 = [0] * 21

		# 固定资产余值
		self.建筑类固定资产余值 = 0
		self.设备及安装类固定资产余值 = 0
		self.回收固定资产余值 = 0

		# 销项税
		self.供冷收入销项税 = [0] * 21
		self.供蒸汽收入销项税 = [0] * 21
		self.发电收入销项税 = [0] * 21
		self.供热收入销项税 = [0] * 21
		self.光伏发电收入销项税 = [0] * 21
		self.天然气销售收入销项税 = [0] * 21
		self.供冷配套费收入销项税 = [0] * 21
		self.供热配套费收入销项税 = [0] * 21
		self.增值税销项税额总和 = [0] * 21

		# 进项税
		self.天然气支出进项税 = [0] * 21
		self.水支出进项税 = [0] * 21
		self.电支出进项税 = [0] * 21
		self.变压器容量费进项税 = [0] * 21
		self.系统备用容量费进项税 = [0] * 21
		self.增值税进项税额总和 = [0] * 21

		# 增值税
		self.增值税总和 = [0] * 21
		# 销售税金及附加总和
		self.销售税金及附加总和 = [0] * 21

		# 流动资金
		self.应收账款 = [0] * 21
		self.天然气存货 = [0] * 21
		self.电存货 = [0] * 21
		self.水存货 = [0] * 21
		self.现金 = [0] * 21
		self.应付账款 = [0] * 21
		self.流动资金总和 = [0] * 21

		# 经营成本
		self.天然气支出 = [0] * 21
		self.水支出 = [0] * 21
		self.电支出 = [0] * 21
		self.变压器容量费 = [0] * 21
		self.系统备用容量费 = [0] * 21
		self.工资支出 = [0] * 21
		self.光伏运维成本 = [0] * 21
		self.土地租金 = [0] * 21
		self.维修费 = [0] * 21
		self.其他管理费用 = [0] * 21
		self.经营成本总和 = [0] * 21

		# 所得税
		self.利润总和 = [0] * 21
		self.EBIT = [0] * 21
		self.所得税总和 = [0] * 21

		# 折旧费
		self.工程建设其他费用待摊费用 = 0
		self.税后建筑类投资 = 0
		self.税后设备及安装类投资 = 0
		self.建筑类折旧费 = [0] * 21
		self.设备及安装类折旧费 = [0] * 21
		self.无形资产折旧费 = [0] * 21
		self.土地购置费折旧费 = [0] * 21
		self.折旧费 = dict()
		self.折旧费总和 = [0] * 21

		# 财务费用
		self.财务费用 = [0] * 21

		# 成本费用总和
		self.成本费用总和 = [0] * 21

		# 净现金流
		self.税后净现金流量 = [0] * 21
		self.累计税后净现金流量 = [0] * 21

		# ===================计算========================
		self.计算销售收入()
		self.计算销项税()

		self.计算经营成本()
		self.计算进项税()
		self.计算增值税及销售税金及附加()
		self.计算流动资金()
		self.计算折旧费()
		self.计算财务费用()
		self.计算成本费用总和()
		self.计算所得税()

		self.计算回收固定资产余值()
		self.计算回收流动资金()
		self.计算现金流入总和()
		self.计算现金流出总和()
		self.计算税后净现金流量()
		self.计算累计税后净现金流量()

		self.内部收益率 = np.irr(self.税后净现金流量)
		self.计算投资回收期()
		self.年均销售收入 = sum(self.销售收入总和) / 20
		self.年均总成本费用 = sum(self.成本费用总和) / 20
		self.年均利润总额 = sum(self.利润总和) / 20
		self.净现值 = np.npv(0.12, self.税后净现金流量)
		self.生成技经计算结果()
		self.生成技经计算明细列表()

		print('税后净现金流量', self.税后净现金流量)
		print('内部收益率', self.内部收益率)
		print('投资回收期', self.投资回收期)
		print('建设投资', self.建设投资)
		print('年均利润总额', self.年均利润总额)

		print('现金流入', self.现金流入)
		print('销售收入总和', self.销售收入总和)
		print('增值税销项税额总和', self.增值税销项税额总和)

		print('现金流出', self.现金流出)
		print('增值税进项税额总和', self.增值税进项税额总和)
		print('增值税总和', self.增值税总和)
		print('流动资金总和', self.流动资金总和)
		print('经营成本总和', self.经营成本总和)
		print('销售税金及附加总和', self.销售税金及附加总和)
		print('所得税总和', self.所得税总和)

		print('成本费用总和', self.成本费用总和)
		for key,value in self.经营成本.items():
			print(key, value)
		print('折旧费总和', self.折旧费总和)
		print('年均总成本费用', self.年均总成本费用)
		print('财务费用', self.财务费用)
		print('年均销售收入', self.年均销售收入)
		print('利润总和', self.利润总和)
		print('维修费', self.维修费)

		for key,value in self.流动资金.items():
			print(key, value)

	def 计算销售收入(self):
		self.供冷收入 = [self.达产率[i] * self.供冷收入_税前 / (1 + self.数据.数据索引['冷增值税税率']) for i in range(21)]
		self.供热收入 = [self.达产率[i] * self.供热收入_税前 / (1 + self.数据.数据索引['热增值税税率']) for i in range(21)]
		self.供蒸汽收入 = [self.达产率[i] * self.供蒸汽收入_税前 / (1 + self.数据.数据索引['蒸汽增值税税率']) for i in range(21)]
		self.发电收入 = [self.达产率[i] * self.发电收入_税前 / (1 + self.数据.数据索引['电增值税税率']) for i in range(21)]
		self.光伏发电收入 = [self.达产率[i] * self.光伏发电收入_税前 / (1 + self.数据.数据索引['电增值税税率']) for i in range(21)]
		self.天然气销售收入 = [self.达产率[i] * self.天然气销售收入_税前 / (1 + self.数据.数据索引['气增值税税率']) for i in range(21)]
		self.供冷配套费收入 = [self.达产率[i] * self.供冷配套费收入_税前 / (1 + self.数据.数据索引['冷增值税税率']) for i in range(21)]
		self.供热配套费收入 = [self.达产率[i] * self.供热配套费收入_税前 / (1 + self.数据.数据索引['热增值税税率']) for i in range(21)]

		self.销售收入['供冷收入'] = self.供冷收入
		self.销售收入['供热收入'] = self.供热收入
		self.销售收入['发电收入'] = self.发电收入
		self.销售收入['光伏发电收入'] = self.光伏发电收入
		self.销售收入['供蒸汽收入'] = self.供蒸汽收入
		self.销售收入['天然气销售收入'] = self.天然气销售收入
		self.销售收入['供冷配套费收入'] = self.供冷配套费收入
		self.销售收入['供热配套费收入'] = self.供热配套费收入

		for value in self.销售收入.values():
			self.销售收入总和 = self.矩阵加法(self.销售收入总和, value)

	def 计算回收固定资产余值(self):
		self.建筑类固定资产余值 = self.税后建筑类投资 * self.数据.数据索引['建筑类残值率']
		self.设备及安装类固定资产余值 = self.税后设备及安装类投资 * self.数据.数据索引['设备及安装类残值率']

		self.回收固定资产余值 = self.建筑类固定资产余值 + self.设备及安装类固定资产余值

	def 计算回收流动资金(self):
		self.回收流动资金 = sum(self.流动资金总和)

	def 计算销项税(self):
		self.供冷收入销项税 = [self.供冷收入[i] * self.数据.数据索引['冷增值税税率'] for i in range(21)]
		self.供蒸汽收入销项税 = [self.供蒸汽收入[i] * self.数据.数据索引['蒸汽增值税税率'] for i in range(21)]
		self.发电收入销项税 = [self.发电收入[i] * self.数据.数据索引['电增值税税率'] for i in range(21)]
		self.供热收入销项税 = [self.供热收入[i] * self.数据.数据索引['热增值税税率'] for i in range(21)]
		self.光伏发电收入销项税 = [self.光伏发电收入[i] * self.数据.数据索引['电增值税税率'] for i in range(21)]
		self.天然气销售收入销项税 = [self.天然气销售收入[i] * self.数据.数据索引['气增值税税率'] for i in range(21)]
		self.供冷配套费收入销项税 = [self.供冷配套费收入[i] * self.数据.数据索引['冷增值税税率'] for i in range(21)]
		self.供热配套费收入销项税 = [self.供热配套费收入[i] * self.数据.数据索引['热增值税税率'] for i in range(21)]

		self.增值税销项税额['供冷收入销项税'] = self.供冷收入销项税
		self.增值税销项税额['供蒸汽收入销项税'] = self.供蒸汽收入销项税
		self.增值税销项税额['发电收入销项税'] = self.发电收入销项税
		self.增值税销项税额['供热收入销项税'] = self.供热收入销项税
		self.增值税销项税额['光伏发电收入销项税'] = self.光伏发电收入销项税
		self.增值税销项税额['天然气销售收入销项税'] = self.天然气销售收入销项税
		self.增值税销项税额['供冷配套费收入销项税'] = self.供冷配套费收入销项税
		self.增值税销项税额['供热配套费收入销项税'] = self.供热配套费收入销项税

		for value in self.增值税销项税额.values():
			self.增值税销项税额总和 = self.矩阵加法(self.增值税销项税额总和, value)			

# =======================现金流出计算===========================================
	def 计算进项税(self):
		self.天然气支出进项税 = [self.天然气支出[i] * self.数据.数据索引['气增值税税率'] for i in range(21)]
		self.水支出进项税 = [self.水支出[i] * self.数据.数据索引['水增值税税率'] for i in range(21)]
		self.电支出进项税 = [self.电支出[i] * self.数据.数据索引['电增值税税率'] for i in range(21)]
		self.变压器容量费进项税 = [self.变压器容量费[i] * self.数据.数据索引['电增值税税率'] for i in range(21)]
		self.系统备用容量费进项税 = [self.系统备用容量费[i] * self.数据.数据索引['电增值税税率'] for i in range(21)]
		self.土地租金进项税 = [0] + [self.土地租金[i + 1] * self.数据.数据索引['土地费用增值税税率']for i in range(20)]

		self.增值税进项税额['天然气支出进项税'] = self.天然气支出进项税
		self.增值税进项税额['水支出进项税'] = self.水支出进项税
		self.增值税进项税额['电支出进项税'] = self.电支出进项税
		self.增值税进项税额['变压器容量费进项税'] = self.变压器容量费进项税
		self.增值税进项税额['系统备用容量费进项税'] = self.系统备用容量费进项税
		self.增值税进项税额['土地租金进项税'] = self.土地租金进项税

		for value in self.增值税进项税额.values():
			self.增值税进项税额总和 = self.矩阵加法(self.增值税进项税额总和, value)

	def 计算增值税及销售税金及附加(self):
		self.工程建设其他费用增值税 = (
				(self.工程建设其他费用总和 - self.土地费用 - self.工程建设其他费用索引['建设单位管理费']) * self.数据.数据索引['工程建设其他费用增值税税率'] / (1 + self.数据.数据索引['工程建设其他费用增值税税率'])
				+ self.土地费用 * self.数据.数据索引['土地费用增值税税率'] / (1 + self.数据.数据索引['土地费用增值税税率'])
		)
		建设投资增值税 = (
				self.建筑费用 * self.数据.数据索引['建筑费用增值税税率'] / (1 + self.数据.数据索引['建筑费用增值税税率'])
				+ self.设备费用 * self.数据.数据索引['设备费用增值税税率'] / (1 + self.数据.数据索引['设备费用增值税税率'])
				+ self.安装费用 * self.数据.数据索引['安装费用增值税税率'] / (1 + self.数据.数据索引['安装费用增值税税率'])
				+ self.工程建设其他费用增值税
		)
		print('建筑费用',self.建筑费用)
		print('设备费用', self.设备费用)
		print('安装费用', self.安装费用)
		print('工程建设其他费用增值税', self.工程建设其他费用增值税)

		# 计算增值税
		剩余抵免额 = 建设投资增值税
		print('剩余抵免额',剩余抵免额)
		for i in range(21):		
			本年度抵免额 = min(self.增值税销项税额总和[i] - self.增值税进项税额总和[i], 剩余抵免额)
			剩余抵免额 -= 本年度抵免额
			self.增值税总和[i] = self.增值税销项税额总和[i] - self.增值税进项税额总和[i] - 本年度抵免额

		# 环保税还没加
		for i in range(21):
			self.销售税金及附加总和[i] = self.增值税总和[i] * self.数据.数据索引['城市维护建设税率'] + self.增值税总和[i] * self.数据.数据索引['教育附加税率'] + self.增值税总和[i] * self.数据.数据索引['水利基金税率']

	# 待完善
	# 流动资产, 流动负债的含义
	# 存货和经营成本是否需要重复计算
	# 应付账款尚未考虑水费, 工资及财务费用
	def 计算流动资金(self):
		# 检查下式
		self.应收账款 = [(self.经营成本总和[i] - (self.维修费[i] + self.光伏运维成本[i])) / self.数据.数据索引['应收账款周转次数'] for i in range(21)]
		self.天然气存货 = [self.天然气支出[i] * self.数据.数据索引['是否备天然气存货']  / self.数据.数据索引['天然气存货周转次数'] for i in range(21)]
		self.电存货 = [self.电支出[i] * self.数据.数据索引['是否备电存货'] / self.数据.数据索引['电存货周转次数'] for i in range(21)]
		self.水存货 = [self.水支出[i] * self.数据.数据索引['是否备水存货'] / self.数据.数据索引['水存货周转次数'] for i in range(21)]
		# 检查下式
		self.现金 = [(self.维修费[i] + self.光伏运维成本[i]) / self.数据.数据索引['维修费周转次数'] for i in range(21)]

		self.应付账款 = [
			(self.天然气支出[i] * self.数据.数据索引['天然气是否先用后付']
			 + self.维修费[i]  * self.数据.数据索引['维修费是否先用后付']
			 + self.水支出[i] * self.数据.数据索引['水费是否先用后付']
			 + self.电支出[i] * self.数据.数据索引['电费是否先用后付']
			 + self.工资支出[i] * self.数据.数据索引['工资是否先用后付']
			 ) / self.数据.数据索引['应付账款周转次数'] for i in range(21)]


		self.流动资金['应收账款'] = self.应收账款
		self.流动资金['天然气存货'] = self.天然气存货
		self.流动资金['电存货'] = self.电存货
		self.流动资金['水存货'] = self.水存货
		self.流动资金['现金'] = self.现金
		self.流动资金['应付账款'] = self.应付账款

		self.流动资金总和 = [0] * 21
		for key, value in self.流动资金.items():
			if key == '应付账款':
				self.流动资金总和 = self.矩阵减法(self.流动资金总和, value)
			else:
				self.流动资金总和 = self.矩阵加法(self.流动资金总和, value)

		累计流动资金 = 0
		for i in range(21):
			if self.流动资金总和[i] > 累计流动资金:
				新增流动资金 = self.流动资金总和[i] - 累计流动资金
				累计流动资金 += 新增流动资金
				self.流动资金总和[i] = 新增流动资金
			else:
				self.流动资金总和[i] = 0

		# self.流动资金总和 = [0] + [4750000] + [1580000] + [0] * 18

	def 计算经营成本(self):
		self.天然气支出 = [self.达产率[i] * self.天然气支出_税前 / (1 + self.数据.数据索引['气增值税税率']) for i in range(21)]
		self.水支出 = [self.达产率[i] * self.水支出_税前 / (1 + self.数据.数据索引['水增值税税率']) for i in range(21)]
		self.电支出 = [self.达产率[i] * self.电支出_税前 / (1 + self.数据.数据索引['电增值税税率']) for i in range(21)]
		self.变压器容量费 = [0] + [self.变压器容量费_税前 / (1 + self.数据.数据索引['电增值税税率'])] * 20
		self.系统备用容量费 = [0] + [self.系统备用容量费_税前 / (1 + self.数据.数据索引['电增值税税率'])] * 20
		self.工资支出 = [0] + [self.工资支出_全年量] * 20
		self.光伏运维成本 = [0] + [self.光伏运维成本_全年量] * 20
		# 土地租金相关部分需完善
		self.土地租金 = [0] + [self.土地租金_全年量_税前 / (1 + self.数据.数据索引['土地费用增值税税率'])] * 20
		self.设备租金 = [0] + [self.设备租金_全年量_税前] * 20
		# 维修费计算待完善
		self.维修费 = [self.维修费_全年量 * self.达产率[i] for i in range(21)]
		self.其他管理费用 = [0] + [self.其他管理费用_全年量] * 20

		self.经营成本['天然气支出'] = self.天然气支出
		self.经营成本['水支出'] = self.水支出
		self.经营成本['电支出'] = self.电支出
		self.经营成本['变压器容量费'] = self.变压器容量费
		self.经营成本['系统备用容量费'] = self.系统备用容量费
		self.经营成本['工资支出'] = self.工资支出
		self.经营成本['光伏运维成本'] = self.光伏运维成本
		self.经营成本['土地租金 '] = self.土地租金
		self.经营成本['设备租金 '] = self.设备租金
		self.经营成本['维修费'] = self.维修费
		self.经营成本['其他管理费用'] = self.其他管理费用

		for value in self.经营成本.values():
			self.经营成本总和 = self.矩阵加法(self.经营成本总和, value)
	
	def 计算所得税(self):
		self.利润总和 = [self.销售收入总和[i] + self.补贴收入[i] - self.成本费用总和[i] - self.销售税金及附加总和[i] for i in range(21)]
		self.EBIT = [self.利润总和[i] + self.财务费用[i] for i in range(21)]
		self.所得税总和 = [self.EBIT[i] * self.数据.数据索引['所得税率'] for i in range(21)]

	# 折旧费待完善
	
	def 计算折旧费(self):
		self.税后土地购置投资 = self.土地购置费投资 / (1 + self.数据.数据索引['土地费用增值税税率'])
		self.工程建设其他费用待摊费用 = self.工程建设其他费用总和 - self.工程建设其他费用增值税 - self.税后土地购置投资
		self.总待摊费用 = self.工程建设其他费用待摊费用 + self.建设期利息 + self.基本预备费
		self.税后建筑类投资 = self.建筑费用 / (1 + self.数据.数据索引['建筑费用增值税税率']) + self.总待摊费用 * (self.建筑费用 / (self.建筑费用 + self.设备费用 + self.安装费用))
		self.税后设备及安装类投资 = (
			self.收购费用
			+ self.设备费用 / (1 + self.数据.数据索引['设备费用增值税税率'])
			+ self.安装费用 / (1 + self.数据.数据索引['安装费用增值税税率'])
			+ self.总待摊费用 * ((self.设备费用 + self.安装费用) / (self.建筑费用 + self.设备费用 + self.安装费用))
		)

		print('税后建筑类投资', self.税后建筑类投资)
		print('设备费用', self.设备费用)
		print('安装费用', self.安装费用)
		print('建设期利息', self.建设期利息)
		print('税后设备及安装类投资', self.税后设备及安装类投资)
		print('土地购置投资', self.土地购置费投资)

		for i in range(int(self.数据.数据索引['建筑类折旧年限'])):
			self.建筑类折旧费[i+1] = self.税后建筑类投资 * (1 - self.数据.数据索引['建筑类残值率']) * (1 / self.数据.数据索引['建筑类折旧年限'])

		for i in range(int(self.数据.数据索引['设备及安装类折旧年限'])):
			self.设备及安装类折旧费[i+1] = self.税后设备及安装类投资 * (1 - self.数据.数据索引['设备及安装类残值率']) * (1 / self.数据.数据索引['设备及安装类折旧年限'])

		for i in range(int(self.数据.数据索引['无形资产折旧年限'])):
			self.无形资产折旧费[i+1] = self.无形资产投资 * (1 - self.数据.数据索引['无形资产残值率']) * (1 / self.数据.数据索引['无形资产折旧年限'])

		for i in range(int(self.数据.数据索引['土地购置费折旧年限'])):
			self.土地购置费折旧费[i+1] = self.税后土地购置投资 * (1 - self.数据.数据索引['土地购置费残值率']) * (1 / self.数据.数据索引['土地购置费折旧年限'])

		self.折旧费['建筑类折旧费'] = self.建筑类折旧费
		self.折旧费['设备及安装类折旧费'] = self.设备及安装类折旧费 
		self.折旧费['无形资产折旧费'] = self.无形资产折旧费 
		self.折旧费['土地购置费折旧费'] = self.土地购置费折旧费

		for value in self.折旧费.values():
			self.折旧费总和 = self.矩阵加法(self.折旧费总和, value)

	def 计算财务费用(self):
		借款余额 = self.借款
		每年还本金 = self.借款 / (self.数据.数据索引['还款周期'] - self.数据.数据索引['还本起始年'] + 1)
		for i in range(int(self.数据.数据索引['还款周期'])):
			self.财务费用[i + 1] = 借款余额 * self.数据.数据索引['借款利率']
			if i + 1 >= self.数据.数据索引['还本起始年']:
				借款余额 -= 每年还本金
			else:
				pass

	def 计算成本费用总和(self):
		self.成本费用总和 = [self.经营成本总和[i] + self.折旧费总和[i] + self.财务费用[i] for i in range(21)]

# =================================合计===================================================
	def 计算现金流入总和(self):
		for i in range(21):
			if i == 20:
				self.现金流入[i] = self.销售收入总和[i] + self.补贴收入[i] + self.增值税销项税额总和[i] + self.回收固定资产余值 + self.回收流动资金 
			else:
				self.现金流入[i] = self.销售收入总和[i] + self.补贴收入[i] + self.增值税销项税额总和[i] 

	def 计算现金流出总和(self):
		for i in range(21):
			if i == 0:
				self.现金流出[i] = self.建设投资 + self.增值税进项税额总和[i] + self.增值税总和[i] + self.流动资金总和[i] + self.经营成本总和[i] + self.销售税金及附加总和[i] + self.所得税总和[i]
			else:
				self.现金流出[i] = self.增值税进项税额总和[i] + self.增值税总和[i] + self.流动资金总和[i] + self.经营成本总和[i] + self.销售税金及附加总和[i] + self.所得税总和[i]

	def 计算税后净现金流量(self):
		self.税后净现金流量 = [self.现金流入[i] - self.现金流出[i] for i in range(21)]

	def 计算累计税后净现金流量(self):
		for i in range(21):
			if i == 0:
				self.累计税后净现金流量[i] = self.税后净现金流量[i]
			else:
				self.累计税后净现金流量[i] = self.累计税后净现金流量[i-1] + self.税后净现金流量[i]

# =================================================================
	def 矩阵加法(self, list1, list2):
		list_sum = [0] * max(len(list1), len(list2))
		for i in range(len(list_sum)):
			if i > len(list1) - 1:
				a = 0
			else:
				a = list1[i]

			if i > len(list2) - 1:
				b = 0
			else:
				b = list2[i]

			list_sum[i] = a + b
		return list_sum

	def 矩阵减法(self, list1, list2):
		list_sum = [0] * max(len(list1), len(list2))
		for i in range(len(list_sum)):
			if i > len(list1) - 1:
				a = 0
			else:
				a = list1[i]

			if i > len(list2) - 1:
				b = 0
			else:
				b = list2[i]

			list_sum[i] = a - b
		return list_sum

	def 计算投资回收期(self):
		for i in range(21):
			if self.累计税后净现金流量[i] > 0:
				self.投资回收期 = i - self.累计税后净现金流量[i] / self.税后净现金流量[i]
				return 
		self.投资回收期 = -0.001

	def 成本收入取值(self, x, y):
		if self.数据.数据索引['采用成本收入设定值赋值'] == '是' and y > 0:
			return y
		else:
			return x

	def 生成技经计算结果(self):
		self.技经计算结果 = {
			'建设投资(万元)' : int(self.建设投资 / 10000),
			'年均销售收入(万元)': int(self.年均销售收入 / 10000),
			'年均总成本费用(万元)': int(self.年均总成本费用 / 10000),
			'年均利润总额(万元)': int(self.年均利润总额 / 10000),
			'投资回收期': round(self.投资回收期, 2),
			'内部收益率_税后': round(self.内部收益率, 4),
			'净现值(万元)': int(self.净现值 / 10000),
		}

		self.技经计算结果json = {
			'investment': int(self.建设投资 / 10000),
			'annualIncome': int(self.年均销售收入 / 10000),
			'annualCost': int(self.年均总成本费用 / 10000),
			'annualProfit': int(self.年均利润总额 / 10000),
			'returnPeriod': round(self.投资回收期, 2),
			'iRR': round(self.内部收益率, 4),
			'netValue': int(self.净现值 / 10000),
		}
# 技经 = 技经计算类( 数据类())

	def 生成技经计算明细列表(self):

		现金流入_copy = copy.deepcopy(self.现金流入)
		销售收入总和_copy = copy.deepcopy(self.销售收入总和)
		增值税销项税额总和_copy = copy.deepcopy(self.增值税销项税额总和)
		现金流出_copy = copy.deepcopy(self.现金流出)
		增值税进项税额总和_copy = copy.deepcopy(self.增值税进项税额总和)
		增值税总和_copy = copy.deepcopy(self.增值税总和)
		流动资金总和_copy = copy.deepcopy(self.流动资金总和)
		经营成本总和_copy = copy.deepcopy(self.经营成本总和)
		销售税金及附加总和_copy = copy.deepcopy(self.销售税金及附加总和)
		所得税总和_copy = copy.deepcopy(self.所得税总和)
		税后净现金流量_copy = copy.deepcopy(self.税后净现金流量)

		单位转换清单 = [
			现金流入_copy,
			销售收入总和_copy,
			增值税销项税额总和_copy,
			现金流出_copy,
			增值税进项税额总和_copy,
			增值税总和_copy,
			流动资金总和_copy,
			经营成本总和_copy,
			销售税金及附加总和_copy,
			所得税总和_copy,
			税后净现金流量_copy,
		]
		for list in 单位转换清单:
			for i, item in enumerate(list):
				list[i] = int(item / 10000)


		self.技经计算明细列表 = []
		self.技经计算明细列表.append(['年份'] + [i+1 for i in range(21)])
		self.技经计算明细列表.append(['1-现金流入'] + 现金流入_copy)
		self.技经计算明细列表.append(['1.1-销售收入总和'] + 销售收入总和_copy)
		self.技经计算明细列表.append(['1.2-增值税销项税额总和'] + 增值税销项税额总和_copy)
		self.技经计算明细列表.append(['1.3-回收固定资产余值'] + [0 for i in range(20)] + [int(self.回收固定资产余值/ 10000)])
		self.技经计算明细列表.append(['1.4-回收流动资金'] + [0 for i in range(20)] + [int(self.回收流动资金 / 10000)])

		self.技经计算明细列表.append(['2-现金流出'] + 现金流出_copy)
		self.技经计算明细列表.append(['2.1-固定资产投资'] +  [int(self.建设投资 / 10000)] + [0 for i in range(20)])
		self.技经计算明细列表.append(['2.2-增值税进项税额总和'] + 增值税进项税额总和_copy)
		self.技经计算明细列表.append(['2.3-增值税总和'] + 增值税总和_copy)
		self.技经计算明细列表.append(['2.4-流动资金总和'] + 流动资金总和_copy)
		self.技经计算明细列表.append(['2.5-经营成本总和'] + 经营成本总和_copy)
		self.技经计算明细列表.append(['2.6-销售税金及附加总和'] + 销售税金及附加总和_copy)
		self.技经计算明细列表.append(['2.7-所得税总和'] + 所得税总和_copy)
		self.技经计算明细列表.append(['3-税后净现金流量'] + 税后净现金流量_copy)
