from django.urls import path
from . import views

urlpatterns = [
    path('', views.research_paper_list, name='research_paper_list'),
    path('create/', views.research_paper_create, name='research_paper_create'),
    path('my-papers/', views.my_research_papers, name='my_research_papers'),
    path('approval/', views.research_paper_approval_list, name='research_paper_approval_list'),
    path('approve/<int:pk>/', views.research_paper_approve, name='research_paper_approve'),
    path('<slug:slug>/', views.research_paper_detail, name='research_paper_detail'),
    path('<slug:slug>/edit/', views.research_paper_edit, name='research_paper_edit'),
    path('<slug:slug>/delete/', views.research_paper_delete, name='research_paper_delete'),
]
