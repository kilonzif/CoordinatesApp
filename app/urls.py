from django.urls import path

from .views import trilateration_view,index

urlpatterns = [
    path('index',index),
    path('',trilateration_view),
]