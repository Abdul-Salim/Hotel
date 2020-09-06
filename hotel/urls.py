"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from hotelapp import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('admin/', admin.site.urls),
    path('customer_signup/', views.customer_signup),
    path('staff_signup/', views.staff_signup),
    path('login_staff/', views.login_staff),
    path('login_customer/', views.login_customer),
    path('my_ads/', views.myads),
    path('about/', views.about),
    path('add_hotel/', views.add_hotel),
    path('add_room/', views.add_room),
    path('hotels/', views.hotel_list),
    path('delete_ad/<int:id>/',views.delete_ad),
    path('edit_ad/<int:id>/',views.edit_ad),
    path('book_room/<int:id>/',views.book_room),
    path('logout/' , auth_views.LogoutView.as_view() , name='logout') ,
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)