from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_list, name='feedback_list'),
    path('create/', views.feedback_create, name='feedback_create'),
    path('edit/<slug:slug>/', views.feedback_edit, name='feedback_edit'),
    path('delete/<slug:slug>/', views.feedback_delete, name='feedback_delete'),
    path('my-feedbacks/', views.my_feedbacks, name='my_feedbacks'),
    path('approval/', views.feedback_approval_list, name='feedback_approval_list'),
    path('approve/<int:pk>/', views.feedback_approve, name='feedback_approve'),
]