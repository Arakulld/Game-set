from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from account.forms import UserForm, AccountForm, EditUserForm
from account.models import TournamentAccount, ActivateToken
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth.models import User
from common import decorators


class CustomLoginView(LoginView):
    template_name = 'account/forms/login.html'

    @method_decorator(decorators.not_auth)
    def get(self, request, *args, **kwargs):
        return super(CustomLoginView, self).get(request, *args, **kwargs)

    @method_decorator(decorators.not_auth)
    def post(self, request, *args, **kwargs):
        return super(CustomLoginView, self).post(request, *args, **kwargs)


class CustomLogoutView(LogoutView):
    template_name = 'account/logout.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(CustomLogoutView, self).get(*args, *kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return super(CustomLogoutView, self).post(*args, **kwargs)


class CustomPasswordReset(PasswordResetView):
    template_name = 'account/forms/reset_password.html'
    from_email = 'email/reset_password_pattern.html'


class CustomPasswordResetDone(PasswordResetDoneView):
    template_name = 'account/reset_password_done.html'


class CustomPasswordResetConfirm(PasswordResetConfirmView):
    template_name = ''


class CustomPasswordResetComplete(PasswordResetCompleteView):
    template_name = ''


class ProfileView(TemplateView):
    template_name = 'account/profile.html'

    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context=context)


class EditProfileView(TemplateView):
    template_name = 'account/forms/edit_profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user: User = request.user
        context = self.get_context_data(**kwargs)
        user_form = EditUserForm(data=request.POST,
                                 instance=user)
        account_form = AccountForm(data=request.POST,
                                   instance=user.account)
        if account_form.is_valid() and user_form.is_valid():
            user.username = user_form.cleaned_data['username']
            user.email = user_form.cleaned_data['email']
            if user_form.cleaned_data['password']:
                user.set_password(user_form.cleaned_data['verify_password'])
            if account_form.cleaned_data['phone_number']:
                account = user.account
                account.phone_number = account_form.cleaned_data['phone_number']
                account.save()
            user.save()
            messages.success(request=request, message='Updated successfully')
            return redirect('profile')
        else:
            from common.services import throw_form_errors_as_message

            throw_form_errors_as_message(request, user_form)
            return self.render_to_response(context)


class RegisterConfirmView(TemplateView):
    template_name = 'account/register_confirm.html'

    @method_decorator(decorators.not_auth)
    def get(self, request, *args, **kwargs):
        return super(RegisterConfirmView, self).get(request, *args, **kwargs)


class RegisterView(TemplateView):
    template_name = 'account/forms/register.html'

    @method_decorator(decorators.not_auth)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context=context)

    @method_decorator(decorators.not_auth)
    def post(self, request, *args, **kwargs):
        user_form = UserForm(data=request.POST)
        account_form = AccountForm(data=request.POST)
        if user_form.is_valid() and account_form.is_valid():
            a_cd = account_form.cleaned_data
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password_confirm'])
            new_user.is_active = False
            new_user.save()
            TournamentAccount.objects.create(user=new_user,
                                             phone_number=a_cd['phone_number'] if a_cd['phone_number'] else None)
            from django.utils.html import strip_tags
            from common.services import base64_encode_time_now

            token = base64_encode_time_now(new_user.username)
            activate_token = ActivateToken.objects.create(token=token, user=new_user)

            subject = 'Confirm account'
            html_message = render_to_string('email/activate_account_pattern.html', {'username': new_user.username,
                                                                                    'activate': activate_token,
                                                                                    'domain': request.META[
                                                                                        'HTTP_ORIGIN']})
            text_message = strip_tags(html_message)
            msg = EmailMultiAlternatives(subject, text_message, settings.EMAIL_HOST_USER, [new_user.email])
            msg.attach_alternative(html_message, 'text/html')
            try:
                msg.send()
            except WindowsError:
                new_user.delete()
                activate_token.delete()
                raise ConnectionError
        elif user_form.errors:
            from common.services import throw_form_errors_as_message
            throw_form_errors_as_message(request, user_form)
            return self.render_to_response(context=self.get_context_data(**kwargs))
        return redirect('register_confirm')


class RegisterActivateView(TemplateView):
    template_name = 'account/register_done.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        assert 'token' in kwargs
        access_token = get_object_or_404(ActivateToken, token=kwargs['token'])
        user = access_token.user
        user.is_active = True
        user.save()
        access_token.delete()
        return self.render_to_response(context)
