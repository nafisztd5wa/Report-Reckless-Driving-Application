from django.contrib import admin
from django.urls import include, path
from drivesafe import views

urlpatterns = [
    path('', views.home, name='home'),
    path('drivesafe/', include('drivesafe.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]