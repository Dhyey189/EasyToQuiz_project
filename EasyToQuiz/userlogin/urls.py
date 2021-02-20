from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls import url
from .views import login, userregistration
urlpatterns=[

    url(r'^login/$', login),
    path('login', views.login, name= 'login'),
    url(r'^userregistration/$', userregistration),
    path('userregistration', views.userregistration, name= 'userregistration'),
    
    # path('UserRegistration',views.register,name='register')
]
