from django.contrib import admin

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from PublicationProject import views

app_name = 'PublicationProject'
urlpatterns = [
    path("publication_form/", views.publication_form, name='publication_form'),
    path("project_form/", views.project_form, name='project_form'),
    path("publication_view/", views.publication_view, name='publication_view'),
    path("project_view/", views.project_view, name='project_view'),
    path("edit_publication/<int:id>", views.edit_publication, name='edit_publication'),
    path("edit_project/<int:id>", views.edit_project, name='edit_project'),
    # path("publication_details/", views.publication_details, name='publication_details'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)