from django.urls import path

from .views import (
    get_posts,
    get_post,
    create_posts,
    update_post,
    delete_post,
    register,
    login
)

urlpatterns = [
    path('posts/', get_posts),
    path('posts/<int:pk>/', get_post),
    path('posts/create/', create_posts),
    path('posts/update/<int:pk>/', update_post),
    path('posts/delete/<int:pk>/', delete_post),
    path('register/',register),
    path('login/', login),
]