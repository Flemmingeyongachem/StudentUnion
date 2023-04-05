from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.auth.models import Group
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('due_receipt/',include("StudentUnion.urls",namespace="StudentUnion")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls',namespace="accounts")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "HTTTC KUMBA STUDENT UNION"
admin.site.unregister(Group)