from django.urls import path
from django.contrib.auth import views as auth_views # auth_views import 추가
from . import views

urlpatterns = [
    path('my-urls/', views.my_urls_view, name='my_urls'),
    path('signup/', views.signup_view, name='signup'),

    path('login/', auth_views.LoginView.as_view(template_name='shortener/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]