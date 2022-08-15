# Django course - Module 12
This is my Django course. I hope you like it.

> These notes follow on from steps/module_11.md
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
        >project_context.py
        >settings.py
        >urls.py
        >wsgi.py
    ecommerce\
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
        >utils.py
        >views.py
    media\
    mediafiles\
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
git checkout module_12
git pull origin module_12
```

## Steps/Commands

>Note: Please 'cd' into the root directory and fire up your virtual environment!

Okay lets start where we left off in the last module. We have built our database tables and spent some time creating an API manager. In this module, we will create the following views.
- Product/item listing page (shop)
- Product/Item detail page
- Cart
- Checkout
- Payment page
- Order listing page
- Order detail page

Lets get started.

1) Views - Open /ecommerce/views.py and add the following code.

```
from django.views import generic
from django.shortcuts import redirect, reverse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from . models import Item, CartItem, Source, Line
from .utils import EcommerceManager
from functools import wraps
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def ajax_required(f):
    """
    AJAX request required decorator
    """
    def wrap(request, *args, **kwargs):
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponseBadRequest('Invalid request')
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def empty_cart(function):
    """
    Decorator for views that checks if a user cart is empty.
    redirect user to /items/
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        ecommerce_manager = EcommerceManager(user = user)
        cart_obj = ecommerce_manager.cart_object()
        if cart_obj.items.all().count() == 0:
            return redirect(reverse('ecommerce:cart'))
        return function(request, *args, **kwargs)
    return wrap

class ItemsView(generic.ListView):
    """
    Listview that displays all active items in shop.

    Queryset of :model:`ecommerce.Item`.

    **Template:**

    :template:`ecommerce/items.html`
    """
    model = Item
    template_name = "ecommerce/items.html"
    paginate_by: int = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = Item.objects.active().filter(stock__gt=0)
        return qs

class ItemView(generic.DetailView):
    """
    Listview that displays individual item in shop.

    An instance of :model:`ecommerce.Item`.

    **Template:**

    :template:`ecommerce/item.html`
    """
    model = Item
    template_name = "ecommerce/item.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required
@ajax_required
def add_or_remove_item(request):
    """
    Function used to handle the adding and removing of items to cart.
    This is also where we handle stock.
    """
    data = {"result": "Error","message": "Something went wrong","redirect": False}
    try:
        obj_id = request.POST["object_id"]
    except (KeyError, ValueError):
        data["message"] = 'Invalid request'
        return JsonResponse(data)

    try:
        action = request.POST["action"]
    except (KeyError, ValueError):
        data["message"] = 'Invalid request'
        return JsonResponse(data)

    try:
        item = Item.objects.get(id = obj_id)
    except Item.DoesNotExist:
        data["message"] = 'Object does not exist'
        return JsonResponse(data)
    
    quantity = request.POST.get("object_quantity", 0)
    quantity = int(quantity)
    stock = item.stock
    cart_item, created = CartItem.objects.get_or_create(user = request.user, item = item)
    ecommerce_manager = EcommerceManager(request.user)
    cart = ecommerce_manager.cart_object()

    match action:
        case "remove":
            cart.add_or_remove(action, cart_item)
            qty = cart_item.quantity
            stock = stock + qty
            item.stock = stock
            item.save()
            cart_item.quantity = 0
            cart_item.save()
        case "add":
            if stock < quantity:
                data["message"] = 'Not enough stock'
                return JsonResponse(data)
            qty = cart_item.quantity
            cart.add_or_remove("add", cart_item)
            stock = stock - quantity
            item.stock = stock
            item.save()
            qty += quantity
            cart_item.quantity = qty
            cart_item.save()
    cart.save()

    item_count=cart.item_count()
    item_total_price=cart.amount()
    item_stock=stock
    data = {
            "result": "Success",
            "message": f'{item.title} has been {action}d to your cart',
            "redirect": False,
            "data": {
                "status": action,
                "item_count": item_count,
                "item_total_price": item_total_price,
                "stock": item_stock
            }
        }
    return JsonResponse(data)


class CartView(generic.TemplateView):
	"""
    TemplateView to display all items in a users cart.

    **Context**

    Stripe publishable key.

    **Template:**

    :template:`ecommerce/cart.html`
    """
	template_name = "ecommerce/cart.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["stripe_key"] = settings.STRIPE_PUBLISHABLE_KEY
		return context

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)



class CheckoutView(generic.TemplateView):
    """
    TemplateView to allow users to pay for all items in their cart.

    **Context**

    Stripe publishable key.
    sources - Queryset of :model:`ecommerce.Source`.
    default_card - An instance of :model:`ecommerce.Source`.

    **Template:**

    :template:`ecommerce/checkout.html`
    """
    template_name = "ecommerce/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stripe_key"] = settings.STRIPE_PUBLISHABLE_KEY
        ecommerce_manager = EcommerceManager(self.request.user)
        context["sources"] = ecommerce_manager.get_source_data()
        try:
            context["default_card"] = ecommerce_manager.wallet_object().sources.get(is_default=True)
        except Source.DoesNotExist:
            context["default_card"] = ""
        return context

    @method_decorator(login_required)
    @method_decorator(empty_cart)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@login_required
@ajax_required
def stripe_payment(request):
    """
    Function to handle the user payment
    """
    data = {"result": "Error","message": "Something went wrong","redirect": False}
    token = request.POST.get("stripeToken", None)
    source_id = request.POST.get("card_id", None)
    ecommerce_manager = EcommerceManager(request.user, token=token, source_id = source_id)
    invoice = ecommerce_manager.post_invoice()
    match invoice["status"]:
        case "200"|"201"|"202"|"203"|"204":
            data["redirect"] = "/"
            data["result"] = "Success"
            data["message"] = invoice["message"]
        case _:
            data["message"] = invoice["message"]
    return JsonResponse(data)


@login_required
@ajax_required
def update_source(request):
    """
    Function to source updates
    """
    data = {"result": "Error","message": "Something went wrong","redirect": False}
    card_id = request.POST.get("card_id", None)
    ecommerce_manager = EcommerceManager(request.user)
    ecommerce_manager.put_source(card_id)
    data["redirect"] = "/checkout/"
    data["result"] = "Success"
    data["message"] = "Your source has been updated"

    return JsonResponse(data)


class OrdersView(generic.ListView):
    """
    Listview that displays all orders made by user.

    Queryset of :model:`ecommerce.Line`.

    **Template:**

    :template:`ecommerce/orders.html`
    """
    model = Line
    template_name = "ecommerce/orders.html"
    paginate_by: int = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = Line.objects.active().filter(user = self.request.user)
        return qs

class OrderView(generic.DetailView):
    """
    DetailView that displays individual order.

    An instance of :model:`ecommerce.Line`.

    **Template:**

    :template:`ecommerce/order.html`
    """
    model = Line
    template_name = "ecommerce/order.html"

    def get_object(self):
        return Line.objects.get(id=self.kwargs['id'])

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
```


2) URL's - Like always, when we adjust our views we should then make sure we check our url's. In this case we need to create a new file called urls.py in /ecommerce. Create the file and user the following code.

```
from django.urls import path
from . import views

app_name = "ecommerce"

urlpatterns = [

    path('items/', views.ItemsView.as_view(), name='items'),
    path('item/<slug:slug>/', views.ItemView.as_view(), name='item'),
	path('items/add-or-remove/', views.add_or_remove_item, name='add_or_remove'),
	path('checkout/', views.CheckoutView.as_view(), name="checkout"),
	path('pay/', views.stripe_payment, name="pay"),
	path('cart/', views.CartView.as_view(), name="cart"),
	path('orders/', views.OrdersView.as_view(), name="orders"),
	path('order/<int:id>/', views.OrderView.as_view(), name="order"),
	path('update-source/', views.update_source, name="update-source"),
	]
```
You can now register the ecommerce app to the /django_course/urls.py file. use the following code.

```
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace="core")),
    path('', include('ecommerce.urls', namespace="ecommerce")),
    path('', include('users.urls', namespace="users")),
    path("__debug__/", include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
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
        >project_context.py
        >settings.py
        >urls.py
        >wsgi.py
    ecommerce\
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
        >urls.py <-- New file
        >utils.py
        >views.py
    media\
    mediafiles\
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

***
***