"""djangoProject_genshin_player_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('cdk', views.cdkey),
    path('cdk_create', views.create_cdkey),
    path('auth', views.auth),
    path('lucky', views.lucky),
    path('sign', views.sign),
    path('unlockmap', views.unlock_map),
    path('setworldlevel', views.set_world_level),
    path('remote_cmd', views.remote_cmd),
    path('', views.index),

]
