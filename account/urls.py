from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.homepage, name='home'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('user-profile/', views.user_profile, name='user-profile'),
]
