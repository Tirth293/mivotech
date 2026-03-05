from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from website import views_csrf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom CSRF failure view
handler403 = 'website.views_csrf.csrf_failure'