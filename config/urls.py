from django.conf import settings
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', lambda r: redirect('accounts:login'), name='root'),
    path('admin/', admin.site.urls),
    path('home/', include('webcrawler.urls', namespace='home')),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('board/', include('board.urls', namespace="board")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
