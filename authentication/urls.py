from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import HomeView, LoginView, LogoutView, ActivateAccountView

urlpatterns = [
    path('', HomeView, name='home'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('activate/<uidb64>/<token>/',ActivateAccountView, name='activate'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='forget_password_email.html'), name = 'password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name= 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)