from flask import session,Flask,render_template
from functools import wraps
 


def verify_login(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if('logged_in' in session) :
            print("logged in")
            return func(*args,**kwargs)
        return render_template('login.html')
    return wrapper

