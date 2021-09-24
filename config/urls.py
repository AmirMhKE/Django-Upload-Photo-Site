from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.static import serve as mediaserve

handler404 = 'app.views.handler404'
handler500 = 'app.views.handler500'

urlpatterns = [
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('', include('social_django.urls', namespace="google_login")),
    path('', include('app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns.append(path(f'{settings.MEDIA_URL[1:]}<path:path>',
    mediaserve, {'document_root': settings.MEDIA_ROOT}))
