from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api.v1_0 import views

router = DefaultRouter(trailing_slash=False)


urlpatterns = [
    url(r'^', include(router.urls))
]

