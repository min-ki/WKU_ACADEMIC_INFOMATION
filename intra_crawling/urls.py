from django.shortcuts import redirect
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', lambda r: redirect('accounts:login'), name='root'),
    path('admin/', admin.site.urls),
    path('home/', include('webcrawler.urls')),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    # url(r'^admin/', admin.site.urls),
]
