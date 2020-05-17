from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^hldesk/', include('hldesk.urls', namespace='hldesk')),
    url(r'^admin/', admin.site.urls),
]
