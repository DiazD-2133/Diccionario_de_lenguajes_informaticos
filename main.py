from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
from flask_bootstrap import Bootstrap
import os

# Control de usuarios
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Importar formularios
from forms import AddNewLanguage, AddNewTopic, LoginForm, RegisterForm

# Se usa para pasar datos a los campos del formulario wtdforms
from werkzeug.datastructures import MultiDict

# Genera clave aleatoria para flask_wtf
SECRET_KEY = os.urandom(32)


# Crear decorador solo admin
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Si el id no es 1 entonces retorna abortar con error 403 error
        if current_user.id != 1:
            return abort(403)
        # De otra forma continua con la funcion
        return f(*args, **kwargs)
    return decorated_function


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

ckeditor = CKEditor(app)
Bootstrap(app)

# Conecta a la DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///languages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Configuracion de tablas
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


class NewLanguage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class Topics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)


# Crea las tablas en la DB
# db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Pagina de inicio
@app.route('/')
def index():
    languages = NewLanguage.query.all()
    return render_template("index.html", languages=languages)


# Constructor de la pagina del lenguage seleccionado
@app.route('/<language>')
def get_list(language):
    languages = NewLanguage.query.all()
    lang_list = []
    for lang in languages:
        lang_list.append(lang.language)
    if language in lang_list:
        language_selected = db.session.query(NewLanguage).filter_by(language=language).first()

        topics_object = db.session.query(Topics).filter_by(language_id=language_selected.id).all()
        return render_template("item_selected.html", languages=languages, topics=topics_object,
                               language=language_selected)
    language = lang_list[0]
    return render_template("item_selected.html", languages=languages, language=language)


# Constructor de la paguina del tema seleccionado
@app.route('/<language>/<topic>')
def get_topic(language, topic):
    languages = NewLanguage.query.all()
    topic_id = request.args.get("topic_id")
    lang_id = request.args.get("lang_id")
    a_class = 'stay_active'
    language_selected = NewLanguage.query.get(lang_id)
    topic_selected = Topics.query.get(topic_id)
    topics_object = db.session.query(Topics).filter_by(language_id=lang_id).all()
    return render_template("item_selected.html", languages=languages, topics=topics_object, language=language_selected,
                           topic_selected=topic_selected, a_class=a_class)


# Constructor de formulario para agregar nuevo lenguaje
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

        language = db.session.query(NewLanguage).filter_by(language=form.language.data).first()

        return redirect(url_for('get_list', language=language.language, lang_id=language.id))
    return render_template("add_l_o_t.html", languages=languages, language=language, form=form)


# Constructor de formulario para agregar nuevo tema
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
        language = NewLanguage.query.get(form.language_id.data)
        topic = db.session.query(Topics).filter_by(item_name=form.item_name.data).first()

        return redirect(url_for('get_topic', language=language.language, topic=topic.item_name, lang_id=language.id,
                                topic_id=topic.id))
    return render_template("add_l_o_t.html", languages=languages, form=form, lang_id=language, topics=topics_object,
                           language=language_selected)


# Constructor de formulario para editar lenguaje
@app.route("/edit-post/<int:language_id>", methods=["GET", "POST"])
def edit_post(language_id):
    language = NewLanguage.query.get(language_id)
    edit_form = AddNewLanguage(
        language=language.language,
        icon=language.icon,
        description=language.description,
        img_url=language.img_url,
    )
    if edit_form.validate_on_submit():
        language.language = edit_form.language.data
        language.icon = edit_form.icon.data
        language.description = edit_form.description.data
        language.img_url = edit_form.img_url.data
        db.session.commit()

        return redirect(url_for('get_list', language=language.language, lang_id=language.id))
    return render_template("add_l_o_t.html", language=language, form=edit_form, is_edit=True)


# Constructor de formulario para editar tema
@app.route("/topic-post/<int:topic_id>", methods=["GET", "POST"])
def edit_topic(topic_id):
    topic = Topics.query.get(topic_id)
    language = NewLanguage.query.get(topic.language_id)
    edit_form = AddNewTopic(
        language_id=topic.language_id,
        item_name=topic.item_name,
        description=topic.description,
    )

    if edit_form.validate_on_submit():

        topic.item_name = edit_form.item_name.data
        topic.description = edit_form.description.data
        db.session.commit()

        return redirect(url_for('get_topic', language=language.language, topic=topic.item_name, lang_id=language.id,
                                topic_id=topic.id))
    return render_template("add_l_o_t.html", language=language, form=edit_form, is_edit=True)


# Funcion de borrar
@app.route("/delete/<int:lang_id>")
def delete_language(lang_id):
    post_to_delete = NewLanguage.query.get(lang_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


# Registrar usuario(Solo importa para registrar al administrador id 1)
@app.route('/register', methods=["GET", "POST"])
def register():
    languages = NewLanguage.query.all()
    language = False

    form = RegisterForm()
    if form.validate_on_submit():

        # Si el correo ya existe
        if User.query.filter_by(email=form.email.data).first():

            # Muestra un mensaje flash
            flash("You've already signed up with that email, log in instead!")

            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()

        # Esta linea autentificara al usuario con Flask-Login
        login_user(new_user)
        return redirect(url_for("index"))

    return render_template("add_l_o_t.html", form=form, languages=languages, language=language)


# Iniciar sesion
@app.route('/login', methods=["GET", "POST"])
def login():

    languages = NewLanguage.query.all()
    language = False

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for("index"))

    return render_template("add_l_o_t.html", form=form, languages=languages, language=language)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
