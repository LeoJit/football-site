"""fixtures_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('leagues', views.leagues, name="leagues"),
    path('fixtures', views.fixtures, name="fixtures"),
    path('laliga', views.LaLiga, name='LaLiga'),
    path('epl', views.EPL, name='English Premier League'),
    path('buli', views.Bundesliga, name='Bundesliga'),
    path('l1', views.Ligue_1, name='Ligue 1'),
    path('seriea', views.Serie_A, name='Serie A'),
    path('search', views.get_name, name='Search')
]
