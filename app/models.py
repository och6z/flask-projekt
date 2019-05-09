from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """
    'users' tábla létrehozása
    """


    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    permisson_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Rossz jelszó formátum
        """
        raise AttributeError('a jelszó nem olvasható.')

    @password.setter
    def password(self, password):
        """
        Jelszó hash
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Hash jelszó ellenőrzés
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# user_loader beállítás
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Group(db.Model):
    """
    'groups' tábla létrehozása
    """

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='group',
                                lazy='dynamic')

    def __repr__(self):
        return '<Group: {}>'.format(self.name)


class Permission(db.Model):
    """
    'permissions' tábla létrehozása
    """

    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='permission',
                                lazy='dynamic')

    def __repr__(self):
        return '<Permission: {}>'.format(self.name)
