from .Gas_Turbine import 燃气轮机类
from .Internal_engine import 燃气内燃机类
from .Gas_boiler import 燃气锅炉类


def 设备对象工厂(数据, 设备样本):
	if 设备样本['名称'] == '燃气轮机':
		return 燃气轮机类('燃气轮机', 数据, 设备样本, 设备样本['锅炉额定产汽量'])
	elif 设备样本['名称'] == '燃气内燃机':
		return 燃气内燃机类('燃气内燃机', 数据, 设备样本, 设备样本['锅炉额定产汽量'])
	elif 设备样本['名称'] == '燃气锅炉':
		return 燃气锅炉类('燃气锅炉', 数据, 锅炉额定产汽量=设备样本['锅炉额定产汽量'])