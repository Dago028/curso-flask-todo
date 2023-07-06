from flask import render_template, session, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash #libreria para tratar contrasenhas
from app.forms import LoginForm

from . import auth
from app.firestore_service import get_user, user_put
from app.models import UserModel, UserData


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': LoginForm()
    }

    if login_form.validate_on_submit():
        username = login_form.username.data #Se usa DATA para traer el dato de la forma, si no, es solo una instancia del Field
        password = login_form.password.data

        user_doc = get_user(username)
        if user_doc.exists:
            password_from_db = user_doc.to_dict()['password']
            
            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                redirect(url_for('hello'))
            else:
                flash('Contraseña incorrecta')
        else:
            flash('El usuario no existe.')
        
        return redirect(url_for('index')) #Si se valida los datos ingresados retorna el index 
    
    return render_template('login.html', **context) #se renderea el login.html

@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)
        if not user_doc.exists: 
            password_hash = generate_password_hash(password) # se genera un hash con el password del usuario
            user_data = UserData(username, password_hash)
            user_put(user_data)

            user = UserModel(user_data)

            login_user(user)

            flash('Bienvenido/a')

            return redirect(url_for('hello'))
        else:
            flash('El usuario ya existe')

    return render_template('signup.html', **context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa Pronto')

    return redirect(url_for('auth.login')) 