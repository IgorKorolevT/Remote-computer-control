from django.urls import path, include
from computer.api import urls as api_urls
from computer.web import urls as web_urls

app_name = "computer"

urlpatterns = [
    path("api/", include(api_urls)),
    path("", include(web_urls)),
]
