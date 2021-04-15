from django.urls import path
from . import views as v

urlpatterns = [
    path('login/', v.CustomLoginView.as_view(), name='login'),
    path('logout/', v.CustomLogoutView.as_view(), name='logout'),
    path('profile/', v.ProfileView.as_view(), name='profile'),
    path('profile/edit/', v.EditProfileView.as_view(), name='edit_profile'),
    path('register/confirm/', v.RegisterConfirmView.as_view(), name='register_confirm'),
    path('register/', v.RegisterView.as_view(), name='register'),
    path('register/activate/<str:token>/', v.RegisterActivateView.as_view(), name='register_activate'),
    path('password-reset/', v.CustomPasswordReset.as_view(), name='password_reset'),
    path('password-reset/done/', v.CustomPasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', v.CustomPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', v.CustomPasswordResetComplete.as_view(), name='password_reset_complete')
]
