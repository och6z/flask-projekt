from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import GroupForm, UserAssignForm, PermissionForm
from .. import db
from ..models import Group, User, Permission


def check_admin():
    # adminisztrátor jogosultsággal nem rendelkező felhasználóknak
    # hozzáférés megtagadva
    if not current_user.is_admin:
        abort(403)


# Csoport


@admin.route('/groups', methods=['GET', 'POST'])
@login_required
def list_groups():
    """
    Csoport lista
    """
    check_admin()

    groups = Group.query.all()

    return render_template('admin/groups/groups.html',
                           groups=groups, title="Csoportok")


@admin.route('/groups/add', methods=['GET', 'POST'])
@login_required
def add_group():
    """
    Csoport hozzáadása az adatbázishoz
    """
    check_admin()

    add_group = True

    form = GroupForm()
    if form.validate_on_submit():
        group = Group(name=form.name.data,
                                description=form.description.data)
        try:
            # csoport hozzáadása az adatbázishoz
            db.session.add(group)
            db.session.commit()
            flash('Sikeresen hozzáadott egy új csoportot.')
        except:
            # ha a csoport név létezik
            flash('Hiba: a csoport neve már létezik.')

        # visszairányítás a csoportok oldalra
        return redirect(url_for('admin.list_groups'))

    # csoport oldal betöltése
    return render_template('admin/groups/group.html', action="Add",
                           add_group=add_group, form=form,
                           title="Csoport hozzáadás")


@admin.route('/groups/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_group(id):
    """
    Csoport szerkesztés
    """
    check_admin()

    add_group = False

    group = Group.query.get_or_404(id)
    form = GroupForm(obj=group)
    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data
        db.session.commit()
        flash('Sikeresen szerkesztette a csoportot.')

        # visszairányítás a csoportok oldalra
        return redirect(url_for('admin.list_groups'))

    form.description.data = group.description
    form.name.data = group.name
    return render_template('admin/groups/group.html', action="Edit",
                           add_group=add_group, form=form,
                           group=group, title="Csoport szerkesztés")


@admin.route('/groups/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_group(id):
    """
    Csoport törlése az adatbázisból
    """
    check_admin()

    group = Group.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    flash('Sikeresen törölte a csoportot.')

    # visszairányítás a csoportok oldalra
    return redirect(url_for('admin.list_groups'))

    return render_template(title="Csoport törlés")


# Jogosultság


@admin.route('/permissions')
@login_required
def list_permissions():
    check_admin()
    """
    Jogosultság lista
    """
    permissions = Permission.query.all()
    return render_template('admin/permissions/permissions.html',
                           permissions=permissions, title='Jogosultságok')


@admin.route('/permissions/add', methods=['GET', 'POST'])
@login_required
def add_permission():
    """
    Jogosultság hozzáadása az adatbázishoz
    """
    check_admin()

    add_permission = True

    form = PermissionForm()
    if form.validate_on_submit():
        permission = Permission(name=form.name.data,
                    description=form.description.data)

        try:
            # jogosultság hozzáadása az adatbázishoz
            db.session.add(permission)
            db.session.commit()
            flash('Sikeresen hozzáadott egy új jogosultságot.')
        except:
            # ha a jogosultság név létezik
            flash('Hiba: a jogosultság neve már létezik.')

        # visszairányítás a jogosultságok oldalra
        return redirect(url_for('admin.list_permissions'))

    # jogosultság oldal betöltése
    return render_template('admin/permissions/permission.html', add_permission=add_permission,
                           form=form, title='Jogosultság hozzáadás')


@admin.route('/permissions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_permission(id):
    """
    Jogosultság szerkesztés
    """
    check_admin()

    add_permission = False

    permission = Permission.query.get_or_404(id)
    form = PermissionForm(obj=permission)
    if form.validate_on_submit():
        permission.name = form.name.data
        permission.description = form.description.data
        db.session.add(permission)
        db.session.commit()
        flash('Sikeresen szerkesztette a jogosultságot.')

        # visszairányítás a jogosultságok oldalra
        return redirect(url_for('admin.list_permissions'))

    form.description.data = permission.description
    form.name.data = permission.name
    return render_template('admin/permissions/permission.html', add_permission=add_permission,
                           form=form, title="Jogosultság szerkesztés")


@admin.route('/permissions/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_permission(id):
    """
    Jogosultság törlése az adatbázisból
    """
    check_admin()

    permission = Permission.query.get_or_404(id)
    db.session.delete(permission)
    db.session.commit()
    flash('Sikeresen törölte a jogosultságot.')

    # visszairányítás a jogosultságok oldalra
    return redirect(url_for('admin.list_permissions'))

    return render_template(title="Jogosultság törlés")


# Felhasználó

@admin.route('/users')
@login_required
def list_users():
    """
    Felhasználó lista
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Felhasználók')


@admin.route('/userss/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    """
    Csoport és jogosultság hozzárendelése a felhasználóhoz
    """
    check_admin()

    user = User.query.get_or_404(id)

    # adminisztrátorhoz csoport vagy jogosultság
    # hozzárendelés megtagadva
    if user.is_admin:
        abort(403)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.group = form.group.data
        user.permission = form.permission.data
        db.session.add(user)
        db.session.commit()
        flash('Sikeresen hozzáadott csoport és jogosultság.')

        # visszairányítás a felhasználók oldalra
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html',
                           user=user, form=form,
                           title='Felhasználó hozzárendelése')
