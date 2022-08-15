# Django course - Module 10
This is my Django course. I hope you like it.

> These notes follow on from steps/module_9.md
***
***

## Current root directory
Your root directory should look like the following.
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
    mediafiles\
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
If in doubt, run the following git commands:
```
git checkout module_10
git pull origin module_10
```

## Steps/Commands

>Note: Please 'cd' into the root directory and fire up your virtual environment!

**Warning** we are about to switch things up a little. This is probably intermediate level but I'll go nice and slowly!!

When putting this course together I was scratching my head to figure out what type of website I could use for demo purposes. The consensus I got when asking around was e-commerce! So thats what we're going to do.

It's always good practice to group similar logic into its own application. We have a core app that handles basic webpage logic. We have a users app to handle user specific data. We now need to create an app to handle everything todo with selling products.

> Note: We will be using [Stripe](https://stripe.com/) to handle payments. However, the code we work through can easily be adapted for other payment processing platforms i.e. Braintree. Please go ahead and create a Stripe account as you'll need it to follow along with this tutorial.

Lets get started.

1) Libraries - There are some great libraries that can help with an e-commerce application. django-money is one of them. Let's get it installed.
```
pip install django-money requests stripe fontawesomefree django-mathfilters python-dateutil
pip freeze > requirements.txt
```

2) New application - If we are grouping e-commerce functionality, I think we should call our app 'ecommerce'. Run the following code to start a new app.
```
django-admin startapp ecommerce
```

Now register our new app and packages in /django_course/settings.py. Update the INSTALLED_APPS variable with the following.

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'ecommerce', # This is our new app
    'users', 
    'django_extensions',
    'djmoney',
    'fontawesomefree',
    'mathfilters',
]  
```

Also, change the TEMPLATES variable to the following.

>Note: we will create a context file in a moment as we will need to access INSTALLED_APPS in our templates.

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_course.context.project_context'
            ],
        },
    },
]
```
Now create a file called context.py in /django_course and add the following code.

```
from django.conf import settings

def project_context(request):
    return {
        "installed_apps": settings.INSTALLED_APPS,
    }
```

Whilst you are in settings.py, add the following variables.
>Note: You will need your test API keys from [Stripe](https://dashboard.stripe.com/test/apikeys)
```
STRIPE_SECRET_KEY = pk_test_xxx
STRIPE_PUBLISHABLE_KEY = sk_test_xxx
```

3) Models - We are going to need a whole bunch of new tables in our database. Go ahead and open /ecommerce/models.py and add the following code.

