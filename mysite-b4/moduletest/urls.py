from django.urls import path
from . import views


urlpatterns = [

    path('GasTurbineFilter/', views.GasTurbineFilter, name='GasTurbineFilter'),
    path('InternalEngineFilter/', views.InternalEngineFilter, name='InternalEngineFilter'),
	path('ConfigurationCombination/', views.ConfigurationCombination, name='ConfigurationCombination'),
	path('OperatingStrategy/', views.OperatingStrategy, name='OperatingStrategy'),
	path('LoadDataUpload/', views.LoadDataUpload, name='LoadDataUpload'),
	path('SolutionComparison/', views.SolutionComparison, name='SolutionComparison'),
	path('Wizard/', views.Wizard, name='Wizard'),
 	path('InvestmentAssessment/', views.InvestmentAssessment, name='InvestmentAssessment'),
  	path('Economic/', views.Economic, name='Economic'),
	path('SteamSolution/', views.SteamSolution, name='SteamSolution'),
	path('registration/', views.registration, name='registration'),
	path('login/', views.Login, name='login'),
	path('index/', views.index, name='index'),
	path('logout/', views.logout, name='logout'),
	path('economicAjax/', views.economicAjax, name='economicAjax'),
	path('loadProjectInfo/', views.loadProjectInfo, name='loadProjectInfo'),
	path('saveProjectInfo/', views.saveProjectInfo, name='saveProjectInfo'),

]

