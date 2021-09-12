from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
from flask_bootstrap import Bootstrap
from werkzeug.datastructures import MultiDict
import os

# Genera clave secreta para flask_wtf
SECRET_KEY = os.urandom(32)


app = Flask(__name__)

ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///languages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLES
class NewLanguage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class Topics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)


app.config['SECRET_KEY'] = SECRET_KEY


# Table creator
# db.create_all()


# WTForms
class AddNewLanguage(FlaskForm):
    language = StringField("Nombre del nuevo lenguaje", validators=[DataRequired()])
    icon = StringField("Datos del icono")
    description = CKEditorField("Descripción del lenguaje", validators=[DataRequired()])
    img_url = StringField("Agregar url de la imangen", validators=[URL()])
    submit = SubmitField("Agregar lenguaje")


class AddNewTopic(FlaskForm):
    language_id = HiddenField()
    item_name = StringField("Agregar tema", validators=[DataRequired()])
    description = CKEditorField("Descripción del tema", validators=[DataRequired()])
    submit = SubmitField("Agregar")


@app.route('/')
def index():
    languages = NewLanguage.query.all()
    return render_template("index.html", languages=languages)


@app.route('/<language>')
def get_list(language):
    languages = NewLanguage.query.all()
    language_id = request.args.get("lang_id")
    language_selected = NewLanguage.query.get(language_id)
    topics_object = db.session.query(Topics).filter_by(language_id=language_id).all()
    return render_template("language_selected.html", languages=languages, topics=topics_object,
                           language=language_selected)


@app.route('/<language>/<topic>')
def get_topic(language, topic):
    languages = NewLanguage.query.all()
    topic_id = request.args.get("topic_id")
    lang_id = request.args.get("lang_id")
    a_class = 'stay_active'
    language_selected = NewLanguage.query.get(lang_id)
    print(a_class)
    topic_selected = Topics.query.get(topic_id)
    topics_object = db.session.query(Topics).filter_by(language_id=lang_id).all()
    return render_template("topic_selected.html", languages=languages, topics=topics_object, language=language_selected,
                           topic_selected=topic_selected, a_class=a_class)


@app.route('/add_lang', methods=["GET", "POST"])
def add_lang():
    languages = NewLanguage.query.all()
    language = False
    form = AddNewLanguage()
    if form.validate_on_submit():
        new_language = NewLanguage(
            language=form.language.data,
            icon=form.icon.data,
            description=form.description.data,
            img_url=form.img_url.data,
        )
        db.session.add(new_language)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_l_o_t.html", languages=languages, language=language, form=form)


@app.route('/add_topic', methods=["GET", "POST"])
def add_topic():
    languages = NewLanguage.query.all()
    language = request.args.get("lang_id")
    language_selected = NewLanguage.query.get(language)
    topics_object = db.session.query(Topics).filter_by(language_id=language).all()

    if request.method == 'POST':
        form = AddNewTopic()
    else:
        # Agrega un valor a un campo invisible
        form = AddNewTopic(formdata=MultiDict({'language_id': language}))

    if form.validate_on_submit():
        if form.validate_on_submit():
            new_topics = Topics(
                language_id=form.language_id.data,
                item_name=form.item_name.data,
                description=form.description.data,
            )
            db.session.add(new_topics)
            db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_l_o_t.html", languages=languages, form=form, lang_id=language, topics=topics_object,
                           language=language_selected)


if __name__ == "__main__":
    app.run(debug=True)
