from django.contrib import admin
from django.urls import path
from django.urls.conf import include, include
from django.contrib.auth import views as auth_views
from hateyourmusic import views

urlpatterns = [
    path('', views.home, name="home"),
    path('users', views.create_user),
    path('users/login', views.login_user, name="login"),
    path('users/logout', views.logout_user, name="logout"),
    path('login/',
         auth_views.LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('comment/<int:post_id>/',
         views.create_comment,
         name='create_comment'),
    path('comment/update/<comment_id>/',
         views.update_comment,
         name='update_comment'),
    path('comment/delete/<comment_id>/',
         views.delete_comment,
         name='delete_comment'),
    path('posts', views.create_post),
    path('posts/update/<id>', views.update_post),
    path('posts/delete/<id>', views.delete_post),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike_post/<int:post_id>/',
         views.dislike_post,
         name='dislike_post'),
    path('admin/', admin.site.urls),
]
