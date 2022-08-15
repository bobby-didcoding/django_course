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
        >stripe.js
    staticfiles\
    steps\
        >account.md
        >admin.md
        >basics.md
        >basics_part_2.md
        >debug.md
        >env.md
        >shop_part_one.md
        >style.md
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
    .env
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


3) Static files - Lastly, we need to create and import some JavaScript to tie all of our work together. 

Create a new html file in /static and call it stripe.js. Use the following code.

```
var stripe = Stripe(stripe_key);

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
base: {
  color: '#32325d',
  fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
  fontSmoothing: 'antialiased',
  fontSize: '16px',
  '::placeholder': {
    color: '#aab7c4'
  }
},
invalid: {
  color: '#fa755a',
  iconColor: '#fa755a'
}
};

// Create an instance of the card Element.
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
    displayError.textContent = event.error.message;
    } else {
    displayError.textContent = '';
    }
});

// Create a token or display an error when the form is submitted.
var form = document.getElementById('payment-form');


form.addEventListener('submit', function(event) {
  event.preventDefault();
  stripe.createToken(card).then(function(result) {
    if (result.error) {
      
      // Inform the customer that there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to your server.
      stripeTokenHandler(result.token);
    }
  });
});

function stripeTokenHandler(token) {
    // Insert the token ID into the form so it gets submitted to the server
    var form = document.getElementById('payment-form');
    var hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'stripeToken');
    hiddenInput.setAttribute('value', token.id);
    form.appendChild(hiddenInput);
    CustomFormSubmitPost($('#payment-form button[type=submit]'));
    $.ajax({
        method: "POST",
        url: "/pay/",
        data: {
          stripeToken: token.id,
        },
        success: function(data, textStatus, jqXHR){
          CustomFormSubmitResponse($('#payment-form button[type=submit]'));
          ShowAlert(data["result"], data["message"], data["result"].toLowerCase(), data["redirect"]);
        },
        error: function(xhr){
          console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}
```
Create a new html file in /static and call it stripe.css. Use the following code.

```
/* Variables */
* {
    box-sizing: border-box;
  }
  
  #payment-form {
    width: 30vw;
    min-width: 500px;
    align-self: center;
    box-shadow: 0px 0px 0px 0.5px rgba(50, 50, 93, 0.1),
      0px 2px 5px 0px rgba(50, 50, 93, 0.1), 0px 1px 1.5px 0px rgba(0, 0, 0, 0.07);
    border-radius: 7px;
    padding: 40px;
  }
  
  #payment-form input {
    border-radius: 6px;
    margin-bottom: 6px;
    padding: 12px;
    border: 1px solid rgba(50, 50, 93, 0.1);
    height: 44px;
    font-size: 16px;
    width: 100%;
    background: white;
  }
  
  .result-message {
    line-height: 22px;
    font-size: 16px;
  }
  
  .result-message a {
    color: rgb(89, 111, 214);
    font-weight: 600;
    text-decoration: none;
  }
  
  .hidden {
    display: none;
  }
  
  #card-error {
    color: rgb(105, 115, 134);
    text-align: left;
    font-size: 13px;
    line-height: 17px;
    margin-top: 12px;
  }
  
  #card-element {
    border-radius: 4px 4px 0 0 ;
    padding: 12px;
    border: 1px solid rgba(50, 50, 93, 0.1);
    height: 44px;
    width: 100%;
    background: white;
  }
  
  #payment-request-button {
    margin-bottom: 32px;
  }
  
  /* Buttons and links */
  #payment-form button {
    background: #9c07b6;
    color: #ffffff;
    font-family: Arial, sans-serif;
    border-radius: 0 0 4px 4px;
    border: 0;
    padding: 12px 16px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    display: block;
    transition: all 0.2s ease;
    box-shadow: 0px 4px 5.5px 0px rgba(0, 0, 0, 0.07);
    width: 100%;
  }
  #payment-form button:hover {
    background-color: #730786;
  }
  #payment-form button:disabled {
    opacity: 0.5;
    cursor: default;
  }
  
  /* spinner/processing state, errors */
  .spinner,
  .spinner:before,
  .spinner:after {
    border-radius: 50%;
  }
  .spinner {
    color: #ffffff;
    font-size: 22px;
    text-indent: -99999px;
    margin: 0px auto;
    position: relative;
    width: 20px;
    height: 20px;
    box-shadow: inset 0 0 0 2px;
    -webkit-transform: translateZ(0);
    -ms-transform: translateZ(0);
    transform: translateZ(0);
  }
  .spinner:before,
  .spinner:after {
    position: absolute;
    content: "";
  }
  .spinner:before {
    width: 10.4px;
    height: 20.4px;
    background: #5469d4;
    border-radius: 20.4px 0 0 20.4px;
    top: -0.2px;
    left: -0.2px;
    -webkit-transform-origin: 10.4px 10.2px;
    transform-origin: 10.4px 10.2px;
    -webkit-animation: loading 2s infinite ease 1.5s;
    animation: loading 2s infinite ease 1.5s;
  }
  .spinner:after {
    width: 10.4px;
    height: 10.2px;
    background: #5469d4;
    border-radius: 0 10.2px 10.2px 0;
    top: -0.1px;
    left: 10.2px;
    -webkit-transform-origin: 0px 10.2px;
    transform-origin: 0px 10.2px;
    -webkit-animation: loading 2s infinite ease;
    animation: loading 2s infinite ease;
  }
  
  @-webkit-keyframes loading {
    0% {
      -webkit-transform: rotate(0deg);
      transform: rotate(0deg);
    }
    100% {
      -webkit-transform: rotate(360deg);
      transform: rotate(360deg);
    }
  }
  @keyframes loading {
    0% {
      -webkit-transform: rotate(0deg);
      transform: rotate(0deg);
    }
    100% {
      -webkit-transform: rotate(360deg);
      transform: rotate(360deg);
    }
  }
  
  @media only screen and (max-width: 600px) {
    form {
      width: 80vw;
    }
  }
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
        >stripe.css <-- New file
        >stripe.js <-- New file
    staticfiles\
    steps\
        >account.md
        >admin.md
        >basics.md
        >basics_part_2.md
        >debug.md
        >env.md
        >shop_part_one.md
        >style.md
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
    .env
    >.gitignore
    >db.sqlite3
    >manage.py
    >README.md
    >requirements.txt
```

***
***