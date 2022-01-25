import self as self
from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, UserProfilerForm
from authapp.models import ShopUser
from basketapp.models import Basket
from geekshop import settings
from django.conf import settings
from mainapp.mixin import BaseClassContextMixin, UserDispatchMixin


class LoginListView(LoginView, BaseClassContextMixin):
    template_name = 'authapp/login.html'
    login_form = ShopUserLoginForm
    title = 'вход'


class Logout(LogoutView, BaseClassContextMixin):
    template_name = "geekshop/index.html"


class RegisterListView(FormView, BaseClassContextMixin):
    model = ShopUser
    title = 'регистрация'
    form_class = ShopUserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('auth:login'))
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def send_verify_link(user):
        verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
        subject = f"для авторизации {user.username} пройдите по ссылке"
        message = f"для авторизации {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}"
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activate_key):
        try:
            user = ShopUser.objects.get(email=email)
            if user and user.activation_key == activate_key and not user.is_activation_key_expired():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self, user)
            return render(self, 'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))


class EditListView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    template_name = 'authapp/edit.html'
    title = 'Профиль'
    form_class = UserProfilerForm

    success_url = reverse_lazy('auth:edit')

    def form_valid(self, form):
        messages.set_level(self.request, messages.SUCCESS)
        messages.success(self.request, "профиль")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, *args, **kwargs):
        return get_object_or_404(ShopUser, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(EditListView, self).get_context_data(**kwargs)
        context['basket'] = EditListView(instance=self.request.user)
        return context


class GoogleAuth(LoginView, BaseClassContextMixin):
    template_name = "authapp/google_auth.html"
