from django.urls import path
from .views import *


urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:user_id>', UserProfile.as_view(), name='profile'),
    path('<int:user_id>/update', ProfileChange.as_view(), name='profile_update')
]
