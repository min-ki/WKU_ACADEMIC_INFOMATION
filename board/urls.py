from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.post_list, name="list"),
    path('<int:pk>/', views.post_detail, name="detail"),
    path('new/', views.post_new, name="new"),
]
