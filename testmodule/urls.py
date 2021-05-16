from django.urls import path
from .views import *


urlpatterns = [
    path('', TestView.as_view(), name='test')
    ]
