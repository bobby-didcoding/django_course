# Django course - Module 1
This is my Django course. I hope you like it.

> These notes follow on from the README.md getting started instructions.
***
***

## Current root directory
Your root directory should look like the following.
```
django_course\  <--This is the root directory
    media\
        ...
    steps\
        ...
    >.gitignore
    >README.md
```
If in doubt, run the following git commands:
```
git checkout module_1
git pull origin module_1
```

## Steps/Commands
You should now have a directory called 'django_course' in your development directory. This will be known as your 'root directory'.

In this module, we will be start our project. To do this we will need to create a virtual environment.
>Note: Python virtual env docs can be found [here](https://docs.python.org/3/tutorial/venv.html).

1) Virtual Environment - Open a terminal and use the following command to create a virtual environment. 
```
python -m venv venv
```
Now activate the virtual environement with the following command.
```
# windows machine
venv\Scripts\activate.bat

#mac/linux
source venv/bin/activate
```
You will that your virtual environment is active when your terminal displays the following:
```
(venv) path\to\project\django_course>
```

2) Packages and requirements - Our project will rely on a whole bunch of 3rd party packages (requirements) to function. We will be using a Python package manager to install packages throughout this course. 
The first and most import package is, of course, Django! The following command will install Django into our virtual environment.
```
pip install django
```
We need a file to store a list of project requirements. This will help you when recreating the project in different environements. Use the following command to create a file called requirements.txt.
```
pip freeze > requirements.txt
```

3) Django - You can now go ahead and start a new Django project. Installing Django has given you access to a handy 'startproject' command. Use the following command to start our new project.
```
django-admin startproject django_course .
```

***
***

## New Root directory
>Note: If all went well, your root directory should now look like this
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

***
***