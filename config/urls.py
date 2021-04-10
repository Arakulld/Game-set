"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from tournaments import views as tv

urlpatterns = [
    path('test/', tv.test_view, name='test'),
    path('', include('tournaments.urls')),

    # Templates \ base
    path('base/', tv.base, name='base'),

    # Templates\ account files
    path('logout', tv.logout, name='logout'),
    path('profile', tv.profile, name='profile'),
    path('register_confirm/', tv.register_confirm, name='register_confirm'),
    path('register_done/', tv.register_done , name='register_done'),

    path('register_confirm/', tv.register_confirm, name='register_confirm'),
    path('reset_password_done/', tv.reset_password_done, name='reset_password_done'),

    # Templates\ email files
    path('activate_account_pattern/', tv.activate_account_pattern , name='activate_account_pattern'),
    path('reset_password_pattern/', tv.reset_password_pattern, name='reset_password_pattern'),

    # Templates\ account\ forms' files
    path('edit_profile/', tv.edit_profile, name='edit_profile'),
    path('login/', tv.login, name='login'),
    path('register/', tv.register, name='register'),
    path('reset_password/', tv.reset_password, name='reset_password'),

    # Tournaments forms files
    path('create_team/', tv.create_team, name='create_team'),
    path('edit_team/', tv.edit_team, name='edit_team'),

    # Tournaments utils file
    path('tournament_detail_header/', tv.tourn_detail_header, name='tournament_detail_header'),

    
    # Tournaments files
    path('user_tournaments_list/', tv.user_tournaments_list, name='user_tournaments_list'),
    path('search_tournaments_list/', tv.search_tournaments_list, name='search_tournaments_list'),
    path('', include('tournaments.urls')),
    path('', include('account.common_urls')),
    path('account/', include('account.account_urls')),
    path('admin/', admin.site.urls),

    # New pages
    path('team_list/', tv.team_list),
    path('dandelions/', tv.team_detail, name='dandelions'),
    path('empty_list/', tv.empty_list, name='empty_list'),
    path('games_menu/', tv.games_menu, name='games_menu'),
    path('pugb_page/', tv.pugb_page, name='pugb_page'),
    path('to_do_list/', tv.to_do_list, name='to_do_list'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
