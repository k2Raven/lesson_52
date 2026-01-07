from django.urls import path
from django.contrib.auth.views import LoginView
from accounts.views import RegisterView, UserDetailView, UserChangeView, UserPasswordChangeView, CustomLogoutView, CustomLoginView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', UserChangeView.as_view(), name='profile_edit'),
    path('profile/password/', UserPasswordChangeView.as_view(), name='password_change'),
]