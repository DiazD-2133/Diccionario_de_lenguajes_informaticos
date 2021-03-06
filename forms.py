from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# Formulario para nuevo lenguaje
class AddNewLanguage(FlaskForm):
    language = StringField("Nombre del nuevo lenguaje", validators=[DataRequired()])
    icon = StringField("Datos del icono")
    description = CKEditorField("Descripción del lenguaje", validators=[DataRequired()])
    img_url = StringField("Agregar url de la imangen", validators=[URL()])
    submit = SubmitField("Agregar lenguaje")


# Formulario para nuevo tema
class AddNewTopic(FlaskForm):
    language_id = HiddenField()
    item_name = StringField("Agregar tema", validators=[DataRequired()])
    description = CKEditorField("Descripción del tema", validators=[DataRequired()])
    submit = SubmitField("Agregar")


# Formulario para registrar nuevo usuario
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


# Formulario para inicio de sesion
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")