```
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from djmoney.models.fields import MoneyField
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)


class Item(
    TimeStampedModel,
    ActivatorModel ,
    TitleSlugDescriptionModel,
    models.Model):

    """
    ecommerce.Item
    Stores a single item entry for our shop
    """

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ["id"]
    
    image = models.ImageField(default='default_item_image.jpg', upload_to='items', null=True, blank=True)

    stock = models.IntegerField(default=1)
    variable_price = MoneyField(
        max_digits=14, 
        decimal_places=2, 
        default_currency='GBP', 
        null=True, 
        blank=True)

    def amount(self):
        amount = int(self.variable_price.amount * 100)
        return amount

    def get_absolute_url(self):
        return f'/item/{self.slug}/'
    

class CartItemManager(models.Manager):
    """
    A Manager for Cart item objects
    """
    def get_query_set(self):
        return self.get_queryset()

    def clear_items(self, user):
        '''
        Used to remove all cart items after payment is processed
        Useage - CartItem.objects.clear_items(auth.User)
        '''
        qs = self.get_query_set().filter(
            user = user
        )

        for q in qs:
            q.delete()



class CartItem(
    TimeStampedModel,
    ActivatorModel ,
    models.Model):
    """
    ecommerce.CartItem
    Stores a single item entry, related to :model:`ecommerce.Item` and
    :model:`auth.User`.
    """
    class Meta:
        verbose_name = 'Item for cart'
        verbose_name_plural = 'Item for cart'
        ordering = ["id"]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def amount(self):
        amount = self.item.amount() * self.quantity
        return amount

    objects = CartItemManager()


class Cart(
    TimeStampedModel,
    ActivatorModel ,
    models.Model):
    """
    ecommerce.Cart
    This is a Users Shopping cart, related to :model:`auth.User`.
    """

    class Meta:
        verbose_name = 'User cart'
        verbose_name_plural = 'User cart'
        ordering = ["id"]

    user = models.OneToOneField(User, on_delete=models.CASCADE)   
    items = models.ManyToManyField(CartItem, blank=True)

    def item_count(self):
        count = 0
        for obj in self.items.all():
            count += obj.quantity
        return count

    def amount(self):
        count = 0
        for obj in self.items.all():
            count += obj.amount()
        return int(count)

    def add_or_remove(self, action, object):
        '''
        Used to easily add or remove users to the cart model
        '''
        match action:
            case "add":
                if object not in self.items.all():
                    self.items.add(object)
            case "remove":
                self.items.remove(object)
        self.save()

    def item_check(self, item):
        '''
        Checks if an item is in the User cart
        '''
        cartitems = [i.item  for i in self.items.all()]
        if item in cartitems:
            return True
        return False

    def qty_check(self, item):
        try:
            cart_item = CartItem.objects.get(item = item, user = self.user)
            return cart_item.quantity
        except CartItem.DoesNotExist:
            return 0.0




class Source(
    TimeStampedModel,
    ActivatorModel ,
    models.Model):
    """
    ecommerce.Source
    Stores Stripe ID's for sources (payment methods).
    """
    class Meta:
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'
        ordering = ["id"]
    stripe_id = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)



class Line(
    TimeStampedModel,
    ActivatorModel ,
    models.Model):

    '''
    ecommerce.Line
    Stores a single line entry, related to :model:`ecommerce.Item` and
    :model:`auth.User`.
    '''
    class Meta:
        verbose_name = 'Invoice Line'
        verbose_name_plural = 'Invoice Lines'
        ordering = ["id"]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)   
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='GBP', null=True, blank=True)
    stripe_id = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1, blank=True,null=True)


class Invoice(
    TimeStampedModel,
    ActivatorModel ,
    models.Model):
    '''
    ecommerce.Invoice
    Stores a single invoice entry, related to :model:`ecommerce.Line`,
    :model:`ecommerce.Source` and :model:`auth.User`.
    '''
    class Meta:
        verbose_name = 'User Invoice'
        verbose_name_plural = 'User Invoices'
        ordering = ["id"]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)   
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, blank=True, null=True) 
    stripe_id = models.CharField(max_length=100)

    lines = models.ManyToManyField(Line, blank=True)

    def item_count(self):
        count = 0
        for obj in self.lines.all():
            count += obj.quantity
        return count

    def amount(self):
        count = 0
        for obj in self.lines.all():
            count += obj.buy_amount * obj.quantity
        return count

    def wallet(self):
        wallet = Wallet.objects.for_source(self.source)
        return wallet

class WalletManager(models.Manager):
    """
    A Manager for Wallet objects
    """
    def get_query_set(self):
        return self.get_queryset()

    def for_source(self, source):
        """
        Returns a Wallet objects queryset for a given source model.
        Usage:
            Source = Source.objects.first()
            Wallet.objects.for_source(Source)
        """
        qs = self.get_query_set().filter(
            sources=source
        )

        return qs

class Wallet(TimeStampedModel, ActivatorModel):
    '''
    ecommerce.Wallet
    Stores a single wallet entry related to :model:`ecommerce.Invoice`,
    :model:`ecommerce.Source` and :model:`auth.User`.
    '''
    class Meta:
        verbose_name = 'User Wallet'
        verbose_name_plural = 'User Wallets'
        ordering = ["id"]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=100, blank=True, null=True)
    invoices = models.ManyToManyField(Invoice, blank=True)
    sources = models.ManyToManyField(Source, blank=True)

    objects = WalletManager()
```

Now commit these changes to the database with the following commands.
```
python manage.py makemigrations
python manage.py migrate
```

4) Admin - As always, we will need to register the new models to admin. This will enable us to CRUD ecommerce models. Open /ecommerce/admin.py and add the following code.

```
from django.contrib import admin
from . import models


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item')

@admin.register(models.Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id','user')

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user' )

@admin.register(models.Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(models.Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ('id','created')

@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id',)
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
        >project_context.py <--New file
        >settings.py
        >urls.py
        >wsgi.py
    ecommerce\ <-- New application
        __pycache__\
        migrations\
            __pycache__\
            >__init__.py
            >0001_initial.py
        >__init__.py
        >admin.py
        >apps.py
        >models.py
        >tests.py
        >views.py
    media\
    mediafiles\
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