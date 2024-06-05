from django.contrib import admin
from django.urls import path
from hateyourmusic import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.admin_view, name="home"),
    path('admin/', admin.site.urls),
    path('users/admin_view', views.admin_view),
    path('users/create', views.create_user),
    path('users/login', views.login_user),
    path('users/logout', views.logout_user),
    path('users/delete/<id>',views.delete_user),
    path('users/update/<id>',views.update_user),
    path('users/update_password/<id>',views.update_password),
    path('users/profile/<id>',views.show_profile)
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)