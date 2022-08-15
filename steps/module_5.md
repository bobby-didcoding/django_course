# Django course - Module 5
This is my Django course. I hope you like it.

> These notes follow on from steps/module_4.md
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
git checkout module_5
git pull origin module_5
```


## Steps/Commands
>Note: Please 'cd' into the root directory and fire up your virtual environment!

Having user accounts on a website is massivley useful, both for customer engagement and retention, and in terms of gathering data which can be used for advertising purposes. Django has a built-in tool that help us deal with the complexities of managing and authenticating users. 

In this module, we will creating our own user profile model to capture user specific information. We will start a new application to group our common logic surrounding our users.

Lets get started.

1) Packages - We will be using a great library called Django extensions. This gives us access to some handy abstract models and functionality that I use daily. Let's go ahead and install the library and add it to our requirements.txt file.
```
pip install django-extensions pycountry
pip freeze > requirements.txt
```

1) Application - Open a terminal and use the following command to create a new app.
```
django-admin startapp users
```

Now open django_course/settings.py and register the new application in INSTALLED_APPS. Please use the following snippet.

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'users', # This is our new app
    'django_extensions', # This is the new extensions library
]   
```

3) Models - Open django_course/users/models.py and write our first model. A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.

```
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import pycountry
from operator import itemgetter

#these are model abstracts from django extensions
from django_extensions.db.models import (
    TimeStampedModel,
	ActivatorModel 
)

country_list = sorted(
        [(country.name, country.name) 
        for country in list(pycountry.countries)], key=itemgetter(0))

country_list.insert(0, ("*Select Country", "*Select Country"))

#(('United Kingdom', 'United Kingdom'), ('France', 'France').....)
COUNTRIES = country_list

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
    country = models.CharField(verbose_name="Country",max_length=100, null=True, blank=True, choices=COUNTRIES)

    longitude = models.CharField(verbose_name="Longitude",max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude",max_length=50, null=True, blank=True)

    @property
    def country_alpha_2(self):
        '''
        Used to return the selected countries alpha 2 repr i.e. England == GB
        '''
        if self.country:
            return pycountry.countries.get(name = self.country).alpha_2
        else:
            return None

    def full_name(self):
        '''
        Return full name or email
        '''
        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name.capitalize()} {self.user.last_name.capitalize()}'
        if self.user.email:
            return self.user.email
        return self.user.email

    def __str__(self):
        return self.full_name()
```

Django has some handy commands that quickly and easily create migration files. Use the following command to create our first migration files.
```
python manage.py makemigrations
```
You will see something similar to this in your log
```
Migrations for 'users':
  users\migrations\0001_initial.py
    - Create model UserProfile
```

Now open users\migrations\0001_initial.py. You will see the following code.
```
# Generated by Django 4.1 on 2022-08-13 05:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('telephone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Contact telephone number')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address')),
                ('town', models.CharField(blank=True, max_length=100, null=True, verbose_name='Town/City')),
                ('county', models.CharField(blank=True, max_length=100, null=True, verbose_name='County')),
                ('post_code', models.CharField(blank=True, max_length=8, null=True, verbose_name='Zip/Post Code')),
                ('country', models.CharField(blank=True, choices=[('*Select Country', '*Select Country'), ('Afghanistan', 'Afghanistan'), ...)], max_length=100, null=True, verbose_name='Country')),
                ('longitude', models.CharField(blank=True, max_length=50, null=True, verbose_name='Longitude')),
                ('latitude', models.CharField(blank=True, max_length=50, null=True, verbose_name='Latitude')),
                ('avatar', models.ImageField(blank=True, default='default_avatar.jpg', null=True, upload_to='avatar')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User profiles',
                'ordering': ['id'],
            },
        ),
    ]
```
This code is used to create the necessary SQL tables in our database.

Let's go ahead and migrate to our database. We have already used the following command in a pervious module. The migrate command cycles through the migration files and create/updates the SQL tables as necessary.
```
python manage.py migrate
```

You should see this in your terminal log
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, users
Running migrations:
  Applying users.0001_initial... OK
```

6) Admin - You can now register our UserProfile model to admin. This will allow us to manage UserProfile entries in the built-in admin page. open /users/admin.py and pase the following code into your editor.

```
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
```

You will now be able to manage UserProfile entries here [http://127.0.0.1:8000/admin/users/userprofile/](http://127.0.0.1:8000/admin/users/userprofile/).

>Note: You will notice that the superuser account that was created in the last module does not have a UserProfile. We will fix this.

5) Signals - Django includes a “signal dispatcher” which helps decoupled applications get notified when actions occur elsewhere in the framework. In a nutshell, signals allow certain senders to notify a set of receivers that some action has taken place. They’re especially useful when many pieces of code may be interested in the same events.
Let's go ahead and write some code that will create a UserProfile for every user that signs up (including superusers). Create a new file in /users called signals.py and paste in the following code.

```
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from . models import UserProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        obj, created = UserProfile.objects.get_or_create(user=instance)
```

The signal needs to be registered so that it is run every time a user signs up. Open /users/apps.py and past in the following code.

```
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
```

To test this functionality, sign into the built-in admin page and create a new user. Make sure you give this user 'staff' and 'superuser' privileges as this will become our new account.

If all went well, there should be a new UserProfile entry here [http://127.0.0.1:8000/admin/users/userprofile/](http://127.0.0.1:8000/admin/users/userprofile/).

To bookend signals, go ahead and delete our original user profile.
>Note: you will be asked to sign in again with the new details.


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
***
***