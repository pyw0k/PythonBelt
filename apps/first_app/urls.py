from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^display_appointments$', views.display_appointments),
    url(r'^add_appointment$', views.add_appointment),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^logout$', views.logout),
    url(r'^update_appointment/(?P<id>\d+)$', views.update_appointment)
]