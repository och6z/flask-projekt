from flask import abort, render_template
from flask_login import current_user, login_required

from . import home


@home.route('/')
def homepage():
    """
    Kezdőlap megjelenítése '/'
    """
    return render_template('home/index.html', title="Hello")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Irányítópult megjelenítése '/dashboard'
    """
    return render_template('home/dashboard.html', title="Irányítópult")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """
    Adminisztrátor irányítópult megjelenítése '/admin/dashboard'
    """
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Irányítópult")
