from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # felhasználó hozzáadása az adatbázishoz
        db.session.add(user)
        db.session.commit()
        flash('Sikeresen regisztrált! Most már bejelentkezhet.')

        # visszairányít a bejelentkezési oldalra
        return redirect(url_for('auth.login'))

    # regisztrációs oldal betöltése
    return render_template('auth/register.html', form=form, title='Regisztráció')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # a felhasználó létezik-e az adatbázisban
        # a megadott jelszó megegyezik-e az adatbázisban lévő jelszóval
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # felhasználó beléptetése
            login_user(user)

            # átirányítás a megfelelő irányítópultra
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # hibás belépési adatok
        else:
            flash('Hibás email cím vagy jelszó.')

    # bejelentkezési oldal betöltése
    return render_template('auth/login.html', form=form, title='Bejelentkezés')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sikeresen kijelentkezett.')

    # visszairányítás a bejelentkezési oldalra
    return redirect(url_for('auth.login'))
