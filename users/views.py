from django.views import generic
from django.shortcuts import redirect, reverse
from django.contrib.auth import logout, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import UserForm, AuthForm

class SignUpView(generic.FormView):
    """
    User sign up page.

    **Template:**

    :template:`users/sign_up.html`
    """
    template_name = "users/sign_up.html"
    form_class = UserForm
    success_url = '/account/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

class SignInView(generic.FormView):
    """
    User sign in page.

    **Template:**

    :template:`users/sign_in.html`
    """
    template_name = "users/sign_in.html"
    form_class = AuthForm
    success_url = '/account/'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


def sign_out(request):
	"""
    User sign out page.
    """
	logout(request)
	return redirect(reverse('users:sign-in'))


class AccountView(generic.TemplateView):
    """
    User account page. CRUD user profile.

    **Template:**

    :template:`users/account.html`
    """
    template_name = "users/account.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserInfoView(generic.TemplateView):
    """
    User information page. CRUD profile details.

    **Template:**

    :template:`users/info.html`
    """
    template_name = "users/info.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)