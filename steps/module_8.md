# Django course - Module 8
This is my Django course. I hope you like it.

> These notes follow on from steps/module_7.md
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
        templates\
            users\
                >account.html
                >info.html
                >sign_in.html
                >sign_up.html
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
git checkout module_8
git pull origin module_8
```


## Steps/Commands

>Note: Please 'cd' into the root directory and fire up your virtual environment!

In this module we will start looking at Django template language. Why? well, our project looks terrible so we need to add some structure and styling. Django’s template language is designed to strike a balance between power and ease. It’s designed to feel comfortable to those used to working with HTML.

Lets get started.

1) CSS - CSS stands for Cascading Style Sheets. CSS describes how HTML elements are to be displayed on screen, paper, or in other media. CSS saves a lot of work. It can control the layout of multiple web pages all at once.
Create a file called main.css in /static and add the following snippet.
```
body {font-family: 'Courier Prime', monospace;}
* {box-sizing: border-box;}

body {

  margin: 0;
}

body, html, .map-container {
  height: 100%;
}

#map-route {
  height: 75%;
  }

.logo {
  width: 150px;
  padding: 8px;
}


ul.sidenav {
  list-style-type: none;
  margin: 0;
  padding: 0;
  width: 25%;
  background-color: #f1f1f1;
  position: fixed;
  height: 100%;
  overflow: auto;
}

ul.sidenav li a {
  display: block;
  color: #000;
  padding: 8px 16px;
  text-decoration: none;
}

ul.sidenav li a.active {
  background-color: #9c07b6;
  color: white;
}

ul.sidenav li a:hover:not(.active) {
  background-color: #555;
  color: white;
}

.div-container {

  margin-left: 25%;
  padding: 1px 16px;
  height: 1000px;
}

@media screen and (max-width: 900px) {
  ul.sidenav {
    width: 100%;
    height: auto;
    position: relative;
  }
  
  ul.sidenav li a {
    float: left;
    padding: 15px;
  }
  
  .div-container {margin-left: 0;}
}

@media screen and (max-width: 400px) {
  ul.sidenav li a {
    text-align: center;
    float: none;
  }
}

input[type=text], input[type=email], input[type=password], select, textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  margin-top: 6px;
  margin-bottom: 16px;
  resize: vertical;
}


::-webkit-input-placeholder { /* Edge */
  color: #9c07b6;
  font-family: 'Courier Prime', monospace;
}

:-ms-input-placeholder { /* Internet Explorer */
  color: #9c07b6;
  font-family: 'Courier Prime', monospace;
}

::placeholder {
  color: #9c07b6;
  font-family: 'Courier Prime', monospace;
}

select.selection option {
  color: #9c07b6;
  font-family: 'Courier Prime', monospace;
}

input, select {
  color: #9c07b6;
  font-family: 'Courier Prime', monospace;

}

/* The container */
.check-container {
  display: block;
  position: relative;
  padding-left: 35px;
  margin-bottom: 12px;
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

/* Hide the browser's default checkbox */
.check-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

/* Create a custom checkbox */
.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 15px;
  width: 15px;
  background-color: #fff;
}

/* On mouse-over, add a grey background color */
.check-container:hover input ~ .checkmark {
  background-color: #ccc;
}

/* When the checkbox is checked, add a green background */
.check-container input:checked ~ .checkmark {
  background-color: #9c07b6;
}

/* Create the checkmark/indicator (hidden when not checked) */
.check-container:after {
  content: "";
  position: absolute;
  display: none;
}

/* Show the checkmark when checked */
.check-container input:checked ~ .checkmark:after {
  display: block;
}

/* Style the checkmark/indicator */
.check-container .checkmark:after {
  left: 9px;
  top: 5px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 3px 3px 0;
  -webkit-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  transform: rotate(45deg);
}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #9c07b6;
}

input:focus + .slider {
  box-shadow: 0 0 1px #9c07b6;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

button[type=submit] {
  background-color: #9c07b6;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type=submit]:hover {
  background-color: #730786;
}

.container {
  border-radius: 5px;
  background-color: #f2f2f2;
  padding: 20px;
}

table {
  font-family: 'Courier Prime', monospace;
  border-collapse: collapse;
  width: 100%;
}

table td, table th {
  border: 1px solid #ddd;
  padding: 8px;
}

table tr:hover {background-color: #ddd;}

table th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #9c07b6;
  color: white;
}

.selected {
  background-color: #730786;
  color: #FFF;
}

#payment-form {
  width: 100%;
}

/* style inputs and link buttons */
input, select,
.btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 4px;
  margin: 5px 0;
  opacity: 0.85;
  display: inline-block;
  font-size: 17px;
  line-height: 20px;
  text-decoration: none; /* remove underline from anchors */
}

input:hover,
.btn:hover {
  opacity: 1;
}

.img-container {
  position: relative;
  width: 50%;
}

.image {
  opacity: 1;
  display: block;
  width: 100%;
  height: auto;
  transition: .5s ease;
  backface-visibility: hidden;
}

.img-overlay {
  transition: .5s ease;
  opacity: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%)
}

.img-container:hover .image {
  opacity: 0.3;
}

.img-container:hover .img-overlay {
  opacity: 1;
}

.img-text {
  background-color: #9c07b6;
  color: white;
  font-size: 16px;
  padding: 16px 32px;
}

.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  max-width: 300px;
  margin: auto;
  text-align: center;
  font-family: arial;
}

