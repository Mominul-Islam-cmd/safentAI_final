
from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.conf.urls.static import static


app_name = 'Guidelines'

urlpatterns = [
    
    path('guidelines_cards/', views.guidelines_cards, name='guidelines_cards'),
    path('ai/', views.ai, name='ai'),
    path('data_analytics/', views.data_analytics, name='data_analytics'),
    path('data_engineer/', views.data_engineer, name='data_engineer'),
    path('research/', views.research, name='research'),
  
]

urlpatterns+= staticfiles_urlpatterns()
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)