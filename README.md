# Django Login & Register
This a Django project that allows users to login to your website and allows them to register for an account as well! The HTML templates use the [Bootstrap login template](https://getbootstrap.com/docs/4.0/examples/sign-in/) and the user data is stored in a JSON file. You can use this in your website!

## Prerequisites:
* [Python](https://www.python.org/) Installed (I used 3.8.9)
* [Django](https://www.djangoproject.com/) installed. (I used 3.1.2)
* A Terminal.

You can install Django with:
```bash
pip install Django==3.1.2
```


You also have to enter the directory. You can do that with Terminal / Command Prompt:

```bash
cd django-login-and-register

```

Once that is done, you can run it on a localhost!

## Running The Server On Localhost

In your Terminal / Command Prompt, type the following:

```bash
pip install django-environ
python3 manage.py runserver

```
You would see some logs now. Ignore them. All you have to do is visit [`localhost:8000`](http://localhost:8000) on your browser. To stop the server, return to your terminal and press `CTRL-C`.