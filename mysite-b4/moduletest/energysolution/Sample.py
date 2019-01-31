import xlrd
from .Data import 数据类
import  os
class 设备样本类:
	def __init__(self, 数据):
		self.数据 = 数据
		file = "static/moduletest/SampleBase.xlsx"
		file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), file)
		wb = xlrd.open_workbook(file)
		self.wb = wb
		self.燃气轮机样本列表 = self.燃气轮机样本库()
		self.燃气内燃机样本列表 = self.燃气内燃机样本库()
		self.燃气锅炉样本列表 = self.燃气锅炉样本库()

	def 燃气锅炉样本库(self):
		燃气锅炉列表 = []
		for i in range(1000):
			temp_dict = {}
			temp_dict['名称'] = '燃气锅炉'
			temp_dict['锅炉额定产汽量'] = i * 0.1
			燃气锅炉列表.append(temp_dict)
		return 燃气锅炉列表

	def 燃气轮机样本库(self):
		data = self.wb
		sheet = data.sheets()[0]
		nrows = sheet.nrows
		燃气轮机列表 = []

		for i in range(1, nrows):
			temp_dict = {}
			temp_dict['名称'] = '燃气轮机'
			temp_dict['公司型号'] = sheet.row_values(i)[2]
			temp_dict['发电功率'] = sheet.row_values(i)[1] * self.数据.数据索引['燃气轮机发电功率修正']
			temp_dict['烟气热量'] = self.计算烟气热量(排烟气量 = sheet.row_values(i)[7] * self.数据.数据索引['燃气轮机烟气流量修正'], 烟气温度 = sheet.row_values(i)[8] * self.数据.数据索引['燃气轮机排烟温度修正'])
			temp_dict['锅炉额定产汽量'] = self.计算余热锅炉蒸汽产量(temp_dict['烟气热量'])
			temp_dict['发电效率'] = sheet.row_values(i)[3] * self.数据.数据索引['燃气轮机发电效率修正'] / 100
			temp_dict['额定制冷量'] = self.计算溴冷机额定制冷量(temp_dict['烟气热量'])

			燃气轮机列表.append(temp_dict)

		return 燃气轮机列表

	def 燃气内燃机样本库(self):
		data = self.wb
		sheet = data.sheets()[1]
		nrows = sheet.nrows
		燃气内燃机列表 = []

		for i in range(2,nrows):
			temp_dict = {}
			temp_dict['名称'] = '燃气内燃机'
			temp_dict['公司型号'] = sheet.row_values(i)[1]
			temp_dict['发电功率'] = sheet.row_values(i)[2]
			temp_dict['发电效率'] = sheet.row_values(i)[12]/ 100

			if sheet.row_values(i)[7] == 0 or sheet.cell_type(i,7) == 0 or sheet.row_values(i)[8] == 0 or sheet.cell_type(i,8) == 0:
				temp_dict['烟气热量'] = sheet.row_values(i)[10]
			else:
				temp_dict['烟气热量'] = self.计算烟气热量(sheet.row_values(i)[8] / 1000, sheet.row_values(i)[7])

			temp_dict['缸套水热量'] = sheet.row_values(i)[4]

			temp_dict['锅炉额定产汽量'] = self.计算余热锅炉蒸汽产量(temp_dict['烟气热量'] )
			temp_dict['额定制冷量'] = self.计算溴冷机额定制冷量(temp_dict['烟气热量'],  temp_dict['缸套水热量'])
			燃气内燃机列表.append(temp_dict)

		return 燃气内燃机列表

	def 计算烟气热量(self, 排烟气量, 烟气温度):
		烟气焓值差 = -10.1 + 1.103 * (烟气温度 - self.数据.数据索引['冷却后烟气温度'])
		烟气热量 = 烟气焓值差 * 排烟气量 * 1000 / 3600
		return 烟气热量

	def 计算溴冷机额定制冷量(self, 烟气热量, 缸套水热量=0):
		制冷量 = 烟气热量 * self.数据.数据索引['烟气型溴冷机COP'] + 缸套水热量 * self.数据.数据索引['热水型溴冷机COP']
		return 制冷量

	def 计算余热锅炉蒸汽产量(self, 烟气热量):
		蒸汽产量 = 烟气热量 * 3600 * self.数据.数据索引['余热锅炉效率'] / self.数据.数据索引['水蒸气焓差'] / 1000
		return 蒸汽产量

	def 选择燃气轮机样本(self, 型号):
		for 样本 in self.燃气轮机样本列表:
			if 样本['公司型号'] == 型号:
				return 样本

	def 选择发电机样本(self, 型号):
		for 样本 in self.燃气轮机样本列表:
			if 样本['公司型号'] == 型号:
				return 样本
		for 样本 in self.燃气内燃机样本列表:
			if 样本['公司型号'] == 型号:
				return 样本
