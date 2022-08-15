# Django course - Module 15
This is my Django course. I hope you like it.

> These notes follow on from steps/module_14.md
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
    ecommerce\
        __pycache__\
        migrations\
            __pycache__\
            >__init__.py
        templatetags\
            ecommerce\
                >__init__.py
                >ecommerce_tags.py
        >__init__.py
        >admin.py
        >apps.py
        >models.py
        >tests.py
        >urls.py
        >utils.py
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
        >alert.js
        >main.css
        >main.js
        >stripe.css
        >strip.js
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
git checkout module_15
git pull origin module_15
```

## Steps/Commands

>Note: Please 'cd' into the root directory and fire up your virtual environment!

Okay lets start where we left off in the last module. We now have views and url's all wired up. We now need to think about templates and static files.

Lets get started.

1) Templates - We need to create new html files for each of the main e-commerce views that we have created. Go ahead and create a new directory in /templates and call it ecommerce.

Create a new html file in /templates/ecommerce and call it items.html. Use the following code.
```
{% extends 'base/base.html' %}
{% load static  %}


{% block content %}
<h1>Shop items</h1>
<div class="row card-column">
  {% for object in object_list %}
  <div class="column">
    <div class="card">
      <img src="{{object.image.url}}" alt="{{object.title}}" style="width:100%">
      <h2>{{object.title}}</h2>
      <p class="price">{{object.variable_price}}</p>
      <p>{{object.description}}</p>
      <p><a class="btn btn-primary" href="{{object.get_absolute_url}}" >&#x2607;</a></p>
    </div>
  </div>
  {% endfor %}

  <div class="pagination">
    <span class="step-links">
        {% if page_obj.has_previous %}
            <a href="?page=1">&laquo; first</a>
            <a href="?page={{ page_obj.previous_page_number }}">previous</a>
        {% endif %}

        <span class="current">
            Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
        </span>

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">next</a>
            <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
        {% endif %}
    </span>
  </div>
</div>
{% endblock %}
```
Create a new html file in /templates/ecommerce and call it item.html. Use the following code.
```
{% extends 'base/base.html' %}
{% load static ecommerce_tags %}

{% block content %}

<h3>Item - {{object.title}}</h3>

<div class="container">
    <div class="row">
        <div class="col-6">
            <form>
                <label for="stock">Price per item</label>
                <input type="text" readonly value="{{object.variable_price}}">
                <label for="stock">Stock</label>
                <input type="text" name="stock-{{object.id}}" id="stock-input-{{object.id}}" class="stock-input-{{object.id}}" readonly value="{{object.stock}}">
                <label for="quantity">Quantity</label>
                <input type="number" min="1" name="quantity-{{object.id}}" id="quantity-input-{{object.id}}" class="quantity-input-{{object.id}}" value="0">
            </form>
        </div>
    <div class="col-6">
        <img src="{{object.image.url}}" alt="{{object.title}}" class="image">
    </div>
    
</div>
    {% item_button item %}
</div>
{% endblock %}
```

Create a new html file in /templates/ecommerce and call it cart.html. Use the following code.

```
{% extends 'base/base.html' %}
{% load static ecommerce_tags mathfilters %}

{% block content %}

<h1>Cart</h1>


<div class="row">
  <div class="col-75">
    {% for object in request.user.cart.items.all %}
    <div class="column item-list-{{object.item.id}}">
      <div class="card">
        
        <img src="{{object.item.image.url}}" alt="{{object.item.title}}" style="width:100%">
        <h2>{{object.item.title}}</h2>
        <p class="price">{{object.item.price}}</p>
        <p>{{object.item.description}}</p>
        <p>  
          <form>
            <div class="form-group row">
              <div class="col-sm-2">
              {% item_button_v2 object.item %}
              </div>
              <label for="quantity" class="col-sm-4 col-form-label">Quantity</label>
              <div class="col-sm-6">
                <input readonly class="form-control-plaintext" name="quantity-{{object.id}}" id="quantity-input-{{object.id}}" class="quantity-input-{{object.id}}" value="{{object.quantity}}">
              </div>
            </div>
            
          </form>
        </p>
        <p><a class="btn btn-primary" href="{{object.item.get_absolute_url}}" >&#x2607;</a></p>
      </div>
    </div>
    {% endfor %}
  </div>

  <div class="col-25">
    <div class="container">
      <h4>Summary
        <span class="price" style="color:black">
          <i class="fa fa-cart-shopping"></i>
          <b class="item-count">{{request.user.cart.item_count}}</b>
        </span>
      </h4>
      <hr>
      <p>Total <span class="price" style="color:black"><b class="item-total-price">£{{request.user.cart.amount|div:100}}</b></span></p>
      <p><a class="btn btn-success" href="{% url 'ecommerce:checkout' %}">Go to checkout</a></p>
    </div>
  </div>
</div>
{% endblock %}
```

Create a new html file in /templates/ecommerce and call it checkout.html. Use the following code.
```
{% extends 'base/base.html' %}
{% load static ecommerce_tags mathfilters djmoney %}

