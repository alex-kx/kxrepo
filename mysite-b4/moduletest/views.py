from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, redirect
import xlrd
import copy
from moduletest.forms import UserForm, UploadExcelForm, UploadExcelForm2, Form2, Form_FirstPage, Form_basic, Form_Machine, Form_Invest, WizardForm, \
	ProjectInfoForm, InvestmentParaForm, EconomicParaForm1, EconomicParaForm2 , EconomicParaForm3, EconomicParaForm4, LHSX_Form
from .energysolution.Data import 数据类
from .energysolution.Sample import 设备样本类
from .energysolution.Configuration_combinations import 配置组合类
from .energysolution.Operation import 全年运行方案
from .energysolution.lianghuashaixuan import 量化筛选类
from .energysolution.Input_Output import 能源投入产出类
from .energysolution.Investment_assessment import 投资估算类
from .energysolution.economic import 技经计算类
from .energysolution.Steam_solutions import 供蒸汽方案

import json
import os
import io
import math
from django import forms
import openpyxl as pyxl
from openpyxl.styles import PatternFill,Border,Side,Alignment,Protection,Font
from urllib import parse
from .energysolution import Machine_factory

from .models import Load, ProjectInfo, LHSX_ProjectInfo
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms import widgets  # 插件
# Create your views here.

def index(request):
	return render(request, 'moduletest/index.html')

