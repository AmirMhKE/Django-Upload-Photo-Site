from django.conf.urls.static import static
from django.urls import include, path

from . import settings

urlpatterns = [
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('', include('social_django.urls', namespace="google_login")),
    path('', include('app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
