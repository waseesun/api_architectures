"""
URL configuration for django_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from real_time_api import ws_consumer

urlpatterns = [
    path("admin/", admin.site.urls),
    path("django-rest-api/", include("rest_api.urls")),
    path("django-webhooks/", include("webhooks.urls")),
    path("django-real-time-api/", include("real_time_api.urls")),
    path("django-graphql-api/", include("graphql_api.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

websocket_urlpatterns = [
    re_path(r'ws/messages/(?P<client_id>[0-9a-f-]+)/$', ws_consumer.WebSocketMessageConsumer.as_asgi()),
]