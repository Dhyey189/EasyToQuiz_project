from django.contrib import admin
from django.urls import path,include
# from . import views
from django.conf.urls import url
from .views import index
urlpatterns=[

    url(r'^index/$', index),
    # path('UserRegistration',views.register,name='register')
]
