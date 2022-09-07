# Django course - Module 13
This is my Django course. I hope you like it.

> These notes follow on from steps/module_12.md
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
        >urls.py
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
git checkout module_13
git pull origin module_13
```

## Steps/Commands

>Note: Please 'cd' into the root directory and fire up your virtual environment!

Okay lets start where we left off in the last module. We now have views and url's all wired up. We now need to think about templates and static files.

Lets get started.

2) Template Tags - We are referencing template tags in our new templates so we'll need to create these. Create a new directory in /ecommerce called templatetags.
Now create a new file called __init__.py and another called ecommerce_tags.py. copy the following code and add it to /ecommerce/templatetags/ecommerce_tags.py.

```
from django import template
from django.template.loader import render_to_string
from ..models import Item
from ..utils import EcommerceManager
register = template.Library()


@register.simple_tag(takes_context=True)
def item_button(context, target):
    '''
    Handles the logic for a button used to add items to a users cart.
    '''
    user = context['request'].user
    ecommerce_manager = EcommerceManager(user = user)

    # do nothing when user isn't authenticated
    if not user.is_authenticated:
        return ''

    target_model = '.'.join((target._meta.app_label, target._meta.object_name))
    undo = False
    cart = ecommerce_manager.cart_object()
    item_field = cart.items
    if cart.item_check(target):
        undo = True

    qty = cart.qty_check(target)

    return render_to_string(
        'ecommerce/item_button.html', {
            'target_model': target_model,
            'object_id': target.id,
            'object_quantity': qty,
            'object_stock': target.stock,
            'undo': undo,
            'item_count': item_field.all().count()
        }
    )

@register.simple_tag(takes_context=True)
def item_button_v2(context, target):
    '''
    Handles the logic for a button used to remove items to a users cart.
    '''
    user = context['request'].user
    ecommerce_manager = EcommerceManager(user = user)

    # do nothing when user isn't authenticated
    if not user.is_authenticated:
        return ''

    target_model = '.'.join((target._meta.app_label, target._meta.object_name))

    undo = False
    # prepare button to remove item if
    # already in cart

    cart = ecommerce_manager.cart_object()
    item_field = cart.items
    if cart.item_check(target):
        undo = True
    qty = cart.qty_check(target)
    return render_to_string(
        'ecommerce/item_button_v2.html', {
            'target_model': target_model,
            'object_id': target.id,
            'object_quantity': qty,
            'object_stock': target.stock,
            'undo': undo,
            'item_count': item_field.all().count()
        }
    )

```

We now need a directory in /templates to store our ecommerce application templates. When it's created you can go ahead and create a new html file in /templates/ecommerce and call it item_button.html. Use the following code.

```
{% load static %}

{% comment %} this adds an icon that, when clicked, allows users to add items to cart!! {% endcomment %}
<a class="item btn btn-success" model="{{ target_model }}" id="target_{{ object_id }}" action="add">
	<i class="item-{{object_id}} fa-solid fa-cart-plus"></i>
	<span class="item-count-{{ object_id }}"></span>
</a>
```

Create a new html file in /templates/ecommerce and call it item_button_v2.html. Use the following code.

```
{% load static %}

{% comment %} this adds an icon that, when clicked, allows users to remove items from cart!! {% endcomment %}
<a style="color:red;" class="item" model="{{ target_model }}" id="target_{{ object_id }}" action="remove"><i class="item-{{object_id}} fa-solid fa-close"></i></a>
```

Create a new html file in /static and call it main.js. Use the following code.

```
// Used to add a spinner to submit buttons
var temp_button_text;
function CustomFormSubmitPost(e) {
    var el = $(e);
    temp_button_text = el.text()
    el.attr('disabled', 'disabled').text("").append('<class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Loading...');
};
function CustomFormSubmitResponse(e) {
    var el = $(e);
    el.removeAttr('disabled').text(temp_button_text);
};


