from django.urls import path
from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('project_record/', views.project_record, name = 'project_record'),

    path('login/', views.Login, name='login'),

    path('logout/', views.logout, name='logout'),

    path('update_week_record_list/', views.update_week_record_list, name='update_week_record_list'),

    path('retrieve_project_name_list/', views.retrieve_project_name_list, name='retrieve_project_name_list'),

    path('retrieve_user_project_record/', views.retrieve_user_project_record, name='retrieve_user_project_record'),

    path('retrieve_user_specific_project_record/', views.retrieve_user_specific_project_record, name='retrieve_user_specific_project_record'),

]