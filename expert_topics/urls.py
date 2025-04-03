from django.urls import path
from . import views

urlpatterns = [
    path('', views.research_topic_list, name='research_topic_list'),
    path('guidelines/', views.become_expert_guidelines, name='become_expert_guidelines'),
    path('create/', views.research_topic_create, name='research_topic_create'),
    path('my-topics/', views.my_research_topics, name='my_research_topics'),
    path('approval/', views.research_topic_approval_list, name='research_topic_approval_list'),
    path('approve/<int:pk>/', views.research_topic_approve, name='research_topic_approve'),
    path('<slug:slug>/', views.research_topic_detail, name='research_topic_detail'),
    path('<slug:slug>/edit/', views.research_topic_edit, name='research_topic_edit'),
    path('<slug:slug>/delete/', views.research_topic_delete, name='research_topic_delete'),
]
