# Shortener

A simple URL shortening web app in written in Python using Django framework.

This web app includes the following function:
* An endpoint that receives a URL and returns a new shortened URL
* An endpoint to retrieve the last 100 shortened URLs
* An endpoint to retrieve the top 10 most popular shortened domains in the past month
* An endpoint to retrieve the number of times a shortened URL has been visited.


## Instructions
    (In the root folder of shortener)
1.  Install the python environment using `pipenv install` if you haven't had pipenv.
2.  Enter Pipenv by `pipenv shell`.
3.  Install Django by `pip install Django`.
5.  Install mathfilters `pip install django-mathfilters`.
6.  Run Django server by `python manage.py runserver`
    In your web browser, visit http://127.0.0.1:8000/
    To exit the running server: Ctrl + C
7.  To Exit pipenv, type `exit`.


# Note:
To directly access the database: `python manage.py dbshell`
