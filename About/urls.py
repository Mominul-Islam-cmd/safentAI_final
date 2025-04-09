from django.contrib import admin

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from About import views


app_name = 'About'
urlpatterns = [
   
    path("about_us/", views.about_us, name='about_us'),
 
    path("team_info_form/", views.team_info_form, name='team_info_form'),
    path("edit_team_info/<int:member_id>", views.edit_team_info, name='edit_team_info'),
    path("delete_info/<int:member_id>", views.delete_info, name='delete_info'),
    # path("team_member_view/", views.team_member_view, name='team_member_view'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)