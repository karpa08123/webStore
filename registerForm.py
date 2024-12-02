from wtforms import Form, StringField, IntegerField
from wtforms.validators import data_required, equal_to, length, Email, NumberRange
import email_validator # Dependencia necesaria para que validador de correo funcione

class Register(Form):
    # Campos necesarios: username | mail | names | lastNames | password | address | rfc

    username = StringField('username', validators=[length(min=3,max=25), data_required(message='El campo es obligatorio')])
    mail = StringField('mail', validators=[data_required(message='El campo es obligatorio'), Email(message="Use un correo valido")])
    names = StringField('names', validators=[length(min=1,max=25), data_required(message='El campo es obligatorio')])
    lastNames = StringField('lastNames', validators=[length(min=1,max=25), data_required(message='El campo es obligatorio')])
    password = StringField('password', validators=[length(min=1,max=25), data_required(message='El campo es obligatorio'), equal_to('password1',message="Las contraseñas no coinciden")])
    password1 = StringField('password1', validators=[length(min=1,max=25), data_required(message='El campo es obligatorio'), equal_to('password',message="Las contraseñas no coinciden")])
    address = StringField('address', validators=[length(min=1,max=25), data_required(message='El campo es obligatorio')])
    rfc = StringField('rfc', validators=[length(min=1,max=25), data_required(message='El campo es obligatorio')])

class Login(Form):
    username = StringField('username', validators=[length(min=3,max=25), data_required(message='El campo es obligatorio')])
    password = StringField('password', validators=[length(min=1,max=25), data_required(message='El campo es obligatorio')])

class Selling(Form):
    quantity = IntegerField('quantity', validators=[NumberRange(min=1, max=99, message='Ha excedido el numero maximo permitido')])
    articleId = StringField('articleId')