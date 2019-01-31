# coding=utf-8
from django import forms
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.forms import widgets  # 插件
from .energysolution.Data import 数据类
from .energysolution.Sample import 设备样本类
from .models import Load, ProjectInfo


class UserForm(forms.Form):
	username = forms.CharField(label='用户名', widget=forms.TextInput())
	password = forms.CharField(label='密码',widget=forms.PasswordInput())
	email = forms.EmailField(label='邮箱')

def validate_excel(value):
	if value.name.split('.')[-1] not in ['xls','xlsx']:
		raise ValidationError(_('Invalid File Type: %(value)s'),params={'value': value},)

class UploadExcelForm(forms.Form):
	# excel = forms.FileField(validators=[validate_excel]) #这里使用自定义的验证

	发电机台数 = forms.IntegerField(label='发电机台数', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	燃气价格 = forms.CharField(label='燃气价格(元/标方)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	蒸汽价格 = forms.CharField(label='蒸汽价格(元/t)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	燃气热值 = forms.CharField(label='燃气热值(kCal/标方)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	水蒸气焓差 = forms.CharField(label='水蒸气焓差(kJ/kg)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	燃气轮机满负荷运行小时数限制 = forms.CharField(label='燃气轮机满负荷运行小时数限制', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	燃气内燃机满负荷运行小时数限制 = forms.CharField(label='燃气内燃机满负荷运行小时数限制',  widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	燃气锅炉效率 = forms.CharField(label='燃气锅炉效率(0<x<1)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	余热锅炉效率 = forms.CharField(label='余热锅炉效率(0<x<1)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

	数据 = 数据类()
	设备样本库 = 设备样本类(数据)
	发电机型号列表 = []
	发电机样本列表 = 设备样本库.燃气轮机样本列表 + 设备样本库.燃气内燃机样本列表
	for i, 样本 in enumerate(发电机样本列表):
		发电机型号列表.append((样本['公司型号'], 样本['公司型号']))


	发电机型号选择 = forms.ChoiceField(
		label = "选择发电机型号",
		choices = 发电机型号列表,  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
		initial = 1,
		widget = widgets.Select(attrs={'class': 'form-control form-control-sm'})
	)

	# 负荷数据列表 = []
	# try:
	# 	负荷数据set  = Load.objects.all()
	# 	for 负荷数据 in 负荷数据set:
	# 		负荷数据列表.append((负荷数据.负荷文件名称, 负荷数据.负荷文件名称))
	# except:
	# 	pass
	#
	# 负荷数据 = forms.ChoiceField(
	# 	label= '选择负荷数据',
	# 	choices = 负荷数据列表,  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
	# 	initial = 0,
	# 	widget = widgets.Select(attrs={'class': 'form-control form-control-sm'})
	# )

	并网模式列表 = [
		("自发自用", "自发自用"),
		("全额上网", "全额上网"),
		("自发自用余电上网", "自发自用余电上网"),
	]

	并网模式 = forms.ChoiceField(
		label= '并网模式',
		choices = 并网模式列表,
		initial = 1,
		widget = widgets.Select(attrs={'class': 'form-control form-control-sm'})
	)

class UploadExcelForm2(forms.Form):
	excel = forms.FileField(validators=[validate_excel]) #这里使用自定义的验证
	负荷数据名称 = forms.CharField(label='负荷数据名称' ,widget=forms.TextInput(attrs={'class': 'form-control'}))

class WizardForm(forms.Form):
	excel = forms.FileField(validators=[validate_excel]) #这里使用自定义的验证
	项目名称 = forms.CharField(label='项目名称', widget=forms.TextInput(attrs={'class': 'form-control'}))

class ProjectInfoForm(forms.Form):
	项目名称 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	发电机台数 = forms.IntegerField(label='发电机台数', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	燃气价格 = forms.CharField(label='燃气价格(元/标方)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	蒸汽价格 = forms.CharField(label='蒸汽价格(元/t)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	燃气热值 = forms.CharField(label='燃气热值(kCal/标方)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	水蒸气焓差 = forms.CharField(label='水蒸气焓(kJ/kg)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	燃气轮机满负荷运行小时数限制 = forms.CharField(label='燃气轮机满负荷运行小时数限制', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	燃气内燃机满负荷运行小时数限制 = forms.CharField(label='燃气内燃机满负荷运行小时数限制', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	燃气锅炉效率 = forms.CharField(label='燃气锅炉效率(0<x<1)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	余热锅炉效率 = forms.CharField(label='余热锅炉效率(0<x<1)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

	数据 = 数据类()
	设备样本库 = 设备样本类(数据)
	发电机型号列表 = []
	发电机样本列表 = 设备样本库.燃气轮机样本列表 + 设备样本库.燃气内燃机样本列表
	for i, 样本 in enumerate(发电机样本列表):
		发电机型号列表.append((样本['公司型号'], 样本['公司型号']))

	发电机型号选择 = forms.ChoiceField(
		label="选择发电机型号",
		choices=发电机型号列表,  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
		initial=1,
		widget=widgets.Select(attrs={'class': 'form-control form-control-sm'})
	)

	并网模式列表 = [
		("自发自用", "自发自用"),
		("全额上网", "全额上网"),
		("自发自用余电上网", "自发自用余电上网"),
	]

	并网模式 = forms.ChoiceField(
		label='并网模式',
		choices=并网模式列表,
		initial=1,
		widget=widgets.Select(attrs={'class': 'form-control form-control-sm'})
	)

class Form2(forms.Form):
	负荷数据列表 = []
	try:
		负荷数据set = Load.objects.all()
		for 负荷数据 in 负荷数据set:
			负荷数据列表.append((负荷数据.负荷文件名称, 负荷数据.负荷文件名称))
	except:
		pass

	负荷数据 = forms.ChoiceField(
		choices=负荷数据列表,  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
		initial=0,
		widget=widgets.Select,
		label = '负荷数据选择',
	)

	并网模式列表 = [
		("自发自用", "自发自用"),
		("全额上网", "全额上网"),
		("自发自用余电上网", "自发自用余电上网"),
	]

	并网模式 = forms.ChoiceField(
		choices=并网模式列表,
		initial=1,
		widget=widgets.Select,
		label = '并网模式',
	)

	技术路线列表 = [
		("燃气轮机", "燃气轮机"),
		("燃气内燃机", "燃气内燃机"),
		("燃气锅炉", "燃气锅炉"),
	]

	技术路线列表 = forms.TypedChoiceField(
		choices=技术路线列表,
		initial=1,
		widget=forms.CheckboxSelectMultiple,
		label='技术路线选择',
	)

class Form_FirstPage(forms.Form):

	数据 = 数据类()
	设备样本库 = 设备样本类(数据)
	发电机型号列表 = []
	发电机样本列表 = 设备样本库.燃气轮机样本列表 + 设备样本库.燃气内燃机样本列表
	for i, 样本 in enumerate(发电机样本列表):
		发电机型号列表.append((样本['公司型号'], 样本['公司型号']))

	发电机型号列表.pop(0)

	发电机型号选择 = forms.ChoiceField(
		label="选择发电机型号",
		choices=发电机型号列表,  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
		widget=widgets.Select(attrs={'class': 'form-control form-control-sm'})
	)

	发电机台数 = forms.IntegerField(label='发电机台数', initial= 1,  widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

	并网模式列表 = [
		("自发自用", "自发自用"),
		("全额上网", "全额上网"),
		("自发自用余电上网", "自发自用余电上网"),
	]

	并网模式 = forms.ChoiceField(
		choices=并网模式列表,
		initial=1,
		widget=widgets.Select(attrs={'class': 'form-control form-control-sm'}),
		label = '并网模式',
	)

class Form_basic(forms.Form):
	燃气价格 = forms.FloatField(label='燃气价格(元/方)', widget=forms.TextInput(attrs={'id': '燃气价格', 'class': 'form-control form-control-sm'}))
	水价格 = forms.FloatField(label='水价格(元/t)', widget=forms.TextInput(attrs={'id': '水价格', 'class': 'form-control form-control-sm'}))
	蒸汽价格 = forms.FloatField(label='蒸汽价格(元/t)', widget=forms.TextInput(attrs={'id': '蒸汽价格', 'class': 'form-control form-control-sm'}))
	燃气热值 = forms.FloatField(label='燃气热值(kCal/方)', widget=forms.TextInput(attrs={'id': '燃气热值', 'class': 'form-control form-control-sm'}))
	管损率 = forms.FloatField(label='管损率', widget=forms.TextInput(attrs={'id': '管损率', 'class': 'form-control form-control-sm'}))
	水蒸气焓差 = forms.FloatField(label='水蒸气与给水焓差(kJ/kg)', widget=forms.TextInput(attrs={'id': '水蒸气焓差', 'class': 'form-control form-control-sm'}))
	土建工程建筑 = forms.FloatField(label='土建工程建筑费用(万元)', widget=forms.TextInput(attrs={'id': '土建工程建筑', 'class': 'form-control form-control-sm'}))
	管网投资总费用 = forms.FloatField(label='管网投资总费用(万元)', widget=forms.TextInput(attrs={'id': '管网投资总费用', 'class': 'form-control form-control-sm'}))
	辅助工程_设备_设定值 = forms.FloatField(label='辅助工程_设备费用(万元)', widget=forms.TextInput(attrs={'id': '辅助工程_设备_设定值', 'class': 'form-control form-control-sm'}))
	辅助工程_安装_设定值 = forms.FloatField(label='辅助工程_安装费用(万元)', widget=forms.TextInput(attrs={'id': '辅助工程_安装_设定值', 'class': 'form-control form-control-sm'}))
	电力接入费 = forms.FloatField(label='电力接入费(万元)', widget=forms.TextInput(attrs={'id': '电力接入费', 'class': 'form-control form-control-sm'}))
	燃气工程费 = forms.FloatField(label='燃气工程费(万元)', widget=forms.TextInput(attrs={'id': '燃气工程费', 'class': 'form-control form-control-sm'}))
	土地费 = forms.FloatField(label='土地购置费(万元)', widget=forms.TextInput(attrs={'id': '土地费', 'class': 'form-control form-control-sm'}))
	收购费用 = forms.FloatField(label='收购费用(万元)', widget=forms.TextInput(attrs={'id': '收购费用', 'class': 'form-control form-control-sm'}))
	人数 = forms.FloatField(label='人数', widget=forms.TextInput(attrs={'id': '人数', 'class': 'form-control form-control-sm'}))
	工资 = forms.FloatField(label='工资(万元/(人*年))', widget=forms.TextInput(attrs={'id': '工资', 'class': 'form-control form-control-sm'}))
	变压器容量费 = forms.FloatField(label='变压器容量费(万元/年)', widget=forms.TextInput(attrs={'id': '变压器容量费', 'class': 'form-control form-control-sm'}))
	系统备用容量费 = forms.FloatField(label='系统备用容量费(万元/年)', widget=forms.TextInput(attrs={'id': '系统备用容量费', 'class': 'form-control form-control-sm'}))
	土地租金 = forms.FloatField(label='土地租金(万元/年)', widget=forms.TextInput(attrs={'id': '土地租金', 'class': 'form-control form-control-sm'}))
	设备租金 = forms.FloatField(label='设备租金(万元/年)', widget=forms.TextInput(attrs={'id': '设备租金', 'class': 'form-control form-control-sm'}))
	额外天然气销售年总收入 = forms.FloatField(label='额外天然气销售年总收入(万元/年)', widget=forms.TextInput(attrs={'id': '额外天然气销售年总收入', 'class': 'form-control form-control-sm'}))
	额外天然气销售年总成本 = forms.FloatField(label='额外天然气销售年总成本(万元/年)', widget=forms.TextInput(attrs={'id': '额外天然气销售年总成本', 'class': 'form-control form-control-sm'}))


class Form_Machine(forms.Form):
	# 自耗电自供应比例 = forms.CharField()
	# 燃气轮机最大规模 = forms.FloatField(label='燃气轮机最大规模', widget=forms.TextInput(attrs={'id': '燃气轮机最大规模', 'class': 'form-control form-control-sm'}))
	# 燃气轮机最小规模 = forms.FloatField(label='燃气轮机最小规模', widget=forms.TextInput(attrs={'id': '燃气轮机最小规模', 'class': 'form-control form-control-sm'}))
	# 燃气轮机最大台数 = forms.FloatField(label='燃气轮机最大台数', widget=forms.TextInput(attrs={'id': '燃气轮机最大台数', 'class': 'form-control form-control-sm'}))
	燃气轮机满负荷运行小时数限制 = forms.FloatField(initial = 6000, label='燃气轮机满负荷运行小时数限制(h)', widget=forms.TextInput(attrs={'id': '燃气轮机满负荷运行小时数限制', 'class': 'form-control form-control-sm'}))
	燃气轮机自耗电比例 = forms.FloatField(initial = 0.04, label='燃气轮机自耗电比例', widget=forms.TextInput(attrs={'id': '燃气轮机自耗电比例', 'class': 'form-control form-control-sm'}))
	燃气轮机最低运行负荷比例 = forms.FloatField(initial = 0.85, label='燃气轮机最低负载比例', widget=forms.TextInput(attrs={'id': '燃气轮机最低运行负荷比例', 'class': 'form-control form-control-sm'}))
	燃气轮机发电效率修正 = forms.FloatField(initial = 1, label='燃气轮机发电效率修正', widget=forms.TextInput(attrs={'id': '燃气轮机发电效率修正', 'class': 'form-control form-control-sm'}))
	燃气轮机烟气流量修正 = forms.FloatField(initial = 1, label='燃气轮机烟气流量修正', widget=forms.TextInput(attrs={'id': '燃气轮机烟气流量修正', 'class': 'form-control form-control-sm'}))
	燃气轮机排烟温度修正 = forms.FloatField(initial = 1, label='燃气轮机排烟温度修正', widget=forms.TextInput(attrs={'id': '燃气轮机排烟温度修正', 'class': 'form-control form-control-sm'}))
	燃气轮机发电功率修正 = forms.FloatField(initial = 1, label='燃气轮机发电功率修正', widget=forms.TextInput(attrs={'id': '燃气轮机发电功率修正', 'class': 'form-control form-control-sm'}))


	燃气内燃机满负荷运行小时数限制 = forms.FloatField(initial = 6000, label='燃气内燃机满负荷运行小时数限制(h)', widget=forms.TextInput(attrs={'id': '燃气内燃机满负荷运行小时数限制', 'class': 'form-control form-control-sm'}))
	燃气内燃机自耗电比例 = forms.FloatField(initial = 0.04, label='燃气内燃机自耗电比例', widget=forms.TextInput(attrs={'id': '燃气内燃机自耗电比例', 'class': 'form-control form-control-sm'}))
	燃气内燃机最低运行负荷比例 = forms.FloatField(initial = 0.75, label='燃气内燃机最低负载比例', widget=forms.TextInput(attrs={'id': '燃气内燃机最低运行负荷比例', 'class': 'form-control form-control-sm'}))
	# 燃气内燃机最大规模 = forms.FloatField(initial = 0, label='燃气内燃机最大规模', widget=forms.TextInput(attrs={'id': '燃气内燃机最大规模', 'class': 'form-control form-control-sm'}))
	# 燃气内燃机最小规模 = forms.FloatField(initial = 0, label='燃气内燃机最小规模', widget=forms.TextInput(attrs={'id': '燃气内燃机最小规模', 'class': 'form-control form-control-sm'}))
	# 燃气内燃机最大台数 = forms.FloatField(initial = 0, label='燃气内燃机最大台数', widget=forms.TextInput(attrs={'id': '燃气内燃机最大台数', 'class': 'form-control form-control-sm'}))

	# 燃气锅炉
	燃气锅炉单位产汽耗电量 = forms.FloatField(initial = 5, label='燃气锅炉单位产汽耗电量(kWh/t)', widget=forms.TextInput(attrs={'id': '燃气锅炉单位产汽耗电量', 'class': 'form-control form-control-sm'}))
	锅炉耗水率 = forms.FloatField(initial = 1.1, label='锅炉耗水率', widget=forms.TextInput(attrs={'id': '锅炉耗水率', 'class': 'form-control form-control-sm'}))
	燃气锅炉效率 = forms.FloatField(initial = 0.95, label='燃气锅炉效率', widget=forms.TextInput(attrs={'id': '燃气锅炉效率', 'class': 'form-control form-control-sm'}))
	# 燃气锅炉满负荷运行小时数限制 = forms.CharField(initial = 0, label='燃气锅炉满负荷运行小时数限制',)
	# 燃气锅炉最低运行负荷比例 = forms.CharField(initial = 0, label='燃气锅炉最低运行负荷比例',)

	# 余热锅炉
	余热锅炉效率 = forms.FloatField(initial = 0.95, label='余热锅炉效率', widget=forms.TextInput(attrs={'id': '余热锅炉效率', 'class': 'form-control form-control-sm'}))
	余热锅炉单位产汽耗电量 = forms.FloatField(initial = 2, label='余热锅炉单位产汽耗电量(kWh/t)', widget=forms.TextInput(attrs={'id': '余热锅炉单位产汽耗电量', 'class': 'form-control form-control-sm'}))
	冷却后烟气温度 = forms.FloatField(initial = 120, label='冷却后烟气温度(℃)', widget=forms.TextInput(attrs={'id': '冷却后烟气温度', 'class': 'form-control form-control-sm'}))

class Form_Invest(forms.Form):
	# 投资估算数据
	# 燃气轮机单位造价 = forms.FloatField(initial = 4900, label='燃气轮机单位造价', widget=forms.TextInput(attrs={'id': '燃气轮机单位造价', 'class': 'form-control form-control-sm'}))
	余热锅炉单位造价 = forms.FloatField(initial = 20, label='余热锅炉单位造价(万元/t)', widget=forms.TextInput(attrs={'id': '余热锅炉单位造价', 'class': 'form-control form-control-sm'}))
	# 燃气内燃机单位造价 = forms.FloatField(initial = 3500, label='燃气内燃机单位造价', widget=forms.TextInput(attrs={'id': '燃气内燃机单位造价', 'class': 'form-control form-control-sm'}))
	燃气锅炉单位造价 = forms.FloatField(initial = 13, label='燃气锅炉单位造价(万元/t)', widget=forms.TextInput(attrs={'id': '燃气锅炉单位造价', 'class': 'form-control form-control-sm'}))
	# 溴冷机单位造价
	# 螺杆机组单位造价

	# 燃气轮机安装费占设备费比例'] = 0.05
	# 燃气内燃机安装费占设备费比例'] = 0.05
	# 其他工艺安装费占设备费比例'] = 0.25
	#
	# 基本预备费占一二类总费用比例


	# 辅助设施设备占工艺系统总投资比例'] = 0.1
	# 辅助设施安装占辅助设施设备比例'] = 0.3
	# 电气工程系统设备占工艺系统总投资比例'] = 0.0833
	# 电气工程系统安装占电气工程系统设备比例'] = 0.2
	# 智能控制系统设备占工艺系统总投资比例'] = 0.0667
	# 智能控制系统安装占智能控制系统设备比例'] = 0.2

	# 管网投资安装占管网投资总费用比例'] = 0.5

	# # 投资估算设定值
	# 采用投资估算设定值赋值'] = '否'
	# 工艺系统_设备_设定值'] = 0
	# 工艺系统_安装_设定值'] = 0
	# 电气系统_设备_设定值'] = 0
	# 电气系统_安装_设定值'] = 0
	# 自控系统_设备_设定值'] = 0
	# 自控系统_安装_设定值'] = 0
	# 室外管网_设备_设定值'] = 0
	# 室外管网_安装_设定值'] = 0
	# 辅助工程_设备_设定值'] = 0
	# 辅助工程_安装_设定值'] = 0
	#
	# 设计费_设定值'] = 0
	# 设单位管理费_设定值'] = 0
	# 联合试运转费_设定值'] = 0
	# 办公及家具购置费_设定值'] = 0
	# 进场培训费_设定值'] = 0
	# 前期咨询费用_设定值'] = 0
	# 监理费_设定值'] = 0
	# 工程保险费_设定值'] = 0
	# 项目建设服务费_设定值'] = 0
	# 招投标费用_设定值'] = 0
	# 特种设备安全监督检验费_设定值'] = 0
	# 勘察费_设定值'] = 0
	# 设备采买费_设定值'] = 0

	# # 成本收入设定值
	# 采用成本收入设定值赋值'] = '否'
	# 供冷收入_设定值'] = 0
	# 供蒸汽收入_设定值'] = 0
	# 发电收入_设定值'] = 0
	# 供热收入_设定值'] = 0
	# 光伏发电收入_设定值'] = 0
	# 天然气销售收入_设定值'] = 0
	# 供冷配套费收入_设定值'] = 0
	# 供热配套费收入_设定值'] = 0
	# 光伏运维成本_设定值'] = 0
	# 天然气支出_设定值'] = 0
	# 水支出_设定值'] = 0
	# 电支出_设定值'] = 0
	# 维修费_设定值'] = 0

	# # 技经相关参数
	# 天然气是否先用后付'] = 0
	# 电费是否先用后付'] = 0
	# 水费是否先用后付'] = 0
	# 维修费是否先用后付'] = 0

	# # 尚未添加至GUI
	# 其他管理费用占工资比例'] = 0.5
	# 第一年达产率'] = 0.75
	#
	# 其他工艺设备维修费占比'] = 0.03
	# 辅助设施维修费占比'] = 0.03
	# 电气工程维修费占比'] = 0.01
	# 智能控制系统维修费占比'] = 0.01
	# 管网维修费占比'] = 0.015
	# 燃气轮机单位发电维修费'] = 0.06
	# 燃气内燃机单位发电维修费'] = 0.06
	# 维修费是否手动赋值'] = '否'
	# 维修费_设定值'] = 0
	#
	# 所得税率'] = 0.25
	# 还本起始年'] = 1
	# 借款比例'] = 0.7
	# 借款利率'] = 0.049
	# 还款周期'] = 7
	#
	# 冷增值税税率'] = 0.11
	# 蒸汽增值税税率'] = 0.11
	# 电增值税税率'] = 0.17
	# 建筑类残值率'] = 0.05
	# 设备及安装类残值率'] = 0.05
	# 气增值税税率'] = 0.11
	# 热增值税税率'] = 0.11
	# 水增值税税率'] = 0.11
	# 建筑费用增值税税率'] = 0.11
	# 设备费用增值税税率'] = 0.17
	# 安装费用增值税税率'] = 0.11
	# 工程建设其他费用增值税税率'] = 0.06
	# 电力接入费增值税税率'] = 0.17
	# 燃气工程费增值税税率'] = 0.17
	# 土地费用增值税税率'] = 0.06
	# 城市维护建设税率'] = 0.07
	# 教育附加税率'] = 0.05
	# 水利基金税率'] = 0
	# 应收账款周转次数'] = 12
	# 应付账款周转次数'] = 12
	# 天然气存货周转次数'] = 12
	# 电存货周转次数'] = 12
	# 水存货周转次数'] = 12
	# 维修费周转次数'] = 12
	# 是否备天然气存货'] = 0
	# 是否备电存货'] = 1
	# 是否备水存货'] = 1
	# 建筑类折旧年限'] = 20
	# 设备及安装类折旧年限'] = 15
	# 无形资产残值率'] = 0
	# 无形资产折旧年限'] = 20
	# 土地购置费残值率'] = 0
	# 土地购置费折旧年限'] = 20

# class WizardForm(forms.ModelForm):
# 	class Meta:
# 		model = ProjectInfo
# 		fields = ['项目名称']

class InvestmentParaForm(forms.Form):
	热力系统设备价格总和 = forms.FloatField(label='热力系统设备价格总和(万元)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	热力系统设备安装费总和 = forms.FloatField(label='热力系统设备安装费总和(万元)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	土建工程建筑费用 = forms.FloatField(label= '土建工程建筑费用(万元)', widget = forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	管网投资总费用 = forms.FloatField(label= '管网投资总费用(万元)', widget = forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	电力接入费 = forms.FloatField(label= '电力接入费(万元)', widget = forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	燃气工程费 = forms.FloatField(label= '燃气工程费(万元)', widget = forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	土地费 = forms.FloatField(label= '土地费(万元)', widget = forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	人数 = forms.IntegerField(label= '人数 (个)', widget = forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	收购费用 = forms.FloatField(label= '收购费用(万元)', widget = forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

class EconomicParaForm1(forms.Form):
	供冷量 = forms.FloatField(label='供冷量(万kWh)', widget=forms.TextInput(attrs={'id': '供冷量','class': 'form-control form-control-sm'}))
	供冷价格 = forms.FloatField(label='供冷价格(元/kWh)', widget=forms.TextInput(attrs={'id': '供冷价格','class': 'form-control form-control-sm'}))
	供蒸汽量 = forms.FloatField(label='供蒸汽量(万t)', widget=forms.TextInput(attrs={'id': '供蒸汽量', 'class': 'form-control form-control-sm'}))
	蒸汽价格 = forms.FloatField(label='蒸汽价格(元/t)', widget=forms.TextInput(attrs={'id': '蒸汽价格','class': 'form-control form-control-sm'}))
	售电量 = forms.FloatField(label='售电量(万kWh)', widget=forms.TextInput(attrs={'id': '售电量', 'class': 'form-control form-control-sm'}))
	售电价格 = forms.FloatField(label='售电价格(元/kWh)', widget=forms.TextInput(attrs={'id': '售电价格','class': 'form-control form-control-sm'}))
	供热量 = forms.FloatField(label='供热量(万kWh)', widget=forms.TextInput(attrs={'id': '供热量', 'class': 'form-control form-control-sm'}))
	供热价格 = forms.FloatField(label='供热价格(元/kWh)', widget=forms.TextInput(attrs={'id': '供热价格', 'class': 'form-control form-control-sm'}))
	光伏售电量 = forms.FloatField(label='光伏售电量(万kWh)', widget=forms.TextInput(attrs={'id': '光伏售电量', 'class': 'form-control form-control-sm'}))
	光伏售电价格 = forms.FloatField(label='光伏售电价格(元/kWh)', widget=forms.TextInput(attrs={'id': '光伏售电价格', 'class': 'form-control form-control-sm'}))
	天然气额外销售量 = forms.FloatField(label='天然气额外销售量(万方)', widget=forms.TextInput(attrs={'id': '天然气额外销售量', 'class': 'form-control form-control-sm'}))
	天然气额外销售价格 = forms.FloatField(label='天然气额外销售价格(元/方)', widget=forms.TextInput(attrs={'id': '天然气额外销售价格', 'class': 'form-control form-control-sm'}))
	# 供冷配套费收入 = forms.FloatField(label='供冷配套费收入(万元)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	# 供热配套费收入 = forms.FloatField(label='供热配套费收入(万元)', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

class EconomicParaForm2(forms.Form):
	天然气成本价格 = forms.FloatField(label='天然气成本价格(元/方)', widget=forms.TextInput(attrs={'id': '天然气成本价格', 'class': 'form-control form-control-sm'}))
	天然气耗量 = forms.FloatField(label='天然气耗量(万方)', widget=forms.TextInput(attrs={'id': '天然气耗量', 'class': 'form-control form-control-sm'}))
	水耗量 = forms.FloatField(label='水耗量(万t)', widget=forms.TextInput(attrs={'id': '水耗量', 'class': 'form-control form-control-sm'}))
	用水价格 = forms.FloatField(label='用水价格(元/t)', widget=forms.TextInput(attrs={'id': '用水价格', 'class': 'form-control form-control-sm'}))
	电耗量 = forms.FloatField(label='电耗量(万kWh)', widget=forms.TextInput(attrs={'id': '电耗量', 'class': 'form-control form-control-sm'}))
	用电价格 = forms.FloatField(label='用电价格(元/kWh)', widget=forms.TextInput(attrs={'id': '用电价格', 'class': 'form-control form-control-sm'}))
	土地租金 = forms.FloatField(label='土地租金(万元)', widget=forms.TextInput(attrs={'id': '土地租金', 'class': 'form-control form-control-sm'}))
	设备租金 = forms.FloatField(label='设备租金(万元)', widget=forms.TextInput(attrs={'id': '设备租金', 'class': 'form-control form-control-sm'}))
	维修费 = forms.FloatField(label='维修费(万元)', widget=forms.TextInput(attrs={'id': '维修费', 'class': 'form-control form-control-sm'}))
	工资及福利 = forms.FloatField(label='工资及福利(万元)', widget=forms.TextInput(attrs={'id': '工资及福利', 'class': 'form-control form-control-sm'}))
	变压器容量费 = forms.FloatField(label='变压器容量费(万元)', widget=forms.TextInput(attrs={'id': '变压器容量费', 'class': 'form-control form-control-sm'}))
	系统备用容量费 = forms.FloatField(label='系统备用容量费(万元)', widget=forms.TextInput(attrs={'id': '系统备用容量费', 'class': 'form-control form-control-sm'}))
	光伏运维成本 = forms.FloatField(label='光伏运维成本(万元)', widget=forms.TextInput(attrs={'id': '光伏运维成本', 'class': 'form-control form-control-sm'}))



class EconomicParaForm3(forms.Form):
	建筑费用 = forms.FloatField(label='I类费用_建筑费用总和(万元)', widget=forms.TextInput(attrs={'id': '建筑费用', 'class': 'form-control form-control-sm'}))
	设备费用 = forms.FloatField(label='I类费用_设备费用总和(万元)', widget=forms.TextInput(attrs={'id': '设备费用', 'class': 'form-control form-control-sm'}))
	安装费用 = forms.FloatField(label='I类费用_安装费用总和(万元)', widget=forms.TextInput(attrs={'id': '安装费用', 'class': 'form-control form-control-sm'}))
	土地费用 = forms.FloatField(label='土地购置费(万元)', widget=forms.TextInput(attrs={'id': '土地费用', 'class': 'form-control form-control-sm'}))
	建设单位管理费 = forms.FloatField(label='建设单位管理费(万元)', widget=forms.TextInput(attrs={'id': '建设单位管理费', 'class': 'form-control form-control-sm'}))
	工程建设其他费用总和 = forms.FloatField(label='工程建设其他费用总和(万元)', widget=forms.TextInput(attrs={'id': '工程建设其他费用总和', 'class': 'form-control form-control-sm'}))
	基本预备费 = forms.FloatField(label='基本预备费(万元)', widget=forms.TextInput(attrs={'id': '基本预备费', 'class': 'form-control form-control-sm'}))
	收购费用 = forms.FloatField(label='收购费用(万元)', widget=forms.TextInput(attrs={'id': '收购费用', 'class': 'form-control form-control-sm'}))
	建设投资 = forms.FloatField(label='建设投资(万元)', widget=forms.TextInput(attrs={'id': '建设投资', 'class': 'form-control form-control-sm'}))

class EconomicParaForm4(forms.Form):
	天然气支付模式列表 = [
		("1", "是"),
		("0", "否"),
	]

	天然气是否先用后付 = forms.ChoiceField(
		choices=天然气支付模式列表,
		initial=1,
		widget=widgets.Select(attrs={'id': '天然气是否先用后付', 'class': 'form-control form-control-sm'}),
		label='天然气是否先用后付',
	)

	电费支付模式列表 = [
		("1", "是"),
		("0", "否"),
	]

	电费是否先用后付 = forms.ChoiceField(
		choices=电费支付模式列表,
		initial=0,
		widget=widgets.Select(attrs={'id': '电费是否先用后付', 'class': 'form-control form-control-sm'}),
		label='电费是否先用后付',
	)

	水费支付模式列表 = [
		("1", "是"),
		("0", "否"),
	]

	水费是否先用后付 = forms.ChoiceField(
		choices=水费支付模式列表,
		initial=0,
		widget=widgets.Select(attrs={'id': '水费是否先用后付','class': 'form-control form-control-sm'}),
		label='水费是否先用后付',
	)

	工资支付模式列表 = [
		("1", "是"),
		("0", "否"),
	]

	工资是否先用后付 = forms.ChoiceField(
		choices=工资支付模式列表,
		initial=1,
		widget=widgets.Select(attrs={'id': '工资是否先用后付','class': 'form-control form-control-sm'}),
		label='工资是否先用后付',
	)

	维修费支付模式列表 = [
		("1", "是"),
		("0", "否"),
	]

	维修费是否先用后付 = forms.ChoiceField(
		choices=维修费支付模式列表,
		initial=1,
		widget=widgets.Select(attrs={'id': '维修费是否先用后付','class': 'form-control form-control-sm'}),
		label='维修费是否先用后付',
	)

class LHSX_Form(forms.Form):

	并网模式列表 = [
		("自发自用", "自发自用"),
		("全额上网", "全额上网"),
		("自发自用余电上网", "自发自用余电上网"),
	]

	并网模式 = forms.ChoiceField(
		choices=并网模式列表,
		initial=1,
		widget=widgets.Select(attrs={'id':'并网模式', 'class': 'form-control form-control-sm'}),
		label='并网模式',
	)

	燃气轮机最大台数 = forms.IntegerField(label='燃气轮机配置数量上限(台)', widget=forms.TextInput(attrs={'id':'燃气轮机最大台数', 'class': 'form-control form-control-sm'}))
	燃气轮机最大规模 = forms.FloatField(label='燃气轮机总装机规模上限(kW)', widget=forms.TextInput(attrs={'id':'燃气轮机最大规模', 'class': 'form-control form-control-sm'}))
	燃气轮机最小规模 = forms.FloatField(label='燃气轮机总装机规模下限(kW)', widget=forms.TextInput(attrs={'id':'燃气轮机最小规模', 'class': 'form-control form-control-sm'}))

	燃气内燃机最大台数 = forms.IntegerField(label='燃气内燃机配置数量上限(台)', widget=forms.TextInput(attrs={'id':'燃气内燃机最大台数', 'class': 'form-control form-control-sm'}))
	燃气内燃机最大规模 = forms.FloatField(label='燃气内燃机总装机规模上限(kW)', widget=forms.TextInput(attrs={'id':'燃气内燃机最大规模', 'class': 'form-control form-control-sm'}))
	燃气内燃机最小规模 = forms.FloatField(label='燃气内燃机总装机规模下限(kW)', widget=forms.TextInput(attrs={'id':'燃气内燃机最小规模', 'class': 'form-control form-control-sm'}))

