from django.urls import path
from . import views

app_name = 'webcrawler'

urlpatterns = [
    path('', views.index, name='index')
    # url(r'^/$', views.index, name='index')
]
