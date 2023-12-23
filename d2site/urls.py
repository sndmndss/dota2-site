from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('player/', include('d2site.apps.player.urls')),
    path('', include('d2site.apps.home.urls')),
    path('match/', include('d2site.apps.matches.urls')),
    path('auth/', include('social_django.urls', namespace='social')),  # TODO: Make models to save user info
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
