from django.contrib import admin
from django.urls import path
from hateyourmusic import views

urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),
    path('users/create', views.create_user),
    path('users/login', views.login_user),
    path('users/logout', views.logout_user),
    path('users/delete/<id>',views.delete_user),
    path('users/update/<id>',views.update_user),
    path('users/update_password/<id>',views.update_password)
]