from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('create/', views.blog_create, name='blog_create'),
    path('my-posts/', views.my_blog_posts, name='my_blog_posts'),
    path('approval/', views.blog_approval_list, name='blog_approval_list'),
    path('approve/<int:pk>/', views.blog_approve, name='blog_approve'),
    path('like/<int:pk>/', views.like_blog_post, name='like_blog_post'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('<slug:slug>/edit/', views.blog_edit, name='blog_edit'),
    path('<slug:slug>/delete/', views.blog_delete, name='blog_delete'),
]
