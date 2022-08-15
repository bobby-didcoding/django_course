from django.views import generic
from django.shortcuts import redirect, reverse, render
from django.contrib.auth import logout, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import UserForm, AuthForm, UserProfileForm, UserAlterationForm
from .models import UserProfile

class SignUpView(generic.FormView):
    """
    Basic user sign up page.

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
    Basic user sign up page.

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
    Basic user sign out page.
    """
	logout(request)
	return redirect(reverse('users:sign-in'))


@login_required
def AccountView(request):
    """
    User account page. CRUD account details.

    **Template:**

    :template:`users/account.html`
    """
    up = request.user.userprofile
    up_form = UserProfileForm(instance = up)
    context = {'form': up_form}

    if request.method == "POST":
        form = UserProfileForm(instance = up, data = request.POST)
        if form.is_valid:
            form.save()
            return redirect('/account/')
    else:
        return render(request, 'users/account.html', context)

@login_required
def UserInfoView(request):
    """
    User information page. CRUD profile details.

    **Template:**

    :template:`users/info.html`
    """
    user = request.user
    u_form = UserAlterationForm(instance = user)
    context = {'form': u_form}

    if request.method == "POST":
        form = UserProfileForm(instance = user, data = request.POST)
        if form.is_valid:
            form.save()
            return redirect('/user-info/')
    else:
        return render(request, 'users/info.html', context)