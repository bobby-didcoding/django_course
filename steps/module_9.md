# Django course - Module 9
This is my Django course. I hope you like it.

> These notes follow on from steps/module_8.md
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
    >.gitignore
    >db.sqlite3
    >manage.py
    >README.md
    >requirements.txt
```
If in doubt, run the following git commands:
```
git checkout module_9
git pull origin module_9
```


## Steps/Commands

>Note: Please 'cd' into the root directory and fire up your virtual environment!

Let's continue building out our user profile. Understanding how to work with images is an essential skill in web development. 
In this module, we will be adding an ImageField to our UserProfile so our users can add an avatar.

When adding functionality I normally take this approach:
- requirements
- models
- forms
- views
- urls
- templates
- static files

Lets get started.

1) Package - We will need to install a package called Pillow that has a whole bunch of handy tools to help us manage images. Use the following command to install Pillow and add it to our requirements file.
```
pip install Pillow
pip freeze > requirements.txt
```

1) Models - lets start with our UserProfile model. We need to add a new ImageFiled to UserProfile. Open /users/models.py and change the code to the following.
```
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

#these are model abstracts from django extensions
from django_extensions.db.models import (
    TimeStampedModel,
	ActivatorModel 
)

class UserProfile(TimeStampedModel,ActivatorModel,models.Model):
    '''
    users.UserProfile
    Stores a single user profile entry related to :model:`auth.User`
    '''
    class Meta:
        verbose_name_plural = 'User profiles'
        ordering = ["id"]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(verbose_name="Contact telephone number", max_length=255, null=True, blank=True)
    address = models.CharField(verbose_name="Address",max_length=100, null=True, blank=True)
    town = models.CharField(verbose_name="Town/City",max_length=100, null=True, blank=True)
    county = models.CharField(verbose_name="County",max_length=100, null=True, blank=True)
    post_code = models.CharField(verbose_name="Zip/Post Code",max_length=8, null=True, blank=True)
    country = models.CharField(verbose_name="Country",max_length=100, null=True, blank=True)
    longitude = models.CharField(verbose_name="Longitude",max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude",max_length=50, null=True, blank=True)

    avatar = models.ImageField(default='default_avatar.jpg', upload_to='avatar', null=True, blank=True) # this is our new avatar filed
	
    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name} {self.user.last_name}'
        return self.user.email
```

Now commit the database changes with the following commands.
```
python manage.py makemigrations
python manage.py migrate
```
2) Forms - Now open /users/forms.py and change the code to the following.

```
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile

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
	avatar = forms.ImageField(required=False)
	telephone = forms.CharField(max_length=255, required=False, widget=forms.TextInput())
	address = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
	town = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
	county = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
	post_code = forms.CharField(max_length=8, required=False, widget=forms.TextInput())
	country = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
	
	class Meta:
		model = UserProfile
		fields = ( 'avatar', 'telephone', 'address', 'town', 'county', 'post_code', 'country')



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
3) Views - Now open /users/views.py and change the code to the following.

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
        form = UserProfileForm(instance = up, data = request.POST, files=request.FILES)
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
```
4) Templates - We do not have any extra url's so lets move onto templates. Open /templates/users/account.html and change the code to the following.

```
{% extends 'base/base.html' %}

{% block content %}
<h1>Welcome to your account {{request.user.userprofile.full_name}}</h1>
<form method="POST" enctype="multipart/form-data"> <!--we added the enctype as we are sending a file with the post data -->
    {% csrf_token %}
    {{form.as_p}}
    <button type="submit">Submit!</button>
</form>
{% endblock %}
```

4) Static and media - Now create a new directory in root called mediafiles and copy the 3 images across from /media. The directory configuration should look like this.

```
...
media\
    >default_avatar.jpg
    >default_item_image_2.jpg
    >default_item_image.jpg
mediafiles\
    >default_avatar.jpg
    >default_item_image_2.jpg
    >default_item_image.jpg
