from flask import session, redirect, url_for, g
from functools import wraps
from models import user as users, project as projects

def email_in_session_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not "email" in session:
            return redirect(url_for("login"))
        else:
            return f(*args, **kwargs)

    return wrapper

def load_project(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        project = projects.get_by_id(kwargs['project_id'])
        if project:
            g.project = project
            return f(*args, **kwargs)
    return wrapper

def load_user(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = users.get_by_email(session['email'])
        if user:
            g.user = user
            return f(*args, **kwargs)
    return wrapper

def user_in_project_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user_in_project = users.get_project_by_mail_by_id(session['email'], kwargs['project_id'])
        if user_in_project:
            g.user_in_project = user_in_project
            return f(*args, **kwargs)
        else:
            return redirect(url_for('user_home'))
    return wrapper

#Adds a "can" function to global
def checks_permission(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        #TODO: Could probably gain a couple milliseconds by storing as dict instead of list
        def can(*actions):
            role_permissions = g.user_in_project.role_permissions
            for action in actions:
                if action not in role_permissions:
                    return False
            return True
        g.can = can
        return f(*args, **kwargs)
    return wrapper
