from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import TemplateView
from .forms import TournamentCreateForm, TeamCreateForm, TeamEditForm
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
            return redirect('index')
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
        try:
            teams = Team.objects.filter(owner=request.user)
        except Team.DoesNotExist:
            teams = None
        context = self.get_context_data(**kwargs)
        context.update({'teams': teams})
        return self.render_to_response(context)


class TeamDetail(TemplateView):
    template_name = 'tournaments/team_detail.html'

    @method_decorator(login_required)
    def get(self, request, slug, *args, **kwargs):
        team = get_object_or_404(Team, slug=slug, owner=request.user)
        context = self.get_context_data(**kwargs)
        context.update({'team': team})
        return self.render_to_response(context)


class TeamDelete(TemplateView):

    @method_decorator(login_required)
    def get(self, request, slug, *args, **kwargs):
        team = get_object_or_404(Team, slug=slug)
        team.delete()
        return redirect('team-list')


class EditTeam(TemplateView):
    template_name = 'tournaments/forms/edit_team.html'

    def post(self, request, slug, *args, **kwargs):
        instance = get_object_or_404(Team, slug=slug, owner=request.user)
        form = TeamEditForm(data=request.POST, files=request.FILES, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('team-list')


def test(request):
    return render(request, 'tournaments/forms/edit_team.html')


def to_do_list(request):
    return render(request=request,
                  template_name='new_pages/to_do_list.html')


def to_do_list_user(request):
    return render(request=request,
                  template_name='new_pages/to_do_list_user.html')
