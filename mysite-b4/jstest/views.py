from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext
import xlrd
from django.views.decorators.csrf import csrf_exempt


def detail(request):
	return render(request, 'jstest/index.html')

def bootstrap(request):
	return render(request, 'jstest/bootstrap.html')

def index(req):
	发电机台数 = req.POST.get('input1')
	print(发电机台数)
	return JsonResponse({'发电机台数': 发电机台数})


def UploadExcel(request):
	return render(request, 'jstest/index.html')
	# return HttpResponse("hahahaha" + 蒸汽负荷list)

def  echartstest(request):
	context = {
		'data1' : [1,2,3,4,5,6,7,8]
	}
	return render(request, 'jstest/hc.html', context)
