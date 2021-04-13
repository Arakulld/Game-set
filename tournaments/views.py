from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import TemplateView
from django.http import Http404
from .forms import TournamentCreateForm, TeamCreateForm, TeamEditForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Team, Tournament, JoinLink
from common.services.services import base64_encode_time_now
from django.db.models import Q
from django.contrib import messages


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
            JoinLink.objects.create(team=team,
                                    link=base64_encode_time_now(string=team.slug))
            return redirect('team-list')
        throw_form_errors_as_message(request, form)
        return self.render_to_response(context)


class TeamList(TemplateView):
    template_name = 'tournaments/team_list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            teams = Team.objects.filter(Q(owner=request.user) | Q(participants__in=[request.user]))
        except Team.DoesNotExist:
            teams = None
        context = self.get_context_data(**kwargs)
        context.update({'teams': teams})
        return self.render_to_response(context)


class TeamDetail(TemplateView):
    template_name = 'tournaments/team_detail.html'

    @method_decorator(login_required)
    def get(self, request, slug, *args, **kwargs):
        try:
            team = Team.objects.get((Q(owner=request.user) | Q(participants__in=[request.user])) & Q(slug=slug))
        except Team.DoesNotExist:
            raise Http404
        context = self.get_context_data(**kwargs)
        context.update({'team': team})
        return self.render_to_response(context)


class TeamDelete(TemplateView):

    @method_decorator(login_required)
    def get(self, request, slug, *args, **kwargs):
        team = get_object_or_404(Team, slug=slug, owner=request.user)
        team.delete()
        return redirect('team-list')


class EditTeam(TemplateView):
    template_name = 'tournaments/forms/edit_team.html'

    def get(self, request, slug, *args, **kwargs):
        get_object_or_404(Team, slug=slug, owner=request.user)
        return super(EditTeam, self).get(request, *args, **kwargs)

    def post(self, request, slug, *args, **kwargs):
        instance = get_object_or_404(Team, slug=slug, owner=request.user)
        form = TeamEditForm(data=request.POST, files=request.FILES, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('team-list')


class JoinTeam(TemplateView):
    @method_decorator(login_required)
    def get(self, request, token, *args, **kwargs):
        join_link = JoinLink.objects.get(link=token)
        if request.user not in join_link.team.participants.all() and join_link.team.owner != request.user:
            join_link.team.participants.add(request.user)
        else:
            messages.error(request, 'Already in this team')
        return redirect('team-list')


def test(request):
    return render(request, 'new_pages/to_do_list.html')


def to_do_list(request):
    return render(request=request,
                  template_name='new_pages/to_do_list_user.html')


def to_do_list_user(request):
    return render(request=request,
                  template_name='new_pages/to_do_list_user.html')
