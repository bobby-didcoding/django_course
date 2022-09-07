# Django course - Module 7
This is my Django course. I hope you like it.

> These notes follow on from steps/module_6.md
***
***

## Current root directory
Your root directory should look like the following.
```
django_course\  <--This is the root directory
    core\
        __pycache__\
        migrations\
            >__init__.py
        templates\
            core\
                >index.html
        >__init__.py
        >admin.py
        >apps.py
        >models.py
        >tests.py
        >urls.py
        >views.py
    django_course\
        __pycache__\
        >__init__.py
        >asgi.py
        >settings.py
        >urls.py
        >wsgi.py
    media\
    static\ 
    staticfiles\
    steps\
    users\
        __pycache__\
        migrations\
            __pycache__\
            >__init__.py
            >0001_initial.py
        templates\
            users\
                >account.html
                >info.html
                >sign_in.html
                >sign_up.html
        >__init__.py
        >admin.py
        >apps.py
        >forms.py
        >models.py
        >signals.py
        >tests.py
        >urls.py
        >views.py
    venv\
    >.gitignore
    >db.sqlite3
    >manage.py
    >README.md
    >requirements.txt
```
If in doubt, run the following git commands:
```
git checkout module_7
git pull origin module_7
```


## Steps/Commands

>Note: Please 'cd' into the root directory and fire up your virtual environment!

In this module, we will be taking what we have learnt so far and using it to build our user account and profile pages. I would like a user to be able to read and update there UserProfile. We will begin with building a model form.

Lets get started.

1) Model Form - If you remember back when we created our first model, we added a whole bunch of fields that we haven't used until now. Go ahead and use the following code in the /users/forms.py file.

```
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, COUNTRIES

class UserForm(UserCreationForm):
	'''
	Form that uses built-in UserCreationForm to handel user creation
	'''
	username = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
	password1 = forms.CharField(required=True, widget=forms.PasswordInput())
	password2 = forms.CharField(required=True, widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')



class AuthForm(AuthenticationForm):
	'''
	Form that uses built-in AuthenticationForm to handel user auth
	'''
	username = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
	password = forms.CharField(required=True, widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username','password')



class UserProfileForm(forms.ModelForm):
	'''
	Basic model-form for our user profile
	'''
	telephone = forms.CharField(max_length=255, required=False, widget=forms.TextInput())
	address = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
	town = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
	county = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
	post_code = forms.CharField(max_length=8, required=False, widget=forms.TextInput())
	country = forms.CharField(max_length=100, required=False, widget=forms.Select(choices=COUNTRIES))
	
	class Meta:
		model = UserProfile
		fields = ('telephone', 'address', 'town', 'county', 'post_code', 'country')


class UserAlterationForm(forms.ModelForm):
	'''
	Basic model-form for our user
	'''
	first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
	last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
	email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput())
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')
```

2) View - The current account view is a 'generic.TemplateView'. This will need changing if we want to instantiate and display a form. Open users/views.py and use the following code.

```
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
        form = UserAlterationForm(instance = user, data = request.POST)
        if form.is_valid:
            form.save()
            return redirect('/user-info/')
    else:
        return render(request, 'users/info.html', context)
```

3) URL change - We have changed our account view from a class based view to a function based view. Therefore, we must now change our users app url file. Open /users/urls.py and change the code to the following.

```
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
	path('sign-up/', views.SignUpView.as_view(), name="sign-up"),
	path('sign-in/', views.SignInView.as_view(), name="sign-in"),
	path('sign-out/', views.sign_out, name="sign-out"),
	path('account/', views.AccountView, name="account"), #We have removed '.as_view()',
    path('user-info/', views.UserInfoView, name="user-info"), #We have removed '.as_view()'
	]
```
Now visit [http://localhost:8000](http://localhost:8000) and test out the new account page.

4) Templates - We can now change our account template with a form. Open /users/templates/users/account.html and replace the code with the following.
```
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <h1>Welcome to your account {{request.user.userprofile.full_name}}</h1>
    <form method="POST">
        {% csrf_token %}
        {{form.as_p}}
        <button type="submit">Submit!</button>
    </form>
    <br>
    <a href="{% url 'users:sign-up' %}">Sign up</a>
</body>
</html>
```
Now open /users/templates/users/info.html and replace the code with the following.
```
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <h1>Info - {{request.user.userprofile.full_name}}</h1>
    <form method="POST">
        {% csrf_token %}
        {{form.as_p}}
        <button type="submit">Submit!</button>
    </form>
    <br>
    <a href="{% url 'users:sign-up' %}">Sign up</a>
</body>
</html>
```
***
***

## Root directory
>Note: If all went well, your root directory should now look like this
```
django_course\  <--This is the root directory
    core\
        __pycache__\
        migrations\
            __pycache__\
            >__init__.py
        >__init__.py
        >admin.py
        >apps.py
        >models.py
        >tests.py
        >urls.py
        >views.py
    django_course\
        __pycache__\
        >__init__.py
        >asgi.py
        >settings.py
        >urls.py
        >wsgi.py
    media\ 
    static\
        >main.css
    staticfiles\
    steps\
    templates\
        base\
            >base.html
        core\
            >index.html
        users\
            >account.html
            >info.html
            >sign_in.html
            >sign_up.html
    users\
        __pycache__\
        migrations\
            __pycache__\
            >__init__.py
            >0001_initial.py
        >__init__.py
        >admin.py
        >apps.py
        >forms.py
        >models.py
        >signals.py
        >tests.py
        >urls.py
        >views.py
    venv\
        include\
        Lib\
        Scripts\
    >.gitignore
    >db.sqlite3
    >manage.py
    >README.md
    >requirements.txt
```

***
***
