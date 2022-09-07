# Django course - Module 6
This is my Django course. I hope you like it.

> These notes follow on from steps/module_5.md
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
        >__init__.py
        >admin.py
        >apps.py
        >models.py
        >signals.py
        >tests.py
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
git checkout module_6
git pull origin module_6
```


## Steps/Commands

>Note: Please 'cd' into the root directory and fire up your virtual environment!

In this module we will be writing the logic to enable users to sign up, sign in and sign out of our application. This will require us to write forms, views, URL's and Django templates.

1) Django forms - Unless you’re planning to build websites and applications that do nothing but publish content, and don’t accept input from your visitors, you’re going to need to understand and use forms. This module will require 2 forms.
Create a new file in /users called forms.py and use the following code.
```
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

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
```

2) Views - A view function, or view for short, is a Python function that takes a web request and returns a web response. This response can be the HTML contents of a web page, or a redirect, or a 404 error, or an XML document, or an image . . . or anything, really.
In our case, we will be writing two views to display forms. The forms will allow users to sign up and sign in.
Open /users/views.py and use the following code.
```
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
```

2) URL's - A clean, elegant URL scheme is an important detail in a high-quality web application. Django lets you design URLs however you want, with no framework limitations. Create a new file in /users called urls.py and use the following code.

```
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
	path('sign-up/', views.SignUpView.as_view(), name="sign-up"),
	path('sign-in/', views.SignInView.as_view(), name="sign-in"),
	path('sign-out/', views.sign_out, name="sign-out"),
	path('account/', views.AccountView.as_view(), name="account"),
    path('info/', views.InfoView.as_view(), name="info"),
	]
```

Our project has been modularized into applications. Therefore, we now need to register the user application URL's in /django_course/urls.py.
Use the following code to register the new user application URL's.

```
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace="core")),
    path('', include('users.urls', namespace="users")), # this is our new URL config
    path("__debug__/", include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

4) Templates - Django is configured to find HTML files in registered app's. However, to help Django you will need to structure the template directory as follows:

```
django_course\ 
    ...
    users\
        __pycache__\
        migrations\
            __pycache__\
            >__init__.py
            >0001_initial.py
        >__init__.py
        templates\
            users\
                ...
                template go here
                ...
        >admin.py
        >apps.py
        >forms.py
        >models.py
        >signals.py
        >tests.py
        >urls.py
        >views.py
    ...
```

Create a sign_in.html file in users/templates/users and use the following snippet.

```
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <h1>Sign in</h1>
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

Create a sign_up.html file in users/templates/users and use the following snippet.

```
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <h1>Sign up</h1>
    <form method="POST">
        {% csrf_token %}
        {{form.as_p}}
        <button type="submit">Submit!</button>
    </form>
    <br>
    <a href="{% url 'users:sign-in' %}">Sign in</a>
</body>
</html>
```

Create a account.html file in users/templates/users and use the following snippet.

```
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <h1>Welcome to your account {{request.user.userprofile.full_name}}</h1>
    <br>
    <a href="{% url 'users:sign-out' %}">Sign out</a>
</body>
</html>
```

Create a info.html file in users/templates/users and use the following snippet.

```
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <h1>Info - {{request.user.userprofile.full_name}}</h1>
    <br>
    <a href="{% url 'users:sign-out' %}">Sign out</a>
</body>
</html>
```

5) Settings - We now need to adjust our settings in /django_course/settings.py. Open settings and add the following code.
```
LOGIN_URL = "users:sign-in"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"
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
    users\  <--New directory
        __pycache__\
        migrations\
            __pycache__\
            >__init__.py
            >0001_initial.py
        templates\  <--New directory
            users\
                >account.html
                >info.html
                >sign_in.html
                >sign_up.html
        >__init__.py
        >admin.py
        >apps.py
        >forms.py <--New file
        >models.py
        >signals.py
        >tests.py
        >urls.py  <--New file
        >views.py
    venv\
    >.gitignore
    >db.sqlite3
    >manage.py
    >README.md
    >requirements.txt
```

***
***
