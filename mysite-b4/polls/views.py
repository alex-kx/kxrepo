
from django.http import HttpResponse, JsonResponse

from django.http import Http404
from django.shortcuts import render, redirect
from .models import Question, Choice, Employee, Project, Blog, Author, Entry, ProjectRecord
import json

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Max,Avg,F,Q, Sum
from django.core import serializers
import xlrd
import os
# Create your views here.



def index(request):
	# results = Project.objects.filter(project_member__employee_name='黄凯欣')
	# results = Employee.objects.filter(project__project_name='湖北钟祥泛能微网项目')
	# proj1 = Project.objects.all()[0]

	# result1 = ProjectRecord.objects.filter(member_name='黄凯欣', project_name='湖北钟祥泛能微网项目')
	result1 = ProjectRecord.objects.filter(project_name__project_name = '湖北钟祥泛能微网项目')
	week_Num_list = []
	working_days_list = []
	for item in result1:
		week_Num_list.append(item.week_Num)
		working_days_list.append(float(item.working_days))

	context = {
		'week_Num_list' : week_Num_list,
		'working_days_list': working_days_list,
	}
	return render(request, 'polls/index.html',context)


def detail(request, question_id):
	try:
		question = Question.objects.get(pk = question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("You're voting on question %s." % question_id)


@login_required
def retrieve_user_project_record(request):
	if request.method == 'POST':
		current_user = request.user
		username = current_user.username
		user_working_days_queryset = ProjectRecord.objects.filter(member_name__employee_name = username).values_list('year_Num', 'week_Num').annotate(Sum('working_days'))
		user_working_days_list = []
		year_Num_list = []
		week_Num_list = []
		for obj in user_working_days_queryset:
			year_Num_list.append(obj[0])
			week_Num_list.append(obj[1])
			user_working_days_list.append(obj[2])
		return JsonResponse({
			'user_working_days_list':user_working_days_list,
			'week_Num_list':week_Num_list,
			'year_Num_list':year_Num_list,
		})


@login_required
def retrieve_user_specific_project_record(request):
	if request.method == 'POST':
		project_name = request.POST.get('project_name')
		member_name = request.user.username
		user_project_record_queryset = ProjectRecord.objects.filter(member_name__employee_name=member_name, project_name__project_name=project_name).values_list('year_Num', 'week_Num', 'record', 'working_days').order_by('year_Num', 'week_Num')
		user_specific_project_working_days_list = []
		user_specific_project_record_list = []
		year_Num_list = []
		week_Num_list = []
		for obj in user_project_record_queryset:
			year_Num_list.append(obj[0])
			week_Num_list.append(obj[1])
			user_specific_project_record_list.append(obj[2])
			user_specific_project_working_days_list.append(obj[3])
		return JsonResponse({
			'year_Num_list':year_Num_list,
			'week_Num_list':week_Num_list,
			'user_specific_project_record_list':user_specific_project_record_list,
			'user_specific_project_working_days_list':user_specific_project_working_days_list,
		})


@login_required
def retrieve_project_name_list(request):
	if request.method == 'POST':
		querySet_project = Project.objects.all()
		project_name_list = []
		for project in querySet_project:
			project_name_list.append(project.project_name)
		return JsonResponse({
			'project_name_list':list(project_name_list),
		})

@login_required
def project_record(request):
	if request.method == 'GET':
		return render(request, 'polls/project_record.html', {})
	if request.method == 'POST':
		member_name = request.user.username
		project_name = request.POST.get('project_name')
		year_Num = int(request.POST.get('year_Num'))
		week_Num = int(request.POST.get('week_Num'))
		record = request.POST.get('record')
		working_days = request.POST.get('working_days')

		project_obj = Project.objects.get(project_name=project_name)
		member_obj = Employee.objects.get(employee_name=member_name)
		print(member_name, project_name, year_Num, week_Num, record)

		try:
			project_record_obj = ProjectRecord.objects.get(member_name = member_obj, project_name = project_obj, year_Num = year_Num, week_Num = week_Num)
			project_record_obj.record = record
			project_record_obj.working_days = working_days
			project_record_obj.save()
			return JsonResponse({'status': '已保存修改'})
		except:
			project_record_obj = ProjectRecord(member_name = member_obj, project_name = project_obj, year_Num = year_Num, week_Num = week_Num, record = record, working_days = working_days)
			project_record_obj.save()
			return JsonResponse({'status': '已保存'})

@login_required
def update_week_record_list(request):
	if request.method == 'POST':
		member_name = request.user.username
		year_Num = int(request.POST.get('year_Num'))
		week_Num = int(request.POST.get('week_Num'))

		member_obj = Employee.objects.get(employee_name=member_name)

		project_record_set = ProjectRecord.objects.filter(member_name = member_obj, year_Num = year_Num, week_Num = week_Num)
		if len(project_record_set) == 0:
			return JsonResponse({'success': 'False'})
		else:
			project_name_list = []
			record_list = []
			working_days_list = []
			for obj in project_record_set:
				project_name_list.append(obj.project_name.project_name)
				record_list.append(obj.record)
				working_days_list.append(obj.working_days)

			item_num = len(project_name_list)
			print(project_name_list)
			return JsonResponse({
				'success': 'True',
				'project_name_list': project_name_list,
				'record_list': record_list,
				'working_days_list': working_days_list,
				'item_num': item_num,
			})


def Login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect( '../project_record')
		else:
			return HttpResponse("用户不存在或密码错误，请返回！")

	if request.method == 'GET':
		return render(request, 'polls/login.html')

@login_required
def logout(request):
	auth.logout(request)
	return redirect("/polls/login/")