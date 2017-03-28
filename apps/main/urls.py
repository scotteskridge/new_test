from django.conf.urls import url, include

from . import views

urlpatterns = [

    url(r'^$', views.index, name = "index"),
    url(r'^add_appointment$', views.add_appointment, name = "add_appointment"),
    url(r'^edit_appointment/(?P<appointment_id>\d+)$', views.edit_appointment, name = "edit_appointment"),
    url(r'^confirm_edit_appointment/(?P<appointment_id>\d+)$', views.confirm_edit_appointment, name = "confirm_edit_appointment"),
    url(r'^delete_appointment/(?P<appointment_id>\d+)$', views.delete_appointment, name = "delete_appointment"),



]
