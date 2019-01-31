from django.contrib import admin

from .models import Question, Choice, Employee, Project, Blog, Author, Entry, ProjectRecord

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Entry)
admin.site.register(ProjectRecord)


