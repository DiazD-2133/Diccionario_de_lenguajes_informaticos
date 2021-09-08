from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
from flask_bootstrap import Bootstrap

import requests


response = requests.get("https://api.npoint.io/6a35337071c7dcfdbf27")
response = response.json()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=True)


class AgregarNuevoLenguaje(FlaskForm):
    language = StringField("Nombre del nuevo lenguaje", validators=[DataRequired()])
    icon = StringField("Datos del icono")
    description = CKEditorField("Descripción del lenguaje", validators=[DataRequired()])
    img_url = StringField("Agregar url de la imangen", validators=[URL()])
    submit = SubmitField("Submit Post")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", languages=response)


@app.route('/<language>')
def get_list(language):
    return render_template("language_selected.html", languages=response, language=language)


@app.route('/add_lang')
def add_lang():
    return render_template("language_selected.html")