# Django course - Module 4
This is my Django course. I hope you like it.

> These notes follow on from steps/module_3.md
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
    venv\
    >.gitignore
    >db.sqlite3
    >manage.py
    >README.md
    >requirements.txt
```
If in doubt, run the following git commands:
```
git checkout module_4
git pull origin module_4
```

## Steps/Commands
>Note: Please 'cd' into the root directory and fire up your virtual environment!

In this module, we will be exploring Django's database API. We will do this in 2 ways. Firstly, Django has a great built-in admin page straight out of the box. The Admin page allows super users to Create, Read, Update and Delete entries in our database. Secondly, we will use the Django shell. The Django shell is a Python shell that gives you access to the database API included with Django.

Let's start with the built-in admin page. You will need a superuser account to gain access.

1) Built-in admin page - Open a terminal and use the following command to create our first user.
> Note: You'll be prompted to add a username, email and password. Please make a note of these.
```
python manage.py createsuperuser
```

When created, visit [http://localhost:8000/admin](http://localhost:8000/admin) in your browser and sign in with your new credentials.


After signing in, you will be redirected to your main admin page. Get used to the layout of the admin pages as we will be using them a lot during this course.

2) Django Shell - As mentioned above, we can also check database entires using Django's shell. Lets go ahead and query our database using the Django shell.
```
python manage.py shell
```
You should see the following in your terminal log
```
Python 3.10.2 (tags/v3.10.2:a58ebcc, Jan 17 2022, 14:12:15) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> 
```
> Note: '>>>' means that the Django shell is working

Now type the following code into the Django shell
```
from django.contrib.auth.models import User
user = User.objects.first()
user.first_name
```
We have imported the built-in User model, used the model manager to get the first database and assigned it to a variable called 'user', We then checked the 'first_name' field. The response should be a '' as we have not set our first name in the database.

Let's add our first name. Add the following to the Django shell.
```
user.first_name = "Bobby"
user.save()
user.first_name
```

We have now assigned "Bobby" to the field 'first_name' and committed it to the database by calling .save(). We then checked the 'first_name' field once more. The response should be 'Bobby'.

This change will be visible in the built-in admin page. Visit [http://127.0.0.1:8000/admin/auth/user/](http://127.0.0.1:8000/admin/auth/user/) and see for yourself.
> Note: Don't forget to fire up a local server, refresh your browser and sign in if necessary.

3) CRUD - Just like the Django shell, Django's built-in admin page allows you to Create, Read, Update and Delete (CRUD) database entires. To demonstrate this, lets add your last name in the built-in admin page [http://127.0.0.1:8000/admin/auth/user/1/change/](http://127.0.0.1:8000/admin/auth/user/1/change/).

Add your last name and click save or press enter.

You can see now that your name has change. 
Let's bookend this by double checking with the Django shell with the following command.
```
python manage.py shell
```
Now use the following.
```
from django.contrib.auth.models import User
user = User.objects.first()
user.last_name
```
In my case, the response should be 'Stearman'.

4) Database API - Django's database API is great. We will explore some common features in this course. For now here are some little snippets to start you off. You can find Django's queryset documentation here [https://docs.djangoproject.com/en/4.0/ref/models/querysets/](https://docs.djangoproject.com/en/4.0/ref/models/querysets/) 
```
from django.contrib.auth.models import User
#get the first entry in the database table
user = User.objects.first()
#get the last entry in the database table
user = User.objects.last()
#gets a specific record by field(s)
user = User.objects.get(id = 1)
user = User.objects.get(first_name = 'Bobby')
user = User.objects.get(first_name = 'Bobby', last_name="Stearman")
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
    venv\
    >.gitignore
    >db.sqlite3
    >manage.py
    >README.md
    >requirements.txt
```

***
***