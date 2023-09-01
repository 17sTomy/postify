from django.urls import path
from . import views
from .views import ProfileUpdateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.feed, name='feed'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('update_profile/', ProfileUpdateView.as_view(), name='update_profile'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='social/login.html'), name='login'),
    path('logout/', login_required(LogoutView.as_view(template_name='social/logout.html')), name='logout'),
    path('post/', views.post, name='post'),
    path('post/<int:post_id>/like', views.like_post, name='like_post'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

