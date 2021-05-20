from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                # Redirect the user to an unauthorized notice!
                flash("Não tem permissão para aceder a esta pagina!", category="error")
                return redirect(url_for('views.dasboard'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

# Admin>Gerente>Supervisor>Operador