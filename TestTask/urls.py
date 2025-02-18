from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import words

admin.site.site_header = 'LestaTask Admin'
admin.site.index_title = 'Superuser Administration'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('words.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
