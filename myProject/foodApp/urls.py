from django.conf.urls import url
from . import views

app_name = 'foodApp'

urlpatterns = {
    url(r'^$', views.index, name='index'),
    url(r'^ajax/communicate/$', views.communicate, name='communicate'),
}