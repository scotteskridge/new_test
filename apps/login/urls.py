from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    #need to register
    url(r'^login$', views.login, name = "login"),
    url(r'^register$', views.register, name = "register"),


        #need to success
    url(r'^success$', views.success, name = "success"),
        #need to logout
    url(r'^logout$', views.logout, name = "logout")
]
