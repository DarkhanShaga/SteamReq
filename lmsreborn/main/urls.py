from django.contrib import admin
from django.urls import path, include
from django.views.generic import *
from .views import *
urlpatterns = [
    # path('', login_request, name="login"),
    # path('', , name="home"),
    path('registration/', register_view, name="reg"),
    path('login/', TemplateView.as_view(template_name='login.html'), name="log"),
    path('qwerty/', auth_view, name='log1'),
    path('home/', HomePageView, name='home'),
    path('account/', AccountPageView, name='account'),
    path('logout/', logout_view, name='logout'),
    path('error/', TemplateView.as_view(template_name='error.html'), name='err'),
    path('delete/', delete_view, name='del'),
    path('update_username/', update_username_view, name='updu'),
    path('update_email/', update_email_view, name='upde'),
    path('update_password/', update_password_view, name='updp'),
    path('update_gpu/', update_gpu_view, name='updg'),
    path('update_cpu/', update_cpu_view, name='updc'),
    path('update_ram/', update_ram_view, name='updr'),
    path('comparing/', comparing, name='comp'),
    path('info/', info_view, name='inf'),
]
