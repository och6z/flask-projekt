from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Group, Permission


class GroupForm(FlaskForm):
    """
    Adminisztrátori űrlap csoport hozzáadáshoz vagy szerkesztéshez
    """
    name = StringField('Név', validators=[DataRequired()])
    description = StringField('Leírás', validators=[DataRequired()])
    submit = SubmitField('Beküldés')


class PermissionForm(FlaskForm):
    """
    Adminisztrátori űrlap jogosultság hozzáadáshoz vagy szerkesztéshez
    """
    name = StringField('Név', validators=[DataRequired()])
    description = StringField('Leírás', validators=[DataRequired()])
    submit = SubmitField('Beküldés')


class UserAssignForm(FlaskForm):
    """
    Adminisztrátori űrlap csoport és jogosultság hozzárendeléshez
    """
    group = QuerySelectField(query_factory=lambda: Group.query.all(),
                                  get_label="name")
    permission = QuerySelectField(query_factory=lambda: Permission.query.all(),
                            get_label="name")
    submit = SubmitField('Beküldés')