{% block extend_head %}
<link rel="stylesheet" href="{% static 'stripe.css' %}">
{% endblock %}

{% block extend_foot %}
<script src="https://js.stripe.com/v3/"></script>
<script src="https://polyfill.io/v3/polyfill.min.js?version=3.52.1&features=fetch"></script>
<script src="{% static 'stripe.js' %}" defer></script>
<script type="text/javascript">
    var stripe_key = '{{stripe_key|safe}}'
</script>
{% endblock %}

{% block content %}

<h1>Checkout</h1>

<div class="row">
    <div class="col-75">
      <div class="container">
        {% if sources.has_sources %}
        <h4>Select a card to use</h4>
        <table id="saved-cards">
            <thead>
            <tr>

                <th>Type</th>
                <th>Card Number</th>
                <th>Exp date</th>
                <th>Is default</th>
                <th>Action</th>
            </tr>
            </thead>
            <tbody>
            {% for s in sources.sources %}
            <tr>

                <td>{{s.type}}</td>
                <td>{{s.card}}</td>
                <td>{{s.exp}}</td>
                <td>{{s.default}}</td>
                <td>{% if not s.default %}<a class="btn btn-warning source" value="{{s.stripe_id}}" >Make default</a>{% endif %}</td>
            </tr>
            {% endfor %}
            </tbody>
        </table>

        <br>
        <a class="btn btn-warning pay" value="{{default_card.stripe_id}}" >Pay <i class="item-total-price">{{request.user.cart.amount|div:100}}</i> with default card</a>
        <br>

        {% endif %}
        <br>
        <h4>Pay with new card</h4>
        <form id="payment-form" style="width: 100%">
            {% csrf_token %}
            <div id="card-element"><!--Stripe.js injects the Card Element--></div>
            <button id="submit" type="submit">
            Pay <i class="item-total-price">£{{request.user.cart.amount|div:100}}</i> with new card
            </button>
            <p id="card-error" role="alert"></p>
            <p class="result-message hidden">
            Payment succeeded, see the result in your
            <a href="" target="_blank">Stripe dashboard.</a> Refresh the page to pay again.
            </p>
        </form>
      </div>
    </div>
  
    <div class="col-25">
      <div class="container">
        <h4>Cart
          <span class="price" style="color:black">
            <i class="fa fa-cart-shopping"></i>
            <b class="item-count">{{request.user.cart.item_count}}</b>
          </span>
        </h4>
        {% for object in request.user.cart.items.all %}
        <p class="item-list-{{object.item.id}}">{% item_button_v2 object.item %}
            <a href="{{object.item.content_object.get_absolute_url}}">{{object.item.content_object.title}}</a> <span class="price">£{{object.amount|div:100}}</span></p>
        {% endfor %}
        <hr>
        <p>Total <span class="price" style="color:black"><b class="item-total-price">£{{ request.user.cart.amount|div:100 }}</b></span></p>
      </div>
    </div>
  </div>
{% endblock %}
```
Create a new html file in /templates/ecommerce and call it orders.html. Use the following code.

```
{% extends 'base/base.html' %}
{% load static ecommerce_tags %}

{% block content %}

<h3>Order - {{object.item.title}}</h3>

<div class="container">
    <div class="row">
        <div class="col-6">
            <form>
                <label for="date">Date</label>
                <input type="text" readonly value="{{object.created}}">
                <label for="stock">Total price</label>
                <input type="text" readonly value="{{object.amount}}">
                <label for="quantity">Quantity</label>
                <input type="number" readonly value="{{object.quantity}}">
            </form>
        </div>
    <div class="col-6">
        <img src="{{object.item.image.url}}" alt="{{object.item.title}}" class="image">
    </div>
    
</div>
</div>
{% endblock %}
```

Create a new html file in /templates/ecommerce and call it order.html. Use the following code.

```
{% extends 'base/base.html' %}
{% load static ecommerce_tags %}

{% block content %}

<h3>Order - {{object.item.title}}</h3>

<div class="container">
    <div class="row">
        <div class="col-6">
            <form>
                <label for="date">Date</label>
                <input type="text" readonly value="{{object.created}}">
                <label for="stock">Total price</label>
                <input type="text" readonly value="{{object.amount}}">
                <label for="quantity">Quantity</label>
                <input type="number" value="{{object.quantity}}">
            </form>
        </div>
    <div class="col-6">
        <img src="{{object.item.image.url}}" alt="{{object.item.title}}" class="image">
    </div>
    
</div>
</div>
{% endblock %}
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
    ecommerce\
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
        >utils.py
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
        >alert.js
        >main.css
        >main.js
        >stripe.css
        >strip.js
    staticfiles\
    steps\
    templates\
        base\
            >base.html
        core\
            >index.html
        ecommerce\ <--New directory
            >cart.html
            >checkout.html
            >item_button_v2.html
            >item_button.html
            >item.html
            >items.html
            >order.html
            >orders.html
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