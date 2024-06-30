from django.contrib import admin
from django.urls import path
from hateyourmusic import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Geral
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("admin_view", views.admin_view),
    # Usuário
    path("users/create", views.user_create, name="user_create"),
    path("users/login", views.user_login, name="user_login"),
    path("users/logout", views.user_logout, name="user_logout"),
    path("users/delete/<id>",views.user_delete, name="user_delete"),
    path("users/update/<id>",views.user_update, name="user_update"),
    path("users/profile/<id>",views.user_view, name="user_view"),
    path("users/musics/<id>", views.user_musics, name="user_musics"),
    path("users/playlists/<id>", views.user_playlists, name="user_playlists"),
    path("users/menu/<id>", views.user_menu, name="user_menu"),
    # Senha
    path("users/update_password/<id>", views.password_update, name="password_update"),
    # Música
    path("musics/create/<id>", views.music_create, name="music_create"),
    path("musics/delete/<id>", views.music_delete, name="music_delete"),
    path("musics/update/<id>", views.music_update, name="music_update"),
    path("musics/view/<id>", views.music_view, name="music_view"),
    path("musics/menu/<id>", views.music_menu, name="music_menu"),
    # Playlist
    path("playlists/create/<id>", views.playlist_create, name="playlist_create"),
    path("playlists/add_music/<id>", views.playlist_add_music, name="playlist_add_music"),
    path("playlists/delete/<id>", views.playlist_delete, name="playlist_delete"),
    path("playlists/view/<id>", views.playlist_view, name="playlist_view"),
    path("playlists/menu/<id>", views.playlist_menu, name="playlist_menu")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)