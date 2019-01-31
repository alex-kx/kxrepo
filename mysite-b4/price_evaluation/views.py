from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os, xlrd
from .models import DevicePrice
# Create your views here.
def insert_price_data(request):
	data = xlrd.open_workbook(os.path.join(os.path.dirname(__file__),"device_price_table.xlsx"))
	table = data.sheet_by_name('Sheet1')
	n_rows = table.nrows,
	for i in range(n_rows[0])[1:]:
		device = table.row_values(i)[0]
		unit = table.row_values(i)[1]
		lower_limit = table.row_values(i)[2]
		upper_limit = table.row_values(i)[3]
		ref_unit_price = table.row_values(i)[4]
		ref_installation_fee = table.row_values(i)[5]
		try:
			price_field_obj = DevicePrice.objects.get(device=device, unit=unit,lower_limit=lower_limit, upper_limit=upper_limit, ref_unit_price=ref_unit_price, ref_installation_fee=ref_installation_fee)
		except:
			price_field_obj = DevicePrice(device=device, unit=unit,lower_limit=lower_limit, upper_limit=upper_limit, ref_unit_price=ref_unit_price, ref_installation_fee=ref_installation_fee)
			price_field_obj.save()
			print("insert new record")
	return HttpResponse("success")

def price_evaluation(request):
	return render(request, 'price_evaluation/price_evaluation.html')

def retrieve_ref_price(request):
	device = request.POST.get('device')
	capacity = request.POST.get('capacity')
	try:
		obj = DevicePrice.objects.get(device=device, lower_limit__lte =capacity, upper_limit__gt=capacity)
		unit = obj.unit
		ref_unit_price = obj.ref_unit_price
		ref_installation_fee = obj.ref_installation_fee
		print(unit,ref_unit_price,ref_installation_fee)
		return JsonResponse({
			"success": "True",
			"unit": unit,
			"ref_unit_price": ref_unit_price,
			"ref_installation_fee": ref_installation_fee,
		})
	except:
		return JsonResponse({"success":"false"})

