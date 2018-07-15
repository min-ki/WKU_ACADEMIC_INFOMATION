from django.urls import path
from . import views

app_name = 'webcrawler'

urlpatterns = [
    path('', views.index, name='index'),
    path('completed/', views.completed_list, name='completed'),
    path('major/', views.major_list, name='major'),
    path('culture/', views.culture_list, name='culture'),
    path('wpoint/', views.wpoint_detail, name='wpoint'),
    path('chart/', views.chart, name='chart'),
]