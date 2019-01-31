from django.db import models
from django.db import models
import datetime


class Employee(models.Model):
	employee_name = models.CharField(max_length = 20)
	def __str__(self):
		return self.employee_name

class Project(models.Model):
	project_name = models.CharField(max_length = 100)
	project_member = models.ManyToManyField(Employee)
	manager = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='manager', null=True)

	def __str__(self):
		return self.project_name

class ProjectRecord(models.Model):
	project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
	member_name = models.ForeignKey(Employee, on_delete=models.CASCADE)
	year_Num = models.IntegerField()
	week_Num = models.IntegerField()
	record = models.CharField(max_length=1000)
	working_days = models.FloatField()


class Question(models.Model):
	question_text = models.CharField(max_length = 200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days = 1)

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	choice_text = models.CharField(max_length = 200)
	votes = models.IntegerField(default = 0)

	def __str__(self):
		return self.choice_text

class Blog(models.Model):
	name = models.CharField(max_length=100)
	tagline = models.TextField()

	def __str__(self):
		return self.name

class Author(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField()

	def __str__(self):
		return self.name

class Entry(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	headline = models.CharField(max_length=255)
	body_text = models.TextField()
	pub_date = models.DateField()
	mod_date = models.DateField()
	authors = models.ManyToManyField(Author)
	n_comments = models.IntegerField()
	n_pingbacks = models.IntegerField()
	rating = models.IntegerField()

	def __str__(self):
		return self.headline