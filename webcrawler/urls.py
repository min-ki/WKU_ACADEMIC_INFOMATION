from django.urls import path
from . import views

app_name = 'webcrawler'

urlpatterns = [
    path('', views.index, name='index'),
    path('point/', views.point, name='point'),
    path('completed/', views.completed_list, name='completed'),
    path('necessary/', views.necessary_list, name='necessary'),
    path('major/', views.major_list, name='major'),
    path('culture/', views.culture_list, name='culture'),
    path('chart/', views.chart, name='chart'),
]
