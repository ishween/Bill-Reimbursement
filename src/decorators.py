
"""
decorators to wrap functions with other functionality without modifying existing function
function is passed in the argument
In this if someone tries to directly reach to add dept/manager/employee/bill type without login we prevent the user to
access it by redirecting it back to login page.
One can directly reach by adding url to perform admins functions without login like http://127.0.0.1:4900/users/alerts
"""
from functools import wraps

from flask import session, redirect, url_for, request


def requires_login(function):
    @wraps(function)
    def login_alert(*args, **kwargs):  # args: func(6,7) arguments, kwargs(x=5, y=7) keyword arguments
        if 'email' not in session.keys() or session['email'] is None:
            redirect(url_for('admins.login_admin', next=request.path))
        return function(*args, **kwargs)
    return login_alert
