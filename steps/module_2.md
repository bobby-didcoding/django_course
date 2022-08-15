# Django course - Module 2
This is my Django course. I hope you like it.

> These notes follow on from steps/module_1.md
***
***

## Current root directory
Your root directory should look like the following.
```
django_course\  <--This is the root directory
    django_course\
        >__init__.py
        >asgi.py
        >settings.py
        >urls.py
        >wsgi.py
    media\
        ...
    steps\
        ...
    venv\
        include\
        Lib\
        Scripts\
    >.gitignore
    >manage.py
    >README.md
    >requirements.txt
```
If in doubt, run the following git commands:
```
git checkout module_2
git pull origin module_2
```

## Steps/Commands
>Note: Please 'cd' into the root directory and fire up your virtual environment!

"Django makes it easier to build better web apps more quickly and with less code."

In this module, we will be creating a Django application for our project. A Django application is a Python package that is specifically intended for use in a Django project. An application may use common Django conventions, such as having models, tests, urls, and views submodules. 

Our application will be called 'core'. This application will hold the logic for our core/main web pages i.e. home, about us, contact us...

1) Applications - Open a terminal and use the following command to start a new application
```
python manage.py startapp core
```

The settings.py file is where we save out project settings. Django will only know to include our core app in the project when we register it. Open django_course/settings.py and register the new application in INSTALLED_APPS. Replace the current settings with the following snippet.
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core' #this is our new application
]
```

2) Views - A view function, or view for short, is a Python function that takes a web request and returns a web response. This response can be the HTML contents of a web page, or a redirect, or a 404 error, or an XML document, or an image . . . or anything, really. Lets create our first view. Open django_course/core/views.py and write a view to handle the user request/response logic. Use the following snippet.
>Note: We will be using one of Django's built in views called 'TemplateView'.
```
from django.views import generic

class HomeView(generic.TemplateView):
	"""
    Website home page.

    **Template:**

    :template:`core/index.html`
    """
	template_name = "core/index.html"
```

3) Templates - We will need a HTML template to render on a browser. Being a web framework, Django needs a convenient way to generate HTML dynamically. The most common approach relies on templates. A template contains the static parts of the desired HTML output as well as some special syntax describing how dynamic content will be inserted. Django is configured to find HTML files in registered app's. However, to help Django you will need to structure the template directory as follows:
```
django_course\ 
    core\
        migrations\
            >__init__.py
        templates\
            core\
                ...
                template go here
                ...
        >__init__.py
        >admin.py
        >apps.py
        >models.py
        >tests.py
        >views.py
```

Create HTMl template - create an index.html file in core/templates/core:

```
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <h1>Welcome to our Django course</h1>
</body>
</html>
```

4) URL's - A clean, elegant URL scheme is an important detail in a high-quality web application. Django lets you design URLs however you want, with no framework limitations. To design URLs for an app, you create a Python module informally called a URLconf (URL configuration). This module is pure Python code and is a mapping between URL path expressions to Python functions (your views). Go ahead and create a new urls.py file in /core to handle url's for the core application. Use the following snipped of code in the new file.

```
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
	path("", views.HomeView.as_view(), name="home"),
]
```

Now go ahead and open django_course/urls.py (URLconf)and wire up the core application urls. Replace the code with the following snippet.

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace="core")), #our bespoke apps
]
```

8) Local server - Django has a built in development server which is a lightweight web server written purely in Python. Django's development server allows us to develop things rapidly, without having to deal with configuring a production server – such as Apache – until you’re ready for production. Use the following command to start a local development server
```
python manage.py runserver
```
You should see this log.
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
August 04, 2022 - 12:18:44
Django version 4.0.6, using settings 'django_course.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
>Note: Don't worry about the unapplied migration error message in your terminal. We'll deal with that soon enough.

You should now be up and running!
>Note: Open an incognito browser when testing your project (Ctrl + Shift + N)

* Our django course project is accessible at [http://localhost:8000](http://localhost:8000)

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
        ...
    steps\
        ...
    venv\
        ...
    >.gitignore
    >db.sqlite3
    >manage.py
    >README.md
    >requirements.txt
```

***
***