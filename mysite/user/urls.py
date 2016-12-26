from django.conf.urls import include, url
from . import views


urlpatterns = [
    #url(r'^$', /),
    url(r'^login', views.user_login),
    url(r'^logout', views.user_logout),
]