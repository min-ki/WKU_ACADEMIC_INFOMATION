from django.conf import settings
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', lambda r: redirect('accounts:login'), name='root'),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('home/', include('webcrawler.urls', namespace='home')),
    path('home/board/', include('board.urls', namespace="board")),
    path('admin/', admin.site.urls),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
