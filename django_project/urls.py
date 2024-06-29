from django.contrib import admin
from django.urls import path
from hateyourmusic import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Geral
    path('', views.admin_view, name="home"),
    path('admin/', admin.site.urls),
    path('users/admin_view', views.admin_view),
    # Usuário
    path('users/create', views.user_create),
    path('users/login', views.user_login),
    path('users/logout', views.user_logout),
    path('users/delete/<id>',views.user_delete),
    path('users/update/<id>',views.user_update),
    path('users/profile/<id>',views.user_view),
    # Senha
    path('users/update_password/<id>',views.password_update),
    # Música
    path('musics/create', views.music_create),
    path('musics/delete/<id>', views.music_delete),
    path('musics/update/<id>', views.music_update),
    path('musics/view/<id>', views.music_view),
    # Playlist
    path('playlists/create/<id>', views.playlist_create),
    path('playlists/add_music/<id>', views.playlist_add_music),
    path('playlists/delete/<id>', views.playlist_delete),
    path('playlists/view/<id>', views.playlist_view)
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)