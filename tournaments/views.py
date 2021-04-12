from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import TournamentCreateForm, TeamCreateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Team, Tournament


class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update({'tournaments': Tournament.objects.all()})
        return self.render_to_response(context)


class CreateTournament(TemplateView):
    template_name = 'tournaments/forms/create_tournament.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        from common.services import throw_form_errors_as_message
        form = TournamentCreateForm(data=request.POST, files=request.FILES)
        context = self.get_context_data(**kwargs)
        if form.is_valid():
            form.save()
            return redirect('')
        throw_form_errors_as_message(request, form)
        return self.render_to_response(context)


class CreateTeam(TemplateView):
    template_name = 'tournaments/forms/create_team.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        from common.services import throw_form_errors_as_message
        team = Team(owner=request.user)
        form = TeamCreateForm(data=request.POST, files=request.FILES, instance=team)
        context = self.get_context_data(**kwargs)
        if form.is_valid():
            form.save()
            return redirect('team-list')
        throw_form_errors_as_message(request, form)
        return self.render_to_response(context)


class TeamList(TemplateView):
    template_name = 'tournaments/team_list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        teams = Team.objects.filter(owner=request.user)
        context = self.get_context_data(**kwargs)
        context.update({'teams': teams})
        return self.render_to_response(context)


class TeamDetail(TemplateView):
    template_name = 'tournaments/team_detail.html'

    @method_decorator(login_required)
    def get(self, request, slug, *args, **kwargs):
        team = Team.objects.get(slug=slug)
        context = self.get_context_data(**kwargs)
        context.update({'team': team})
        return self.render_to_response(context)


class TeamDelete(TeamDetail):

    @method_decorator(login_required)
    def get(self, request, slug, *args, **kwargs):
        team = Team.objects.get(slug=slug)
        team.delete()
        return redirect('team-list')


def test_view(request):
    return render(request=request,
                  template_name='tournaments/forms/create_tournament.html')


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


def edit_team(request):
    return render(request=request,
                  template_name='tournaments/forms/edit_team.html')


# Tournaments 'utils' file
def tourn_detail_header(request):
    return render(request=request,
                  template_name='tournaments/utils/tournament_detail_header.html')


# Tournaments files
def user_tournaments_list(request):
    return render(request=request,
                  template_name='tournaments/user_tournaments_list.html')


def search_tournaments_list(request):
    return render(request=request,
                  template_name='tournaments/search_tournaments_list.html')


# New pages
def team_list(request):
    return render(request=request,
                  template_name='new_pages/../templates/tournaments/team_list.html')


def team_detail(request):
    return render(request=request,
                  template_name='new_pages/team_detail.html')


def empty_list(request):
    return render(request=request,
                  template_name='new_pages/empty_team_list.html')


def games_menu(request):
    return render(request=request,
                  template_name='new_pages/../templates/index.html')


def pugb_page(request):
    return render(request=request,
                  template_name='tournaments/forms/create_tournament.html')


def to_do_list(request):
    return render(request=request,
                  template_name='new_pages/to_do_list.html')
