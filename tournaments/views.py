from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from tournaments.models import Tournament


def test_view(request):
    return render(request=request,
                  template_name='account/profile.html')


# Templates \ base
def base(request):
    return render(request=request,
                  template_name='base.html')


# Templates\ account\ forms files
def edit_profile(request):
    return render(request=request,
                  template_name='account/forms/edit_profile.html')


def login(request):
    return render(request=request,
                  template_name='account/forms/login.html')


def register(request):
    return render(request=request,
                  template_name='account/forms/register.html')


def reset_password(request):
    return render(request=request,
                  template_name='account/forms/reset_password.html')


# Templates\ email files
def reset_password_pattern(request):
    return render(request=request,
                  template_name='email/reset_password_pattern.html')

def activate_account_pattern(request):
    return render(request=request,
                  template_name='email/activate_account_pattern.html')


# Templates\ account files
def logout(request):
    return render(request=request,
                  template_name='account/logout.html')

def profile(request):
    return render(request=request,
                  template_name='account/profile.html')

def register_done(request):
    return render(request=request,
                  template_name='account/register_done.html')


def register_confirm(request):
    return render(request=request,
                  template_name='account/register_confirm.html')


def reset_password_done(request):
    return render(request=request,
                  template_name='account/reset_password_done.html')


# Tournaments 'forms' files 
def create_team(request):
    return render(request=request,
                  template_name='tournaments/forms/create_team.html')


def tournament_info(request):
    return render(request=request,
                  template_name='tournaments/forms/create_tournament_info.html')


def edit_team(request):
    return render(request=request,
                  template_name='tournaments/forms/edit_team.html')


# Tournaments 'utils' file
def tourn_detail_header(request):
    return render(request=request,
                  template_name='tournaments/utils/tournament_detail_header.html')

def messages(request):
    return render(request=request,
                  template_name='tournaments/utils/messages.html')


# Tournaments files
def user_tournaments_list(request):
    return render(request=request,
                  template_name='tournaments/user_tournaments_list.html')


def search_tournaments_list(request):
    return render(request=request,
                  template_name='tournaments/search_tournaments_list.html')


def tourn_detail_overview(request):
    return render(request=request,
                  template_name='tournaments/tournament_detail_overview.html')


# New pages
def create_tournaments(request):
    return render(request=request,
                  template_name='new_pages/create_tournaments.html')

def dandelions(request):
    return render(request=request,
                  template_name='new_pages/dandelions.html')

def empty_list(request):
    return render(request=request,
                  template_name='new_pages/empty_team_list.html')

def games_menu(request):
    return render(request=request,
                  template_name='new_pages/games_menu.html')

def pugb_page(request):
    return render(request=request,
                  template_name='new_pages/pugb_page.html')

def to_do_list(request):
    return render(request=request,
                  template_name='new_pages/to_do_list.html')




@login_required
def tournament_detail(request, slug):
    tournament = get_object_or_404(Tournament, slug=slug)
    return render(request=request,
                  template_name='tournaments/tournament_detail_overview.html',
                  context={'tournament': tournament,
                           'user': request.user}, )