def registration(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		try:
			User_obj = User.objects.get(username = username)
			return HttpResponse('用户已注册!!!')
		except:
			User_obj = User.objects.create(username=username, password=password, email=email)
			User_obj.set_password(password)
			User_obj.save()
			return redirect('/moduletest/login')

	if request.method == 'GET':
		return render(request, 'moduletest/registration.html')

def Login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect( '../SolutionComparison')

	if request.method == 'GET':
		return render(request, 'moduletest/login.html')

@login_required
def logout(request):
	auth.logout(request)
	return redirect("/moduletest/login/")

def 供蒸汽方案筛选燃气轮机(数据, 燃气轮机样本列表, 蒸汽负荷, 燃气轮机最小规模, 燃气轮机最大规模):
	筛选后的设备样本列表 = []
	for 燃气轮机样本 in 燃气轮机样本列表:
		if 燃气轮机样本['锅炉额定产汽量'] == 0:
			筛选后的设备样本列表.append([燃气轮机样本])
		else:
			for i in range(数据.数据索引['燃气轮机最大台数']):
				台数 = i + 1
				if 燃气轮机样本['锅炉额定产汽量'] * 台数 <= 1.1 * 蒸汽负荷 and 燃气轮机最小规模 <= 燃气轮机样本['发电功率'] * 台数 and 燃气轮机样本['发电功率'] * 台数 <= 燃气轮机最大规模:
					筛选后的设备样本列表.append([燃气轮机样本] * 台数)
	return 筛选后的设备样本列表

def GasTurbineFilter(request):
	str_list = []
	if '蒸汽负荷' in request.POST and '燃气轮机最小规模' in request.POST and '燃气轮机最大规模' in request.POST:
		数据 = 数据类()
		设备样本库 = 设备样本类(数据)
		燃气轮机样本列表 = 设备样本库.燃气轮机样本列表
		蒸汽负荷 = float(request.POST['蒸汽负荷'])
		燃气轮机最小规模 = float(request.POST['燃气轮机最小规模'])
		燃气轮机最大规模 = float(request.POST['燃气轮机最大规模'])

		筛选后的设备样本列表 = 供蒸汽方案筛选燃气轮机(数据, 燃气轮机样本列表, 蒸汽负荷, 燃气轮机最小规模, 燃气轮机最大规模)

		for 设备样本组 in 筛选后的设备样本列表:
			temp_list = []
			for 设备样本 in 设备样本组:
				temp_list.append(设备样本['名称'] + ':' + str(round(设备样本['锅炉额定产汽量'], 2)))
			str_list.append(temp_list)

		context = {'filter_list': str_list,}
		return render(request, 'moduletest/GasTurbineFilter.html', context)
	else:
		return render(request, 'moduletest/GasTurbineFilter.html')


def 供蒸汽方案筛选燃气内燃机(数据, 燃气内燃机样本列表, 蒸汽负荷, 燃气内燃机最小规模, 燃气内燃机最大规模):
	筛选后的设备样本列表 = []
	for 燃气内燃机样本 in 燃气内燃机样本列表:
		if 燃气内燃机样本['锅炉额定产汽量'] == 0:
			筛选后的设备样本列表.append([燃气内燃机样本])
		else:
			for i in range(数据.数据索引['燃气内燃机最大台数']):
				台数 = i + 1
				if 燃气内燃机样本['锅炉额定产汽量'] * 台数 <= 1.1 * 蒸汽负荷 and 燃气内燃机最小规模 <= 燃气内燃机样本['发电功率'] * 台数 and 燃气内燃机样本['发电功率'] * 台数 <= 燃气内燃机最大规模:
					筛选后的设备样本列表.append([燃气内燃机样本] * 台数)
	return 筛选后的设备样本列表


def InternalEngineFilter(request):
	str_list = []
	if '蒸汽负荷' in request.POST and '燃气内燃机最小规模' in request.POST and '燃气内燃机最大规模' in request.POST:
		数据 = 数据类()
		设备样本库 = 设备样本类(数据)
		燃气内燃机样本列表 = 设备样本库.燃气内燃机样本列表

		蒸汽负荷 = float(request.POST['蒸汽负荷'])
		燃气内燃机最小规模 = float(request.POST['燃气内燃机最小规模'])
		燃气内燃机最大规模 = float(request.POST['燃气内燃机最大规模'])

		筛选后的设备样本列表 = 供蒸汽方案筛选燃气内燃机(数据, 燃气内燃机样本列表, 蒸汽负荷, 燃气内燃机最小规模, 燃气内燃机最大规模)

		for 设备样本组 in 筛选后的设备样本列表:
			temp_list = []
			for 设备样本 in 设备样本组:
				temp_list.append(设备样本['名称'] + ':' + str(round(设备样本['锅炉额定产汽量'], 2)))
			str_list.append(temp_list)

		context = {'filter_list': str_list,}

		return render(request, 'moduletest/InternalEngineFilter.html', context)
	else:
		return render(request, 'moduletest/InternalEngineFilter.html')


def 供蒸汽方案筛选燃气锅炉(蒸汽负荷):
	筛选后的设备样本列表 = []
	燃气锅炉样本 = {'名称': '燃气锅炉', '锅炉额定产汽量': math.ceil(蒸汽负荷)  }
	筛选后的设备样本列表.append([燃气锅炉样本])
	return 筛选后的设备样本列表

def get_excel_stream(file):
	# StringIO操作的只能是str，如果要操作二进制数据，就需要使用BytesIO。
	excel_stream = io.BytesIO()
	# 这点很重要，传给save函数的不是保存文件名，而是一个BytesIO流（在内存中读写）
	file.save(excel_stream)
	# getvalue方法用于获得写入后的byte将结果返回给re
	res = excel_stream.getvalue()
	excel_stream.close()
	return res

@login_required
def ConfigurationCombination(request):
	if '蒸汽负荷' in request.POST and '燃气内燃机最小规模' in request.POST and '燃气内燃机最大规模' in request.POST and '燃气轮机最小规模' in request.POST and '燃气轮机最大规模' in request.POST:
		数据 = 数据类()
		蒸汽负荷 = float(request.POST['蒸汽负荷'])
		数据.数据索引['燃气轮机最小规模'] = float(request.POST['燃气轮机最小规模'])
		数据.数据索引['燃气轮机最大规模'] = float(request.POST['燃气轮机最大规模'])
		数据.数据索引['燃气内燃机最小规模'] = float(request.POST['燃气内燃机最小规模'])
		数据.数据索引['燃气内燃机最大规模'] = float(request.POST['燃气内燃机最大规模'])


		技术路线列表 = ['燃气轮机', '燃气内燃机', '燃气锅炉']
		量化筛选 = 配置组合类(数据, 蒸汽负荷,  技术路线列表)
		配置方案列表 = 量化筛选.配置方案列表

		str_list = []
		for 配置方案 in 配置方案列表:
			temp_list = []
			for 设备样本 in 配置方案:
				if 设备样本['名称'] == '燃气轮机' or 设备样本['名称'] == '燃气内燃机':
					temp_list.append(str(设备样本['发电功率']) + 'kW ' + str(设备样本['名称'])  +  '\n' +  str(设备样本['公司型号']) +  '\n' + '产汽量:' +  str(round(设备样本['锅炉额定产汽量'], 2) ) + 't/h')
				else:
					temp_list.append(设备样本['名称']   + '\n' +  '产汽量:' + str(round(设备样本['锅炉额定产汽量'], 2)) + 't/h')
			str_list.append(temp_list)

		context = {
			'combination_list': str_list,
			'lastTime' : request.POST,
			'data' : 数据.数据索引,
				   }
		return render(request, 'moduletest/ConfigurationCombination.html', context)
	else:

		# wb = pyxl.Workbook()
		# res = get_excel_stream(wb)
		# response = HttpResponse(content_type='application/vnd.ms-excel')
		# response['Content-Disposition'] = 'attachment;filename=' + "excel_name" + '.xlsx'
		# response.write(res)
		# return response

		return render(request, 'moduletest/ConfigurationCombination.html')

@login_required
def LoadDataUpload(request):
	if request.method == 'GET':
		obj1 = UploadExcelForm2()
		context = {
			'obj1': obj1
		}

		return render(request, 'moduletest/LoadDataUpload.html', context)

	if request.method == 'POST':
		obj1 = UploadExcelForm2(request.POST, request.FILES)
		if obj1.is_valid():
			context = {
				'obj1':obj1
			}
			print('loading')
			wb = xlrd.open_workbook(
				filename=None, file_contents=request.FILES['excel'].read())  # 关键点在于这里
			sheet_load = wb.sheets()[0]
			蒸汽负荷list = sheet_load.col_values(colx=0, start_rowx=1, end_rowx=8761)
			电负荷list = sheet_load.col_values(colx=1, start_rowx=1, end_rowx=8761)
			市政电价list = sheet_load.col_values(colx=5, start_rowx=1, end_rowx=25)
			上网电价list = sheet_load.col_values(colx=6, start_rowx=1, end_rowx=25)
			内部售电价list = sheet_load.col_values(colx=7, start_rowx=1, end_rowx=25)

			负荷文件名称 = request.POST.get('负荷数据名称')
			print(负荷文件名称)
			蒸汽负荷str = ""
			for i in 蒸汽负荷list:
				蒸汽负荷str += (',' + str(i))

			电负荷str = ""
			for i in 电负荷list:
				电负荷str += (',' + str(i))

			市政电价str = ""
			for i in 市政电价list:
				市政电价str += (',' + str(i))

			上网电价str = ""
			for i in 上网电价list:
				上网电价str += (',' + str(i))

			内部售电价str = ""
			for i in 内部售电价list:
				内部售电价str += (',' + str(i))

			# 负荷数据 = Load(负荷文件名称=负荷文件名称, steam_load=蒸汽负荷str, electricity_load=电负荷str, 市政电价 = 市政电价str, 上网电价 = 上网电价str, 内部售电价 = 内部售电价str)
			# 负荷数据.save()

			try:
				项目参数 = LHSX_ProjectInfo.objects.get(项目名称 = 负荷文件名称, username=request.user.username)
				项目参数.steam_load = 蒸汽负荷str
				项目参数.electricity_load = 电负荷str
				项目参数.市政电价 = 市政电价str
				项目参数.上网电价 = 上网电价str
				项目参数.内部售电价 = 内部售电价str
				项目参数.save()
				print("overwrite")
			except:
				项目参数 = LHSX_ProjectInfo(username=request.user.username, 项目名称=负荷文件名称, steam_load=蒸汽负荷str, electricity_load=电负荷str, 市政电价 = 市政电价str, 上网电价 = 上网电价str, 内部售电价 = 内部售电价str)
				项目参数.save()
				print("new write")

			try:
				负荷数据 = Load.objects.get(负荷文件名称__exact = 负荷文件名称, username=request.user.username)
				负荷数据.steam_load = 蒸汽负荷str
				负荷数据.electricity_load = 电负荷str
				负荷数据.市政电价 = 市政电价str
				负荷数据.上网电价 = 上网电价str
				负荷数据.内部售电价 = 内部售电价str
				负荷数据.save()
				print("overwrite")
			except:
				负荷数据 = Load(username=request.user.username, 负荷文件名称=负荷文件名称, steam_load=蒸汽负荷str, electricity_load=电负荷str, 市政电价 = 市政电价str, 上网电价 = 上网电价str, 内部售电价 = 内部售电价str)
				负荷数据.save()
				print("new write")

			return redirect( '/moduletest/SolutionComparison')

@login_required
def OperatingStrategy(request):
	if request.method == 'GET':
		数据 = 数据类()
		设备样本库 = 设备样本类(数据)
		发电机型号列表 = []
		发电机样本列表 = 设备样本库.燃气轮机样本列表 + 设备样本库.燃气内燃机样本列表
		for 样本 in 发电机样本列表:
			发电机型号列表.append(样本['公司型号'])
		context = {
			'发电机型号列表': 发电机型号列表
		}
		obj1 = UploadExcelForm()

		负荷数据列表 = []
		try:
			负荷数据set = Load.objects.all()
			for 负荷数据 in 负荷数据set:
				负荷数据列表.append(负荷数据.负荷文件名称)
		except:
			pass
		context['负荷数据列表'] = 负荷数据列表
		context['obj1'] = obj1

	if request.method == 'POST':
		print(request.POST.get('test'))
		数据 = 数据类()
		数据.数据索引['水蒸气焓差'] = float(request.POST.get('水蒸气焓差'))
		数据.数据索引['余热锅炉效率'] = float(request.POST.get('余热锅炉效率'))
		设备样本库 = 设备样本类(数据)
		发电机型号列表 = []
		发电机样本列表 = 设备样本库.燃气轮机样本列表 + 设备样本库.燃气内燃机样本列表
		for 样本 in 发电机样本列表:
			发电机型号列表.append(样本['公司型号'])
		context = {
			'发电机型号列表': 发电机型号列表
		}
		负荷数据列表 = []
		try:
			负荷数据set = Load.objects.all()
			for 负荷数据 in 负荷数据set:
				负荷数据列表.append(负荷数据.负荷文件名称)
		except:
			pass
		context['负荷数据列表'] = 负荷数据列表

		obj1 = UploadExcelForm(request.POST)
		if obj1.is_valid():

			print('loading')

			负荷文件名称 = request.POST.get('负荷数据')
			print(负荷文件名称)
			context['负荷文件名称'] = json.dumps(负荷文件名称)

			负荷数据 = Load.objects.get(负荷文件名称__exact = 负荷文件名称)
			蒸汽负荷list = 字符串转列表(负荷数据.steam_load)
			电负荷list = 字符串转列表(负荷数据.electricity_load)
			市政电价list = 字符串转列表(负荷数据.市政电价)
			上网电价list = 字符串转列表(负荷数据.上网电价)
			内部售电价list = 字符串转列表(负荷数据.内部售电价)
			负荷数据.save()


			数据.数据索引['蒸汽负荷'] = 蒸汽负荷list
			数据.数据索引['电负荷'] = 电负荷list
			数据.数据索引['市政电价'] = 市政电价list * 365
			数据.数据索引['上网电价'] = 上网电价list * 365
			数据.数据索引['内部售电价'] = 内部售电价list * 365
			context['obj1'] = obj1

			数据.数据索引['燃气价格'] = float(request.POST.get('燃气价格'))
			数据.数据索引['蒸汽价格'] = float(request.POST.get('蒸汽价格'))
			数据.数据索引['燃气热值'] = float(request.POST.get('燃气热值'))

			数据.数据索引['燃气轮机满负荷运行小时数限制'] = float(request.POST.get('燃气轮机满负荷运行小时数限制'))
			数据.数据索引['燃气内燃机满负荷运行小时数限制'] = float(request.POST.get('燃气内燃机满负荷运行小时数限制'))
			数据.数据索引['燃气锅炉效率'] = float(request.POST.get('燃气锅炉效率'))



			数据.数据索引['并网模式'] = request.POST.get('并网模式')
			发电机型号 = request.POST.get('发电机型号选择')
			发电机样本 = 设备样本库.选择发电机样本(发电机型号)

			发电机设备 = Machine_factory.设备对象工厂(数据, 发电机样本)
			context['发电机功率'] = 发电机设备.发电机规模
			发电机台数 = int(request.POST.get('发电机台数'))
			设备列表 = [发电机设备] * 发电机台数

			发电机总产汽量 = 0
			for 设备 in 设备列表:
				发电机总产汽量 += 设备.锅炉额定产汽量

			燃气锅炉需解决负荷 = max(蒸汽负荷list) - 发电机总产汽量

			if 燃气锅炉需解决负荷 > 0:
				燃气锅炉样本 = {
					'名称':'燃气锅炉',
					'锅炉额定产汽量': 燃气锅炉需解决负荷
				}
				设备列表.append(Machine_factory.设备对象工厂(数据, 燃气锅炉样本))

			if 发电机总产汽量 > 0:
				备用燃气锅炉样本 = {
					'名称': '燃气锅炉',
					'锅炉额定产汽量': 发电机总产汽量
				}
				备用燃气锅炉 = Machine_factory.设备对象工厂(数据, 备用燃气锅炉样本)
				备用燃气锅炉.是否为备用锅炉 = True
				设备列表.append(备用燃气锅炉)

			for 设备 in 设备列表:
				print(设备.锅炉额定产汽量)

			全年产蒸汽运行方案 = 全年运行方案(数据, 设备列表)
			投入产出 = 能源投入产出类(数据, 设备列表)
			结果显示索引列表 = 投入产出.结果显示索引列表
			结果表头列表 = []
			结果数据列表 = []
			for k, v  in 结果显示索引列表.items():
				结果表头列表.append(k)
				结果数据列表.append(v)

			context['结果表头列表'] = 结果表头列表
			context['结果数据列表'] = 结果数据列表

			print(结果显示索引列表)
			发电机发电量列表 = 全年产蒸汽运行方案.发电机发电量列表
			发电机运行列表 = 全年产蒸汽运行方案.发电机运行列表
			燃气锅炉运行列表 = 全年产蒸汽运行方案.燃气锅炉运行列表
			备用燃气锅炉运行列表 = 全年产蒸汽运行方案.备用燃气锅炉运行列表
			运行收益列表 = 全年产蒸汽运行方案.运行收益列表

			for i in range(8760):
				蒸汽负荷list[i] = round(蒸汽负荷list[i] , 2)
				发电机发电量列表[i] = round(发电机发电量列表[i], 2)
				发电机运行列表[i] = round(发电机运行列表[i], 2)
				燃气锅炉运行列表[i] = round(燃气锅炉运行列表[i], 2)
				备用燃气锅炉运行列表[i] = round(备用燃气锅炉运行列表[i], 2)
				运行收益列表[i] = round(运行收益列表[i], 2)

			时刻列表 = [i+1 for i in range(8760)]
			输出量列表 = zip(时刻列表, 蒸汽负荷list, 电负荷list, 发电机发电量列表, 数据.数据索引['市政电价'], 数据.数据索引['上网电价'], 数据.数据索引['内部售电价'], 发电机运行列表, 燃气锅炉运行列表, 备用燃气锅炉运行列表, 运行收益列表)

			context['蒸汽负荷'] = 蒸汽负荷list
			context['发电机运行列表'] = 发电机运行列表
			context['燃气锅炉运行列表'] = 燃气锅炉运行列表
			context['备用燃气锅炉运行列表'] = 备用燃气锅炉运行列表
			context['时间'] = 时刻列表
			context['输出量列表'] = 输出量列表

	return render(request, 'moduletest/OperatingStrategy.html', context)


def 字符串转列表(str):
	temp_list = str.split(',')
	temp_list.pop(0)
	for index, item in enumerate(temp_list):
		temp_list[index] = round(float(item), 4)
	return temp_list


@login_required
def Wizard(request):
	if request.method == 'GET':
		obj1 = WizardForm()
		项目信息set = ProjectInfo.objects.all()
		项目名称列表 = []
		for 项目信息 in 项目信息set:
			项目名称列表.append(项目信息.项目名称)

		context = {
			'obj1': obj1,
			'项目名称列表': 项目名称列表
		}
		return render(request, 'moduletest/Wizard.html', context)

	if request.method == 'POST':
		obj1 = WizardForm(request.POST, request.FILES)
		if obj1.is_valid():
			context = {
				'obj1': obj1
			}
			print('loading')
			wb = xlrd.open_workbook(
				filename=None, file_contents=request.FILES['excel'].read())  # 关键点在于这里
			sheet_load = wb.sheets()[0]
			蒸汽负荷list = sheet_load.col_values(colx=0, start_rowx=1, end_rowx=8761)
			电负荷list = sheet_load.col_values(colx=1, start_rowx=1, end_rowx=8761)
			市政电价list = sheet_load.col_values(colx=5, start_rowx=1, end_rowx=25)
			上网电价list = sheet_load.col_values(colx=6, start_rowx=1, end_rowx=25)
			内部售电价list = sheet_load.col_values(colx=7, start_rowx=1, end_rowx=25)

			项目名称 = request.POST.get('项目名称')

			蒸汽负荷str = ""
			for i in 蒸汽负荷list:
				蒸汽负荷str += (',' + str(i))

			电负荷str = ""
			for i in 电负荷list:
				电负荷str += (',' + str(i))

			市政电价str = ""
			for i in 市政电价list:
				市政电价str += (',' + str(i))

			上网电价str = ""
			for i in 上网电价list:
				上网电价str += (',' + str(i))

			内部售电价str = ""
			for i in 内部售电价list:
				内部售电价str += (',' + str(i))

			try:
				项目信息 = Load.objects.get(项目名称__exact = 项目名称)
				项目信息.steam_load = 蒸汽负荷str
				项目信息.electricity_load = 电负荷str
				项目信息.市政电价 = 市政电价str
				项目信息.上网电价 = 上网电价str
				项目信息.内部售电价 = 内部售电价str
				项目信息.save()
				print("overwrite")
			except:
				项目信息 = ProjectInfo(项目名称 = 项目名称, steam_load=蒸汽负荷str, electricity_load=电负荷str, 市政电价=市政电价str, 上网电价=上网电价str,
							内部售电价=内部售电价str)
				项目信息.save()
				print("new write")

		return render(request, 'moduletest/OperatingStrategy02.html', context)

@login_required
def InvestmentAssessment(request):

	if request.method == 'GET':
		form1 = InvestmentParaForm()
		context = {
			'form1':form1
		}
		return render(request, 'moduletest/InvestmentAssessment.html', context)

	if request.method == 'POST':
		form1 = InvestmentParaForm(request.POST)
		context = {
			'form1': form1,
		}
		if form1.is_valid():
			数据  = 数据类()
			土建工程建筑费用 = float(request.POST.get('土建工程建筑费用'))  * 10000
			管网投资总费用 = float(request.POST.get('管网投资总费用'))  *  10000
			电力接入费 = float(request.POST.get('电力接入费'))  *  10000
			燃气工程费 = float(request.POST.get('燃气工程费'))  *  10000
			土地费 = float(request.POST.get('土地费'))  *  10000
			人数 = float(request.POST.get('人数'))
			收购费用 = float(request.POST.get('收购费用'))  *  10000
			热力系统设备价格总和 = float(request.POST.get('热力系统设备价格总和'))  *  10000
			热力系统设备安装费总和 = float(request.POST.get('热力系统设备安装费总和'))  *  10000

			数据.数据索引['土建工程建筑'] = 土建工程建筑费用
			数据.数据索引['管网投资总费用'] = 管网投资总费用
			数据.数据索引['电力接入费'] = 电力接入费
			数据.数据索引['燃气工程费'] = 燃气工程费
			数据.数据索引['土地费'] = 土地费
			数据.数据索引['人数'] = 人数
			数据.数据索引['收购费用'] = 收购费用

			投资估算 = 投资估算类(热力系统总设备价格 = 热力系统设备价格总和, 热力系统总设备安装费 = 热力系统设备安装费总和, 数据 = 数据, 是否有电力接入费 = True)

			context['投资估算结果'] = 投资估算.投资估算结果array

		return render(request, 'moduletest/InvestmentAssessment.html', context)

@login_required
def Economic(request):

	if request.method == 'GET':
		form1 = EconomicParaForm1()
		form2 = EconomicParaForm2()
		form3 = EconomicParaForm3()
		form4 = EconomicParaForm4()
		context = {
			'达产率': [1] * 20,
			'form1': form1,
			'form2': form2,
			'form3': form3,
			'form4': form4,
		}
		return render(request, 'moduletest/Economic.html', context)

	if request.method == 'POST':

		form1 =  EconomicParaForm1(request.POST)
		form2 = EconomicParaForm2(request.POST)
		form3 = EconomicParaForm3(request.POST)
		form4 = EconomicParaForm4(request.POST)
		context = {
			'form1': form1,
			'form2': form2,
			'form3': form3,
			'form4': form4,
		}
		if form1.is_valid() and form2.is_valid() and form3.is_valid():
			数据  = 数据类()

			成本收入索引 = dict()
			成本收入索引['供冷收入'] = float(request.POST.get('供冷量'))  * 10000 * float(request.POST.get('供冷价格'))
			成本收入索引['蒸汽收入'] = float(request.POST.get('供蒸汽量'))  * 10000 * float(request.POST.get('蒸汽价格'))
			成本收入索引['售电收入'] = float(request.POST.get('售电量'))  * 10000 * float(request.POST.get('售电价格'))
			成本收入索引['供热收入'] = float(request.POST.get('供热量'))  * 10000 * float(request.POST.get('供热价格'))
			成本收入索引['光伏发电收入'] = float(request.POST.get('光伏售电量'))  * 10000 * float(request.POST.get('光伏售电价格'))
			数据.数据索引['额外天然气销售年总收入'] = float(request.POST.get('天然气额外销售量'))  * 10000 * float(request.POST.get('天然气额外销售价格'))
			# 数据.数据索引['供冷配套费收入'] = float(request.POST.get('供冷配套费收入'))  * 10000
			# 数据.数据索引['供热配套费收入'] = float(request.POST.get('供热配套费收入'))  * 10000

			数据.数据索引['天然气是否先用后付'] = int(request.POST.get('天然气是否先用后付'))
			数据.数据索引['电费是否先用后付'] = int(request.POST.get('电费是否先用后付'))
			数据.数据索引['水费是否先用后付'] = int(request.POST.get('水费是否先用后付'))
			数据.数据索引['工资是否先用后付'] = int(request.POST.get('工资是否先用后付'))
			数据.数据索引['维修费是否先用后付'] = int(request.POST.get('维修费是否先用后付'))
			# 数据.数据索引['第一年达产率'] = float(request.POST.get('第一年达产率'))
			达产率 = request.POST.get('达产率').split(',')
			达产率.pop(-1)
			context['达产率'] = 达产率
			for i, value in enumerate(达产率):
				达产率[i] = float(value)
			数据.数据索引['达产率'] = [0] + 达产率



			成本收入索引['工资及福利'] = float(request.POST.get('工资及福利'))  * 10000
			成本收入索引['光伏运维成本'] = float(request.POST.get('光伏运维成本'))  * 10000
			数据.数据索引['额外天然气销售年总成本'] = float(request.POST.get('天然气额外销售量')) * 10000 *  float(request.POST.get('天然气成本价格'))
			成本收入索引['燃气费'] = float(request.POST.get('天然气耗量'))  * 10000 *  float(request.POST.get('天然气成本价格'))
			成本收入索引['水费'] = float(request.POST.get('水耗量'))  * 10000 *  float(request.POST.get('用水价格'))
			成本收入索引['电费'] = float(request.POST.get('电耗量'))  * 10000 *  float(request.POST.get('用电价格'))
			数据.数据索引['变压器容量费'] = float(request.POST.get('变压器容量费'))  * 10000
			数据.数据索引['系统备用容量费'] = float(request.POST.get('系统备用容量费'))  * 10000
			数据.数据索引['土地租金'] = float(request.POST.get('土地租金'))  * 10000
			数据.数据索引['设备租金'] = float(request.POST.get('设备租金'))  * 10000
			维修费 = float(request.POST.get('维修费'))  * 10000

			工程费用索引 = {
				'工程费用':dict()
			}
			工程建设其他费用索引 = dict()
			工程费用索引['工程费用']['建筑'] = float(request.POST.get('建筑费用'))  * 10000
			工程费用索引['工程费用']['设备'] = float(request.POST.get('设备费用'))  * 10000
			工程费用索引['工程费用']['安装'] = float(request.POST.get('安装费用'))  * 10000
			工程建设其他费用索引['土地费'] = float(request.POST.get('土地费用'))  * 10000
			工程建设其他费用索引['建设单位管理费'] = float(request.POST.get('建设单位管理费'))  * 10000
			工程建设其他费用索引['工程建设其他费用合计'] = float(request.POST.get('工程建设其他费用总和'))  * 10000
			基本预备费 = float(request.POST.get('基本预备费'))  * 10000
			收购费用 = float(request.POST.get('收购费用'))  * 10000
			建设投资 = float(request.POST.get('建设投资'))  * 10000

			技经计算 = 技经计算类(数据, 成本收入索引, 工程费用索引, 工程建设其他费用索引, 基本预备费, 收购费用, 建设投资, 维修费)
			context['技经计算结果'] = 技经计算.技经计算结果
			context['技经计算明细列表'] = 技经计算.技经计算明细列表

		return render(request, 'moduletest/Economic.html', context)

@login_required
def economicAjax(request):
	数据 = 数据类()
	成本收入索引 = dict()
	成本收入索引['供冷收入'] = float(request.POST.get('供冷量')) * 10000 * float(request.POST.get('供冷价格'))
	成本收入索引['蒸汽收入'] = float(request.POST.get('供蒸汽量')) * 10000 * float(request.POST.get('蒸汽价格'))
	成本收入索引['售电收入'] = float(request.POST.get('售电量')) * 10000 * float(request.POST.get('售电价格'))
	成本收入索引['供热收入'] = float(request.POST.get('供热量')) * 10000 * float(request.POST.get('供热价格'))
	成本收入索引['光伏发电收入'] = float(request.POST.get('光伏售电量')) * 10000 * float(request.POST.get('光伏售电价格'))
	数据.数据索引['额外天然气销售年总收入'] = float(request.POST.get('天然气额外销售量')) * 10000 * float(request.POST.get('天然气额外销售价格'))
	# 数据.数据索引['供冷配套费收入'] = float(request.POST.get('供冷配套费收入'))  * 10000
	# 数据.数据索引['供热配套费收入'] = float(request.POST.get('供热配套费收入'))  * 10000

	数据.数据索引['天然气是否先用后付'] = int(request.POST.get('天然气是否先用后付'))
	数据.数据索引['电费是否先用后付'] = int(request.POST.get('电费是否先用后付'))
	数据.数据索引['水费是否先用后付'] = int(request.POST.get('水费是否先用后付'))
	数据.数据索引['工资是否先用后付'] = int(request.POST.get('工资是否先用后付'))
	数据.数据索引['维修费是否先用后付'] = int(request.POST.get('维修费是否先用后付'))
	# 数据.数据索引['第一年达产率'] = float(request.POST.get('第一年达产率'))
	达产率 = request.POST.get('达产率').split(',')
	print(达产率)
	达产率.pop(-1)
	for i, value in enumerate(达产率):
		达产率[i] = float(value)
	数据.数据索引['达产率'] = [0] + 达产率
	print(len(数据.数据索引['达产率']))

	成本收入索引['工资及福利'] = float(request.POST.get('工资及福利')) * 10000
	成本收入索引['光伏运维成本'] = float(request.POST.get('光伏运维成本')) * 10000
	数据.数据索引['额外天然气销售年总成本'] = float(request.POST.get('天然气额外销售量')) * 10000 * float(request.POST.get('天然气成本价格'))
	成本收入索引['燃气费'] = float(request.POST.get('天然气耗量')) * 10000 * float(request.POST.get('天然气成本价格'))
	成本收入索引['水费'] = float(request.POST.get('水耗量')) * 10000 * float(request.POST.get('用水价格'))
	成本收入索引['电费'] = float(request.POST.get('电耗量')) * 10000 * float(request.POST.get('用电价格'))
	数据.数据索引['变压器容量费'] = float(request.POST.get('变压器容量费')) * 10000
	数据.数据索引['系统备用容量费'] = float(request.POST.get('系统备用容量费')) * 10000
	数据.数据索引['土地租金'] = float(request.POST.get('土地租金')) * 10000
	数据.数据索引['设备租金'] = float(request.POST.get('设备租金')) * 10000
	维修费 = float(request.POST.get('维修费')) * 10000

	工程费用索引 = {
		'工程费用': dict()
	}
	工程建设其他费用索引 = dict()
	工程费用索引['工程费用']['建筑'] = float(request.POST.get('建筑费用')) * 10000
	工程费用索引['工程费用']['设备'] = float(request.POST.get('设备费用')) * 10000
	工程费用索引['工程费用']['安装'] = float(request.POST.get('安装费用')) * 10000
	工程建设其他费用索引['土地费'] = float(request.POST.get('土地费用')) * 10000
	工程建设其他费用索引['建设单位管理费'] = float(request.POST.get('建设单位管理费')) * 10000
	工程建设其他费用索引['工程建设其他费用合计'] = float(request.POST.get('工程建设其他费用总和')) * 10000
	基本预备费 = float(request.POST.get('基本预备费')) * 10000
	收购费用 = float(request.POST.get('收购费用')) * 10000
	建设投资 = float(request.POST.get('建设投资')) * 10000

	最小值 = round(float(request.POST.get('最小值')),3)
	最大值 = round(float(request.POST.get('最大值')),3)
	步长 = round(float(request.POST.get('步长')),3)
	计算列表长度 = int((最大值 - 最小值) / 步长) + 1
	计算列表 = [最小值 + i * 步长 for i in range(计算列表长度)]
	技经计算结果列表 = []

	if request.POST.get('变量选择') == '设备租金':
		for i in 计算列表:
			数据.数据索引['设备租金'] = i * 10000
			技经计算 = 技经计算类(数据, 成本收入索引, 工程费用索引, 工程建设其他费用索引, 基本预备费, 收购费用, 建设投资, 维修费)
			技经计算结果列表.append(技经计算.技经计算结果json)

	if request.POST.get('变量选择') == '土地租金':
		for i in 计算列表:
			数据.数据索引['土地租金'] = i * 10000
			技经计算 = 技经计算类(数据, 成本收入索引, 工程费用索引, 工程建设其他费用索引, 基本预备费, 收购费用, 建设投资, 维修费)
			技经计算结果列表.append(技经计算.技经计算结果json)

	if request.POST.get('变量选择') == '天然气成本价格':
		for i in 计算列表:
			数据.数据索引['额外天然气销售年总成本'] = float(request.POST.get('天然气额外销售量')) * 10000 * i
			成本收入索引['燃气费'] = float(request.POST.get('天然气耗量')) * 10000 * i
			技经计算 = 技经计算类(数据, 成本收入索引, 工程费用索引, 工程建设其他费用索引, 基本预备费, 收购费用, 建设投资, 维修费)
			技经计算结果列表.append(技经计算.技经计算结果json)

	if request.POST.get('变量选择') == '天然气额外销售价格':
		for i in 计算列表:
			数据.数据索引['额外天然气销售年总收入'] = float(request.POST.get('天然气额外销售量')) * 10000 * i
			技经计算 = 技经计算类(数据, 成本收入索引, 工程费用索引, 工程建设其他费用索引, 基本预备费, 收购费用, 建设投资, 维修费)
			技经计算结果列表.append(技经计算.技经计算结果json)

	if request.POST.get('变量选择') == '光伏售电价格':
		for i in 计算列表:
			成本收入索引['光伏发电收入'] = float(request.POST.get('光伏售电量')) * 10000 * i
			技经计算 = 技经计算类(数据, 成本收入索引, 工程费用索引, 工程建设其他费用索引, 基本预备费, 收购费用, 建设投资, 维修费)
			技经计算结果列表.append(技经计算.技经计算结果json)

	if request.POST.get('变量选择') == '蒸汽价格':
		for i in 计算列表:
			成本收入索引['蒸汽收入'] = float(request.POST.get('供蒸汽量')) * 10000 * i
			技经计算 = 技经计算类(数据, 成本收入索引, 工程费用索引, 工程建设其他费用索引, 基本预备费, 收购费用, 建设投资, 维修费)
			技经计算结果列表.append(技经计算.技经计算结果json)

	if request.POST.get('变量选择') == '供热价格':
		for i in 计算列表:
			成本收入索引['供热收入'] = float(request.POST.get('供热量')) * 10000 * i
			技经计算 = 技经计算类(数据, 成本收入索引, 工程费用索引, 工程建设其他费用索引, 基本预备费, 收购费用, 建设投资, 维修费)
			技经计算结果列表.append(技经计算.技经计算结果json)

	if request.POST.get('变量选择') == '供冷价格':
		for i in 计算列表:
			成本收入索引['供冷收入'] = float(request.POST.get('供冷量')) * 10000 * i
			技经计算 = 技经计算类(数据, 成本收入索引, 工程费用索引, 工程建设其他费用索引, 基本预备费, 收购费用, 建设投资, 维修费)
			技经计算结果列表.append(技经计算.技经计算结果json)

	if request.POST.get('变量选择') == '售电价格':
		for i in 计算列表:
			成本收入索引['售电收入'] = float(request.POST.get('售电量')) * 10000 * i
			技经计算 = 技经计算类(数据, 成本收入索引, 工程费用索引, 工程建设其他费用索引, 基本预备费, 收购费用, 建设投资, 维修费)
			技经计算结果列表.append(技经计算.技经计算结果json)

	for index, value in enumerate(计算列表):
		计算列表[index] = round(value, 3)

	技经计算结果列表filtered = []
	计算列表filtered = []
	for i, 计算结果 in enumerate(技经计算结果列表):
		if math.isnan(计算结果['iRR']) or math.isnan(计算结果['netValue']):
			pass
		else:
			技经计算结果列表filtered.append(计算结果)
			计算列表filtered.append(计算列表[i])

	return JsonResponse({
		'技经计算结果列表': 技经计算结果列表filtered,
		'x': 计算列表filtered,
	})

@login_required
def SteamSolution(request):
	if request.method == 'GET':
		负荷数据列表 = []
		try:
			负荷数据set = Load.objects.filter(username=request.user.username)
			for 负荷数据 in 负荷数据set:
				负荷数据列表.append(负荷数据.负荷文件名称)
		except:
			print("get load data from database failed")

		Form_FirstPage_obj = Form_FirstPage()
		Form_basic_obj = Form_basic()
		Form_Machine_obj = Form_Machine()
		Form_Invest_obj = Form_Invest()
		context = {
			'负荷数据列表' : 负荷数据列表,
			'Form_FirstPage_obj': Form_FirstPage_obj,
			'Form_basic_obj': Form_basic_obj,
			'Form_Machine_obj': Form_Machine_obj,
			'Form_Invest_obj': Form_Invest_obj,
		}
		return render(request, 'moduletest/SteamSolution.html', context)

	if request.method == 'POST':
		负荷数据列表 = []
		try:
			负荷数据set = Load.objects.filter(username=request.user.username)
			for 负荷数据 in 负荷数据set:
				负荷数据列表.append(负荷数据.负荷文件名称)
		except:
			pass



		Form_FirstPage_obj = Form_FirstPage(request.POST)
		Form_basic_obj = Form_basic(request.POST)
		Form_Machine_obj = Form_Machine(request.POST)
		Form_Invest_obj = Form_Invest(request.POST)

		context = {
			'负荷数据列表': 负荷数据列表,
			'Form_FirstPage_obj': Form_FirstPage_obj,
			'Form_basic_obj': Form_basic_obj,
			'Form_Machine_obj': Form_Machine_obj,
			'Form_Invest_obj': Form_Invest_obj,
		}

		if Form_FirstPage_obj.is_valid() and Form_basic_obj.is_valid() and Form_Machine_obj.is_valid() and Form_Invest_obj.is_valid():
			数据 = 数据类()
			数据.数据索引['余热锅炉效率'] = float(request.POST.get('余热锅炉效率'))
			数据.数据索引['冷却后烟气温度'] = float(request.POST.get('冷却后烟气温度'))
			数据.数据索引['水蒸气焓差'] = float(request.POST.get('水蒸气焓差'))
			数据.数据索引['燃气轮机发电效率修正'] = float(request.POST.get('燃气轮机发电效率修正'))
			数据.数据索引['燃气轮机烟气流量修正'] = float(request.POST.get('燃气轮机烟气流量修正'))
			数据.数据索引['燃气轮机排烟温度修正'] = float(request.POST.get('燃气轮机排烟温度修正'))
			数据.数据索引['燃气轮机发电功率修正'] = float(request.POST.get('燃气轮机发电功率修正'))

			设备样本库 = 设备样本类(数据)

			负荷文件名称 = request.POST.get('负荷数据')
			context['负荷文件名称'] = json.dumps(负荷文件名称)
			负荷数据 = Load.objects.get(负荷文件名称__exact = 负荷文件名称)
			蒸汽负荷list = 字符串转列表(负荷数据.steam_load)
			电负荷list = 字符串转列表(负荷数据.electricity_load)
			市政电价list = 字符串转列表(负荷数据.市政电价)
			上网电价list = 字符串转列表(负荷数据.上网电价)
			内部售电价list = 字符串转列表(负荷数据.内部售电价)
			负荷数据.save()

			数据.数据索引['管损率'] = float(request.POST.get('管损率'))
			for i, 蒸汽负荷 in enumerate(蒸汽负荷list):
				蒸汽负荷list[i] = 蒸汽负荷list[i] / (1 - 数据.数据索引['管损率'])
			数据.数据索引['蒸汽负荷'] = 蒸汽负荷list
			数据.数据索引['电负荷'] = 电负荷list
			数据.数据索引['市政电价'] = 市政电价list * 365
			数据.数据索引['上网电价'] = 上网电价list * 365
			数据.数据索引['内部售电价'] = 内部售电价list * 365

			数据.数据索引['并网模式'] = request.POST.get('并网模式')

			参数列表 = [
				'燃气价格',
				'水价格',
				'蒸汽价格',
				'额外天然气销售年总收入',
				'额外天然气销售年总成本',
				'人数',
				'工资',
				# 其他基础数据
				'土建工程建筑',
				'管网投资总费用',
				'燃气热值',

				'管损率',
				# '自耗电自供应比例',

				# 量化筛选计算控制
				# '燃气轮机最大规模',
				# '燃气轮机最小规模',
				# '燃气内燃机最大规模',
				# '燃气内燃机最小规模',
				# '燃气轮机最大台数',
				# '燃气内燃机最大台数',

				# 燃气锅炉
				'燃气锅炉单位产汽耗电量',
				'锅炉耗水率',
				'燃气锅炉效率',
				# '燃气锅炉满负荷运行小时数限制',
				# '燃气锅炉最低运行负荷比例',

				# 余热锅炉
				'余热锅炉效率',
				'余热锅炉单位产汽耗电量',
				'冷却后烟气温度',

				# 燃气轮机
				'燃气轮机满负荷运行小时数限制',
				'燃气轮机自耗电比例',
				'燃气轮机最低运行负荷比例',

				# 燃气内燃机
				'燃气内燃机满负荷运行小时数限制',
				'燃气内燃机自耗电比例',
				'燃气内燃机最低运行负荷比例',

				# 投资估算数据
				# '燃气轮机单位造价',
				'余热锅炉单位造价',
				# '燃气内燃机单位造价',
				'燃气锅炉单位造价',

				'辅助工程_设备_设定值',
				'辅助工程_安装_设定值',

				'电力接入费',
				'土地费',
				'燃气工程费',
				'收购费用',

				'变压器容量费',
				'系统备用容量费',
				'土地租金',
				'设备租金',
			]


			for 参数索引 in 参数列表:
				数据.数据索引[参数索引] = float(request.POST.get(参数索引))

			发电机型号 = request.POST.get('发电机型号选择')
			发电机样本 = 设备样本库.选择发电机样本(发电机型号)
			print(发电机样本)
			发电机设备 = Machine_factory.设备对象工厂(数据, 发电机样本)
			context['发电机功率'] = 发电机设备.发电机规模
			发电机台数 = int(request.POST.get('发电机台数'))
			设备列表 = [发电机设备] * 发电机台数

			发电机总产汽量 = 0
			for 设备 in 设备列表:
				发电机总产汽量 += 设备.锅炉额定产汽量

			燃气锅炉需解决负荷 = max(蒸汽负荷list) - 发电机总产汽量

			if 燃气锅炉需解决负荷 > 0:
				燃气锅炉样本 = {
					'名称':'燃气锅炉',
					'锅炉额定产汽量': 燃气锅炉需解决负荷
				}
				设备列表.append(Machine_factory.设备对象工厂(数据, 燃气锅炉样本))

			if 发电机总产汽量 > 0:
				备用燃气锅炉样本 = {
					'名称': '燃气锅炉',
					'锅炉额定产汽量': 发电机总产汽量
				}
				备用燃气锅炉 = Machine_factory.设备对象工厂(数据, 备用燃气锅炉样本)
				备用燃气锅炉.是否为备用锅炉 = True
				设备列表.append(备用燃气锅炉)

			蒸汽方案 = 供蒸汽方案(数据, 设备列表)
			投入产出 = 蒸汽方案.能源投入产出
			全年产蒸汽运行方案 = 蒸汽方案.全年运行方案
			投资估算 = 蒸汽方案.投资估算
			技经计算 = 蒸汽方案.技经计算


			context['设备配置'] = 蒸汽方案.设备配置str
			context['投入产出索引列表'] = 投入产出.结果显示索引列表
			context['技经计算结果'] = 技经计算.技经计算结果
			context['投资估算结果'] = 投资估算.投资估算结果array
			context['技经计算明细列表'] = 技经计算.技经计算明细列表
			context['全年运行情况列表'] = 全年产蒸汽运行方案.全年运行情况列表


			发电机运行列表 = 全年产蒸汽运行方案.发电机运行列表
			燃气锅炉运行列表 = 全年产蒸汽运行方案.燃气锅炉运行列表
			备用燃气锅炉运行列表 = 全年产蒸汽运行方案.备用燃气锅炉运行列表
			时刻列表 = [i + 1 for i in range(8760)]

			context['蒸汽负荷'] = 蒸汽负荷list
			context['发电机运行列表'] = 发电机运行列表
			context['燃气锅炉运行列表'] = 燃气锅炉运行列表
			context['备用燃气锅炉运行列表'] = 备用燃气锅炉运行列表
			context['时间'] = 时刻列表

		return render(request, 'moduletest/SteamSolution.html', context)

@login_required
def SolutionComparison(request):
	if request.method == 'GET':
		负荷数据列表 = []
		try:
			负荷数据set = Load.objects.filter(username=request.user.username)
			for 负荷数据 in 负荷数据set:
				负荷数据列表.append(负荷数据.负荷文件名称)
		except:
			print("get load data from database failed")

		LHSX_Form_obj = LHSX_Form()
		Form_basic_obj = Form_basic()
		Form_Machine_obj = Form_Machine()
		Form_Invest_obj = Form_Invest()
		EconomicParaForm4_obj = EconomicParaForm4()
		context = {
			'负荷数据列表' : 负荷数据列表,
			'LHSX_Form_obj': LHSX_Form_obj,
			'Form_basic_obj': Form_basic_obj,
			'Form_Machine_obj': Form_Machine_obj,
			'Form_Invest_obj': Form_Invest_obj,
			'EconomicParaForm4_obj': EconomicParaForm4_obj,
		}
		return render(request, 'moduletest/SolutionComparison.html', context)

	if request.method == 'POST':
		负荷数据列表 = []
		try:
			负荷数据set = Load.objects.filter(username=request.user.username)
			for 负荷数据 in 负荷数据set:
				负荷数据列表.append(负荷数据.负荷文件名称)
		except:
			pass



		LHSX_Form_obj = LHSX_Form(request.POST)
		Form_basic_obj = Form_basic(request.POST)
		Form_Machine_obj = Form_Machine(request.POST)
		Form_Invest_obj = Form_Invest(request.POST)
		EconomicParaForm4_obj = EconomicParaForm4(request.POST)

		context = {
			'负荷数据列表': 负荷数据列表,
			'LHSX_Form_obj': LHSX_Form_obj,
			'Form_basic_obj': Form_basic_obj,
			'Form_Machine_obj': Form_Machine_obj,
			'Form_Invest_obj': Form_Invest_obj,
			'EconomicParaForm4_obj': EconomicParaForm4_obj,
		}

		if LHSX_Form_obj.is_valid() and Form_basic_obj.is_valid() and Form_Machine_obj.is_valid() and Form_Invest_obj.is_valid() and EconomicParaForm4_obj:
			数据 = 数据类()
			数据.数据索引['余热锅炉效率'] = float(request.POST.get('余热锅炉效率'))
			数据.数据索引['冷却后烟气温度'] = float(request.POST.get('冷却后烟气温度'))
			数据.数据索引['水蒸气焓差'] = float(request.POST.get('水蒸气焓差'))
			数据.数据索引['燃气轮机发电效率修正'] = float(request.POST.get('燃气轮机发电效率修正'))
			数据.数据索引['燃气轮机烟气流量修正'] = float(request.POST.get('燃气轮机烟气流量修正'))
			数据.数据索引['燃气轮机排烟温度修正'] = float(request.POST.get('燃气轮机排烟温度修正'))
			数据.数据索引['燃气轮机发电功率修正'] = float(request.POST.get('燃气轮机发电功率修正'))

			设备样本库 = 设备样本类(数据)

			负荷文件名称 = request.POST.get('负荷数据')
			context['负荷文件名称'] = json.dumps(负荷文件名称)
			负荷数据 = Load.objects.get(负荷文件名称__exact = 负荷文件名称, username=request.user.username)
			蒸汽负荷list = 字符串转列表(负荷数据.steam_load)
			电负荷list = 字符串转列表(负荷数据.electricity_load)
			市政电价list = 字符串转列表(负荷数据.市政电价)
			上网电价list = 字符串转列表(负荷数据.上网电价)
			内部售电价list = 字符串转列表(负荷数据.内部售电价)
			负荷数据.save()

			数据.数据索引['管损率'] = float(request.POST.get('管损率'))
			for i, 蒸汽负荷 in enumerate(蒸汽负荷list):
				蒸汽负荷list[i] = 蒸汽负荷list[i] / (1 - 数据.数据索引['管损率'])
			数据.数据索引['蒸汽负荷'] = 蒸汽负荷list
			数据.数据索引['电负荷'] = 电负荷list
			数据.数据索引['市政电价'] = 市政电价list * 365
			数据.数据索引['上网电价'] = 上网电价list * 365
			数据.数据索引['内部售电价'] = 内部售电价list * 365

			达产率 = request.POST.get('达产率').split(',')
			达产率.pop(-1)
			for i, value in enumerate(达产率):
				达产率[i] = float(value)
			数据.数据索引['达产率'] = [0] + 达产率

			数据.数据索引['并网模式'] = request.POST.get('并网模式')
			数据.数据索引['燃气价格'] = float(request.POST.get('燃气价格'))
			数据.数据索引['水价格'] = float(request.POST.get('水价格'))
			数据.数据索引['蒸汽价格'] = float(request.POST.get('蒸汽价格'))
			数据.数据索引['额外天然气销售年总收入'] = float(request.POST.get('额外天然气销售年总收入')) * 10000
			数据.数据索引['额外天然气销售年总成本'] = float(request.POST.get('额外天然气销售年总成本')) * 10000
			数据.数据索引['人数'] = float(request.POST.get('人数'))
			数据.数据索引['工资'] = float(request.POST.get('工资')) * 10000

			数据.数据索引['土建工程建筑'] = float(request.POST.get('土建工程建筑'))* 10000
			数据.数据索引['管网投资总费用'] = float(request.POST.get('管网投资总费用'))* 10000
			数据.数据索引['燃气热值'] = float(request.POST.get('燃气热值'))

			数据.数据索引['管损率'] = float(request.POST.get('管损率'))

			数据.数据索引['燃气轮机最大规模'] = float(request.POST.get('燃气轮机最大规模'))
			数据.数据索引['燃气轮机最小规模'] = float(request.POST.get('燃气轮机最小规模'))
			数据.数据索引['燃气内燃机最大规模'] = float(request.POST.get('燃气内燃机最大规模'))
			数据.数据索引['燃气内燃机最小规模'] = float(request.POST.get('燃气内燃机最小规模'))
			数据.数据索引['燃气轮机最大台数'] = float(request.POST.get('燃气轮机最大台数'))
			数据.数据索引['燃气内燃机最大台数'] = float(request.POST.get('燃气内燃机最大台数'))


			数据.数据索引['燃气锅炉单位产汽耗电量'] = float(request.POST.get('燃气锅炉单位产汽耗电量'))
			数据.数据索引['锅炉耗水率'] = float(request.POST.get('锅炉耗水率'))
			数据.数据索引['燃气锅炉效率'] = float(request.POST.get('燃气锅炉效率'))

			数据.数据索引['余热锅炉效率'] = float(request.POST.get('余热锅炉效率'))
			数据.数据索引['余热锅炉单位产汽耗电量'] = float(request.POST.get('余热锅炉单位产汽耗电量'))
			数据.数据索引['冷却后烟气温度'] = float(request.POST.get('冷却后烟气温度'))

			数据.数据索引['燃气轮机满负荷运行小时数限制'] = float(request.POST.get('燃气轮机满负荷运行小时数限制'))
			数据.数据索引['燃气轮机自耗电比例'] = float(request.POST.get('燃气轮机自耗电比例'))
			数据.数据索引['燃气轮机最低运行负荷比例'] = float(request.POST.get('燃气轮机最低运行负荷比例'))

			数据.数据索引['燃气内燃机满负荷运行小时数限制'] = float(request.POST.get('燃气内燃机满负荷运行小时数限制'))
			数据.数据索引['燃气内燃机自耗电比例'] = float(request.POST.get('燃气内燃机自耗电比例'))
			数据.数据索引['燃气内燃机最低运行负荷比例'] = float(request.POST.get('燃气内燃机最低运行负荷比例'))

			数据.数据索引['余热锅炉单位造价'] = float(request.POST.get('余热锅炉单位造价')) * 10000
			数据.数据索引['燃气锅炉单位造价'] = float(request.POST.get('燃气锅炉单位造价')) * 10000

			数据.数据索引['辅助工程_设备_设定值'] = float(request.POST.get('辅助工程_设备_设定值')) * 10000
			数据.数据索引['辅助工程_安装_设定值'] = float(request.POST.get('辅助工程_安装_设定值')) * 10000

			数据.数据索引['电力接入费'] = float(request.POST.get('电力接入费')) * 10000
			数据.数据索引['土地费'] = float(request.POST.get('土地费')) * 10000
			数据.数据索引['燃气工程费'] = float(request.POST.get('燃气工程费')) * 10000
			数据.数据索引['收购费用'] = float(request.POST.get('收购费用')) * 10000

			数据.数据索引['变压器容量费'] = float(request.POST.get('变压器容量费')) * 10000
			数据.数据索引['系统备用容量费'] = float(request.POST.get('系统备用容量费')) * 10000
			数据.数据索引['土地租金'] = float(request.POST.get('土地租金')) * 10000
			数据.数据索引['设备租金'] = float(request.POST.get('设备租金')) * 10000

			数据.数据索引['天然气是否先用后付'] = float(request.POST.get('天然气是否先用后付'))
			数据.数据索引['电费是否先用后付'] = float(request.POST.get('电费是否先用后付'))
			数据.数据索引['水费是否先用后付'] = float(request.POST.get('水费是否先用后付'))
			数据.数据索引['维修费是否先用后付'] = float(request.POST.get('维修费是否先用后付'))
			数据.数据索引['工资是否先用后付'] = float(request.POST.get('工资是否先用后付'))


			量化筛选 = 量化筛选类(数据)

			输出结果 = []
			方案标识列表 = []
			建设投资列表 = []
			利润总额列表 = []
			内部收益率列表 = []
			投资回收期列表 = []
			for 方案 in 量化筛选.方案列表:
				方案标识列表.append(方案.设备配置string)
				建设投资列表.append(方案.指标索引['建设投资/万'])
				利润总额列表.append(方案.指标索引['利润总额/万'])
				内部收益率列表.append(方案.指标索引['内部收益率'])
				投资回收期列表.append(方案.指标索引['投资回收期/年'])
				输出结果.append(方案.结果列表)

			表头 = [
				'设备配置',
				'建设投资(万元)',
				'年均销售收入(万元)',
				'年均总成本费用(万元)',
				'年均利润总额(万元)',
				'投资回收期',
				'内部收益率_税后',

				'等效满负荷运行小时数(h)',
				
				'发电量/万kWh',
				'外购电量/万kWh',
				'自耗电量/万kWh',
				'售电量/万kWh',
				'产汽量/万t',
				'售汽量/万t',
				'耗气量/万方',
				'耗水量',
				'蒸汽收入/万元',
				'售电收入/万万',
				'燃气费/万元',
				'电费/万元',
				'水费/万元',
			]

			context['表头'] = 表头
			context['输出结果'] = 输出结果
			context['方案标识列表'] = [i+1  for i in range(len(量化筛选.方案列表))]
			context['建设投资列表'] = 建设投资列表
			context['利润总额列表'] = 利润总额列表
			context['内部收益率列表'] = 内部收益率列表
			context['投资回收期列表'] = 投资回收期列表

		return render(request, 'moduletest/SolutionComparison.html', context)

def loadProjectInfo(request):
	项目名称 = request.POST.get('项目名称')
	项目参数 = LHSX_ProjectInfo.objects.get(项目名称 = 项目名称,  username=request.user.username)

	达产率 = 项目参数.达产率.split(',')
	达产率.pop(-1)
	for i, value in enumerate(达产率):
		达产率[i] = float(value)

	return JsonResponse({
		'达产率': 达产率,

		'并网模式': 项目参数.并网模式,
		'燃气轮机最大台数': 项目参数.燃气轮机最大台数,
		'燃气轮机最大规模': 项目参数.燃气轮机最大规模,
		'燃气轮机最小规模': 项目参数.燃气轮机最小规模,
		'燃气内燃机最大台数': 项目参数.燃气内燃机最大台数,
		'燃气内燃机最大规模': 项目参数.燃气内燃机最大规模,
		'燃气内燃机最小规模': 项目参数.燃气内燃机最小规模,

		'燃气价格': 项目参数.燃气价格,
		'水价格': 项目参数.水价格,
		'蒸汽价格': 项目参数.蒸汽价格,
		'燃气热值': 项目参数.燃气热值,
		'管损率': 项目参数.管损率,
		'水蒸气焓差': 项目参数.水蒸气焓差,
		'土建工程建筑': 项目参数.土建工程建筑,
		'管网投资总费用': 项目参数.管网投资总费用,
		'辅助工程_设备_设定值': 项目参数.辅助工程_设备_设定值,
		'辅助工程_安装_设定值': 项目参数.辅助工程_安装_设定值,
		'电力接入费': 项目参数.电力接入费,
		'燃气工程费': 项目参数.燃气工程费,
		'土地费': 项目参数.土地费,
		'收购费用': 项目参数.收购费用,
		'人数': 项目参数.人数,
		'工资': 项目参数.工资,
		'变压器容量费': 项目参数.变压器容量费,
		'系统备用容量费': 项目参数.系统备用容量费,
		'土地租金': 项目参数.土地租金,
		'设备租金': 项目参数.设备租金,
		'额外天然气销售年总收入': 项目参数.额外天然气销售年总收入,
		'额外天然气销售年总成本': 项目参数.额外天然气销售年总成本,
		'燃气轮机满负荷运行小时数限制': 项目参数.燃气轮机满负荷运行小时数限制,
		'燃气轮机自耗电比例': 项目参数.燃气轮机自耗电比例,
		'燃气轮机最低运行负荷比例': 项目参数.燃气轮机最低运行负荷比例,
		'燃气轮机发电效率修正': 项目参数.燃气轮机发电效率修正,
		'燃气轮机烟气流量修正': 项目参数.燃气轮机烟气流量修正,
		'燃气轮机排烟温度修正': 项目参数.燃气轮机排烟温度修正,
		'燃气轮机发电功率修正': 项目参数.燃气轮机发电功率修正,
		'燃气内燃机满负荷运行小时数限制': 项目参数.燃气内燃机满负荷运行小时数限制,
		'燃气内燃机自耗电比例': 项目参数.燃气内燃机自耗电比例,
		'燃气内燃机最低运行负荷比例': 项目参数.燃气内燃机最低运行负荷比例,
		'燃气锅炉单位产汽耗电量': 项目参数.燃气锅炉单位产汽耗电量,
		'锅炉耗水率': 项目参数.锅炉耗水率,
		'燃气锅炉效率': 项目参数.燃气锅炉效率,
		'余热锅炉效率': 项目参数.余热锅炉效率,
		'余热锅炉单位产汽耗电量': 项目参数.余热锅炉单位产汽耗电量,
		'冷却后烟气温度': 项目参数.冷却后烟气温度,
		'余热锅炉单位造价': 项目参数.余热锅炉单位造价,
		'燃气锅炉单位造价': 项目参数.燃气锅炉单位造价,
		'天然气是否先用后付': 项目参数.天然气是否先用后付,
		'电费是否先用后付': 项目参数.电费是否先用后付,
		'水费是否先用后付': 项目参数.水费是否先用后付,
		'工资是否先用后付': 项目参数.工资是否先用后付,
		'维修费是否先用后付': 项目参数.维修费是否先用后付,
	})

def saveProjectInfo(request):

	try:
		obj = LHSX_ProjectInfo.objects.get(项目名称 = request.POST.get('项目名称'), username = request.user.username)
	except:
		obj = LHSX_ProjectInfo(项目名称=request.POST.get('项目名称'), username=request.user.username)

	obj.达产率 = request.POST.get('达产率')

	obj.并网模式 = request.POST.get('并网模式')
	obj.燃气轮机最大台数 = request.POST.get('燃气轮机最大台数')
	obj.燃气轮机最大规模 = request.POST.get('燃气轮机最大规模')
	obj.燃气轮机最小规模 = request.POST.get('燃气轮机最小规模')
	obj.燃气内燃机最大台数 = request.POST.get('燃气内燃机最大台数')
	obj.燃气内燃机最大规模 = request.POST.get('燃气内燃机最大规模')
	obj.燃气内燃机最小规模 = request.POST.get('燃气内燃机最小规模')

	obj.燃气价格 = request.POST.get('燃气价格')
	obj.水价格 = request.POST.get('水价格')
	obj.蒸汽价格 = request.POST.get('蒸汽价格')
	obj.燃气热值 = request.POST.get('燃气热值')
	obj.管损率 = request.POST.get('管损率')
	obj.水蒸气焓差 = request.POST.get('水蒸气焓差')
	obj.土建工程建筑 = request.POST.get('土建工程建筑')
	obj.管网投资总费用 = request.POST.get('管网投资总费用')
	obj.辅助工程_设备_设定值 = request.POST.get('辅助工程_设备_设定值')
	obj.辅助工程_安装_设定值 = request.POST.get('辅助工程_安装_设定值')
	obj.电力接入费 = request.POST.get('电力接入费')
	obj.燃气工程费 = request.POST.get('燃气工程费')
	obj.土地费 = request.POST.get('土地费')
	obj.收购费用 = request.POST.get('收购费用')
	obj.人数 = request.POST.get('人数')
	obj.工资 = request.POST.get('工资')
	obj.变压器容量费 = request.POST.get('变压器容量费')
	obj.系统备用容量费 = request.POST.get('系统备用容量费')
	obj.土地租金 = request.POST.get('土地租金')
	obj.设备租金 = request.POST.get('设备租金')
	obj.额外天然气销售年总收入 = request.POST.get('额外天然气销售年总收入')
	obj.额外天然气销售年总成本 = request.POST.get('额外天然气销售年总成本')
	obj.燃气轮机满负荷运行小时数限制 = request.POST.get('燃气轮机满负荷运行小时数限制')
	obj.燃气轮机自耗电比例 = request.POST.get('燃气轮机自耗电比例')
	obj.燃气轮机最低运行负荷比例 = request.POST.get('燃气轮机最低运行负荷比例')
	obj.燃气轮机发电效率修正 = request.POST.get('燃气轮机发电效率修正')
	obj.燃气轮机烟气流量修正 = request.POST.get('燃气轮机烟气流量修正')
	obj.燃气轮机排烟温度修正 = request.POST.get('燃气轮机排烟温度修正')
	obj.燃气轮机发电功率修正 = request.POST.get('燃气轮机发电功率修正')
	obj.燃气内燃机满负荷运行小时数限制 = request.POST.get('燃气内燃机满负荷运行小时数限制')
	obj.燃气内燃机自耗电比例 = request.POST.get('燃气内燃机自耗电比例')
	obj.燃气内燃机最低运行负荷比例 = request.POST.get('燃气内燃机最低运行负荷比例')
	obj.燃气锅炉单位产汽耗电量 = request.POST.get('燃气锅炉单位产汽耗电量')
	obj.锅炉耗水率 = request.POST.get('锅炉耗水率')
	obj.燃气锅炉效率 = request.POST.get('燃气锅炉效率')
	obj.余热锅炉效率 = request.POST.get('余热锅炉效率')
	obj.余热锅炉单位产汽耗电量 = request.POST.get('余热锅炉单位产汽耗电量')
	obj.冷却后烟气温度 = request.POST.get('冷却后烟气温度')
	obj.余热锅炉单位造价 = request.POST.get('余热锅炉单位造价')
	obj.燃气锅炉单位造价 = request.POST.get('燃气锅炉单位造价')
	obj.天然气是否先用后付 = request.POST.get('天然气是否先用后付')
	obj.电费是否先用后付 = request.POST.get('电费是否先用后付')
	obj.水费是否先用后付 = request.POST.get('水费是否先用后付')
	obj.工资是否先用后付 = request.POST.get('工资是否先用后付')
	obj.维修费是否先用后付 = request.POST.get('维修费是否先用后付')

	obj.save()

	return JsonResponse({'success': 'success'})