//ajax functions to alter tha like and bookmark buttons
"use strict";
var AJAXControls = function () {
    var item = function(){
        $('a.item').click(function() {
            var $obj = $(this);
            var target_id = $obj.attr('id').split('_')[1];
            var action = $obj.attr('action')
            var quantity = $('#quantity-input-'+target_id).val()
            $obj.prop('disabled', true);
            $.ajax({
                url: '/items/add-or-remove/',
                type: 'POST',
                data: {
                    target_model: $obj.attr('model'),
                    object_id: target_id,
                    object_quantity: quantity,
                    action: action
                },
                success: function(data) {
                    if (data["result"] == 'Success'){
                        $(".item-count").html(data["data"]["item_count"]);
                        $(".item-total-price").html(data["data"]["item_total_price"]);
                        $('#stock-input-'+target_id).val(data["data"]["stock"])
                        $('#quantity-input-'+target_id).val(0)
                        $obj.prop('disabled', false);
                        if (data["data"]["status"]=="remove"){
                            $(".item-list-" + target_id).remove();
                        }
                    }
                    ShowAlert(data["result"], data["message"], data["result"].toLowerCase(), data["redirect"]);
                }
            });
        });
    };

    var source = function(){
        $('a.source').click(function() {
            var $obj = $(this);
            var card_id = $obj.attr('value')
            $obj.prop('disabled', true);
            $.ajax({
                url: '/update-source/',
                type: 'POST',
                data: {
                    card_id: card_id,
                },
                success: function(data) {
                    ShowAlert(data["result"], data["message"], data["result"].toLowerCase(), data["redirect"]);
                }
            });
        });
    };

    var pay = function(){
        $('a.pay').click(function() {
            var $obj = $(this);
            var card_id = $obj.attr('value')
            $obj.prop('disabled', true);
            $.ajax({
                url: '/pay/',
                type: 'POST',
                data: {
                    card_id: card_id,
                },
                success: function(data) {
                    ShowAlert(data["result"], data["message"], data["result"].toLowerCase(), data["redirect"]);
                }
            });
        });
    };

    return {
        init: function () {
            item();
            source();
            pay();
        }
    };
}();

jQuery(document).ready(function () {
    AJAXControls.init();
});


$(function() {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
})

```
Create a new html file in /static and call it alert.js. Use the following code.

```
function ShowAlert(title, message, type, redirect) {
    if(redirect){
        toastr[type](message, title, {
            positionClass: 'toast-bottom-right',
            closeButton: true,
            progressBar: true,
            newestOnTop: true,
            rtl: $("body").attr("dir") === "rtl" || $("html").attr("dir") === "rtl",
            timeOut: 1000,
            onHidden: function () {
                window.location.assign(redirect);
            }
        });
    }
    else{
        toastr[type](message, title, {
            positionClass: 'toast-bottom-right',
            closeButton: true,
            progressBar: true,
            newestOnTop: true,
            rtl: $("body").attr("dir") === "rtl" || $("html").attr("dir") === "rtl",
            timeOut: 1000,
        });
    }
};
```

Lastly, open templates/base/base.html and replace the code with the following.

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
    
    <!-- Toastr alerts -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.css" integrity="sha512-3pIirOrwegjM6erE5gPSwkUzO+3cTjpnV9lexlNZqvupR64iZBnOOTiiLPb9M36zpMScbmUNIcHUqKD47M719g==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    
    <!--Fontawesome-->
    <script src="{% static 'fontawesomefree/js/all.min.js' %}"></script> 
    <script src="https://kit.fontawesome.com/8b7dd2a781.js" crossorigin="anonymous"></script>

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
        {% if 'ecommerce' in installed_apps %}
        <li><a {% if 'item' in request.path %}class="active"{% endif %}  href="{% url 'ecommerce:items' %}">Shop Items</a></li>
        <li><a {% if 'cart' in request.path %}class="active"{% endif %}  href="{% url 'ecommerce:cart' %}">Cart</a></li>
        <li><a {% if 'order' in request.path %}class="active"{% endif %}  href="{% url 'ecommerce:orders' %}">Orders</a></li>
        {% endif %}
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

    <!-- Toastr -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js" integrity="sha512-VEd+nq25CkR676O+pLBnDW09R7VQX9Mdiij052gVCp5yVH3jGtH70Ho/UUv4mJDsEdTvqRCFZg0NKGiojGnUCw==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

    <!--Our own j2-->
    <script src="{% static 'alert.js' %}"></script>
    <script src="{% static 'main.js' %}"></script>

    {% block extend_foot %}<!-- This allows us to extend the foot scripts in HTML docs that have special requirements-->{% endblock %}

    </body>
</html>
```

Now run the following code to round up all the new static files.
```
python manage.py collectstatic
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
    ecommerce\
        __pycache__\
        migrations\
            __pycache__\
            >__init__.py
        templatetags\ <-- New directory
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
        >alert.js <--New file
        >main.css
        >main.js <--New file
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
