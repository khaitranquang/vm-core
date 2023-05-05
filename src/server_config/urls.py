from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('django_prometheus.urls')),
    url(r'^v1/', include('api.v1_0.urls')),

]
