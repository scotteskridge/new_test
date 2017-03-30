from django.conf.urls import url, include

from . import views

urlpatterns = [

    url(r'^$', views.index, name = "index"),
    url(r'^create_trip$', views.create_trip, name = "create_trip"),
    url(r'^confirm_create_trip$', views.confirm_create_trip, name = "confirm_create_trip"),
    url(r'^view_trip/(?P<trip_id>\d+)$', views.view_trip, name = "view_trip"),

    url(r'^join_trip/(?P<trip_id>\d+)$', views.join_trip, name = "join_trip"),


]
