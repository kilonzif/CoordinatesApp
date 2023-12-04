from django.urls import path
from .views import getData, postData

urlpatterns = [
    path('', getData),
    path('post/', postData),

]


