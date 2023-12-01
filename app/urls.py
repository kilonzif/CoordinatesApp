from django.urls import path

from .views import TrilaterationView

urlpatterns = [
    path('trilateration/', TrilaterationView.as_view(), name='trilateration_api'),

]