...
```

Now visit [http://localhost:8000/account/](http://localhost:8000/account/) to see the changes we have made.

You should now be able to update your avatar with the default 'Choose file' button. Let's make it look pretty with the help of a Javascript package.

5) 3rd party libraries - Django has got a lot of tricks up it's sleeve but there are areas that can be approved with your own bespoke code or the use of a 3rd part library. We have already installed python/django packages such as Pillow and Django Extensions. However, with some small adjustments, we can also use frontend JavaScript libraries to rub some funk on our project. We will be we using a library created by [Krajee](https://plugins.krajee.com/file-input) to improve the look and feel of our avatar field. For it to work correctly, we need to install a JavaScript library called Jquery.
Open /base/base.html and replace the code with the following.

```
<!DOCTYPE html>
{% load static %}
<html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- visit https://fonts.google.com/specimen/Courier+Prime?preview.text_type=custom to get script-->
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Courier+Prime&display=swap" rel="stylesheet">

    <!--Bootstrap-->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    
    <!--Our own css-->
    <link rel="stylesheet" href="{% static 'main.css' %}">
    
    {% block extend_head %}<!-- This allows us to extend the head scripts in HTML docs that have special requirements-->{% endblock %}
    </head>
    <body>

    <!--Side nav-->
    {% if request.user.is_authenticated %}
    <ul class="sidenav">
        <li><a {% if 'account' in request.path %}class="active"{% endif %} href="{% url 'users:account' %}">User Account ({{request.user.username}})</a></li>
        <li><a {% if 'info' in request.path %}class="active"{% endif %}  href="{% url 'users:user-info' %}">User Info</a></li>
        <li><a href="{% url 'users:sign-out' %}">Sign Out</a></li>
    </ul>
    {% else %}
    <ul class="sidenav">
        <li><a {% if 'sign-in' in request.path %}class="active"{% endif %} href="{% url 'users:sign-in' %}">Sign in</a></li>
        <li><a {% if 'sign-up' in request.path %}class="active"{% endif %} href="{% url 'users:sign-up' %}">Sign up</a></li>
    </ul>
    {% endif %}

    <div class="div-container">
        {% block content %}<!--Used to add code to head-->{% endblock %}
    </div>

    <!--visit https://code.jquery.com/ for jquery script-->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
    <!--Bootstrap-->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

    {% block extend_foot %}<!-- This allows us to extend the foot scripts in HTML docs that have special requirements-->{% endblock %}

    </body>
</html>
```

Open /templates/users/account.html and replace the code with the following.

```
{% extends 'base/base.html' %}

{% block extend_head %}
<link href="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.5/css/fileinput.min.css" media="all" rel="stylesheet" type="text/css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.min.css" crossorigin="anonymous">
<style>
    .kv-avatar .krajee-default.file-preview-frame,.kv-avatar .krajee-default.file-preview-frame:hover {
        margin: 0;
        padding: 0;
        border: none;
        box-shadow: none;
        text-align: center;
    }
    .kv-avatar {
        display: inline-block;
        max-width: 100%;
    }
    .kv-avatar .file-input {
        display: table-cell;
    }
    .file-default-preview > img:nth-child(1) {
      max-width:100% !important;
    }
    .kv-avatar .file-default-preview .img {
        max-width:100% !important; 
    }
    .kv-reqd {
        color: red;
        font-family: monospace;
        font-weight: normal;
    }
</style>
{% endblock %}

{% block extend_foot %}
<script src="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.5/js/fileinput.min.js"></script>
<script>
    var avatar_url = '{{request.user.userprofile.avatar.url|safe}}'
    var btnCust = '<button type="button" class="btn btn-secondary" title="Add picture tags" ' +
        'onclick="alert(\'Call your custom code here.\')">' +
        '<i class="bi-tag"></i>' +
        '</button>';
    $("#id_avatar").fileinput({
        overwriteInitial: true,
        maxFileSize: 1500,
        showClose: false,
        showCaption: false,
        browseLabel: '',
        removeLabel: '',
        browseIcon: '<i class="bi-folder2-open"></i>',
        removeIcon: '<i class="bi-x-lg"></i>',
        removeTitle: 'Cancel or reset changes',
        elErrorContainer: '#kv-avatar-errors-1',
        msgErrorClass: 'alert alert-block alert-danger',
        defaultPreviewContent: '<img src="'+ avatar_url +'" alt="Your Avatar">',
        layoutTemplates: {main2: '{preview} {remove} {browse}'},
        allowedFileExtensions: ["jpg", "png", "gif"]
    });
</script>
{% endblock %}

{% block content %}
<h1>Welcome to your account {{request.user.userprofile.full_name}}</h1>
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <div class="col-sm-4 text-center">
        <div class="kv-avatar">
            <div class="file-loading">
                <input id="id_avatar" name="avatar" type="file">
            </div>
        </div>
        <div class="kv-avatar-hint">
            <small>Select file < 1500 KB</small>
        </div>
    </div>
    <p><label>Telephone:</label>{{form.telephone}}</p>
    <p><label>Address:</label>{{form.address}}</p>
    <p><label>Town:</label>{{form.town}}</p>
    <p><label>County:</label>{{form.county}}</p>
    <p><label>Post Code:</label>{{form.post_code}}</p>
    <p><label>Country:</label>{{form.country}}</p>
    <button type="submit">Submit!</button>
</form>
<div id="kv-avatar-errors-1" class="text-center" style="display:none"></div>
{% endblock %}
```
You will now ba able to see the fruits of your labour at [http://localhost:8000](http://localhost:8000).
>Note: Open an incognito browser (Ctrl + Shift + N) as this will ensure your browser will grab the new changes.

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
    mediafiles\ <--New directory
    static\
        >main.css
    staticfiles\
    steps\
        >admin.md
        >basics.md
        >basics_part_2.md
        >debug.md
        >user_app_part_2.md
        >user_app.md
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