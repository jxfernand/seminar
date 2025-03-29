from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Import settings
from django.conf.urls.static import static  # Import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rejistu/', include('rejistu.urls')),
    path('', include('seminar.urls')),
    path('facer/', include('facer.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Add this to serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG is False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)