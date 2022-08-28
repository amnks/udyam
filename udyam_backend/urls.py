from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import LeaderBoard, Dashboard, Team_delete, Update_User, teamView

urlpatterns = [
	path('leaderboard', LeaderBoard, name='leaderboard'),
    path('dashboard', Dashboard, name='dashboard'),
    path('team', teamView, name="team"),
    path('team-delete/<int:id>', Team_delete, name='team-delete'),
    path('update-user', Update_User, name='update-user')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)