.price {
  color: grey;
  font-size: 22px;
}

.card button {
  border: none;
  outline: 0;
  padding: 12px;
  color: white;
  background-color: #000;
  text-align: center;
  cursor: pointer;
  width: 100%;
  font-size: 18px;
}

.card button:hover {
  opacity: 0.7;
}

* {
  box-sizing: border-box;
}

.row {
  display: -ms-flexbox; /* IE10 */
  display: flex;
  -ms-flex-wrap: wrap; /* IE10 */
  flex-wrap: wrap;
  margin: 0 -16px;
}

.col-25 {
  -ms-flex: 25%; /* IE10 */
  flex: 25%;
}

.col-50 {
  -ms-flex: 50%; /* IE10 */
  flex: 50%;
}

.col-75 {
  -ms-flex: 75%; /* IE10 */
  flex: 75%;
}

.col-25,
.col-50,
.col-75 {
  padding: 0 16px;
}

.container {
  background-color: #f2f2f2;
  padding: 5px 20px 15px 20px;
  border: 1px solid lightgrey;
  border-radius: 3px;
}

input[type=text] {
  width: 100%;
  margin-bottom: 20px;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

label {
  margin-bottom: 10px;
  display: block;
}

.icon-container {
  margin-bottom: 20px;
  padding: 7px 0;
  font-size: 24px;
}



.btn:hover {
  background-color: #45a049;
}

a {
  color: #2196F3;
}

hr {
  border: 1px solid lightgrey;
}

span.price {
  float: right;
  color: grey;
}

/* Responsive layout - when the screen is less than 800px wide, make the two columns stack on top of each other instead of next to each other (also change the direction - make the "cart" column go on top) */
@media (max-width: 800px) {
  .row {
    flex-direction: column-reverse;
  }
  .col-25 {
    margin-bottom: 20px;
  }
}

/* Float four columns side by side */
.column {
  float: left;
  width: 25%;
  padding: 0 10px;
}
/* Remove extra left and right margins, due to padding in columns */
.row {margin: 0 -5px;}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}
/* Responsive columns - one column layout (vertical) on small screens */
@media screen and (max-width: 600px) {
  .column {
    width: 100%;
    display: block;
    margin-bottom: 20px;
  }
}

.pagination {
  display: inline-block;
  position: fixed;     
     text-align: center;    
     bottom: 0px; 
     width: 100%;
}

.pagination a {
  color: black;
  float: left;
  padding: 8px 16px;
  text-decoration: none;
}

.pagination a.active {
  background-color: #4CAF50;
  color: white;
  border-radius: 5px;
}

.pagination a:hover:not(.active) {
  background-color: #ddd;
  border-radius: 5px;
}
```
You will need to run the following command to ensure Django picks up the new file when rendering each page.
```
python manage.py collectstatic
```

2) HTML structure - Django template language gives us access to a whole range of variables, filters and tags that help us add logic to our HTML files. Let's begin by changing our template structure. Create the following directory structure in root directory.
```
django_course\ <--- Root directory
    ...
    templates\
        base\
            >base.html
        core\ <--- Copy this over from your core add templates
        users\ <--- Copy this over from your users app templates
    ...
```
>Note: You can delete the template folders in core and users when you have moved them over to /templates.

Add the following snippet to /templates/base/base.html.
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

    <!--Bootstrap-->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

    {% block extend_foot %}<!-- This allows us to extend the foot scripts in HTML docs that have special requirements-->{% endblock %}

    </body>
</html>
```
We now have a base HTML file that we can build on. We can now go ahead and update our core and user templates.

Open /templates/core/index.html and paste in the following snippet.
```
{% extends 'base/base.html' %}

{% block content %}
<h1>Welcome to our Django course</h1>
{% endblock %}
```

Open /templates/users/account.html and paste in the following snippet.
```
{% extends 'base/base.html' %}

{% block content %}
<h1>Welcome to your account {{request.user.userprofile.full_name}}</h1>
<form method="POST">
    {% csrf_token %}
    {{form.as_p}}
    <button type="submit">Submit!</button>
</form>
{% endblock %}
```

Open /templates/users/info.html and paste in the following snippet.
```
{% extends 'base/base.html' %}

{% block content %}
<h1>Info - {{request.user.userprofile.full_name}}</h1>
<form method="POST">
    {% csrf_token %}
    {{form.as_p}}
    <button type="submit">Submit!</button>
</form>
{% endblock %}
```

Open /templates/users/sign_in.html and paste in the following snippet.
```
{% extends 'base/base.html' %}

{% block content %}
<h1>Sign in</h1>
<form method="POST">
    {% csrf_token %}
    {{form.as_p}}
    <button type="submit">Submit!</button>
</form>
<br>
<a href="{% url 'users:sign-up' %}">Sign up</a>
{% endblock %}
```

Open /templates/users/sign_up.html and paste in the following snippet.
```
{% extends 'base/base.html' %}

{% block content %}
<h1>Sign up</h1>
<form method="POST">
    {% csrf_token %}
    {{form.as_p}}
    <button type="submit">Submit!</button>
</form>
<br>
<a href="{% url 'users:sign-in' %}">Sign in</a>
{% endblock %}
```

3) New settings - Our new template structure is easier to understand. However, Django needs to know where to look for the new templates. Update the 'TEMPLATES' variable in /django_course/settings.py with the following.
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
            ],
        },
    },
]
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
        >main.css <-- New file
    staticfiles\
    steps\
    templates\ <-- New directory
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
