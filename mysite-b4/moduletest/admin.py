from django.contrib import admin
from .models import Load, ProjectInfo, LHSX_ProjectInfo

admin.site.register([Load, ProjectInfo, LHSX_ProjectInfo])
