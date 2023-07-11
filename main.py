import unittest
from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user


from app import create_app
from app.forms import TodoForm, DeleteTodoForm
from app.firestore_service import get_users, get_todos, put_todo, delete_todo

app = create_app()

app.config['ENV'] = 'development' #No funciona

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.route('/')
@login_required
def index():
    user_ip = request.remote_addr
    
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response

''' El metodo recibe GET por defecto, pero para los formularios 
hay que agregar que recibe el metodo POST'''
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    user_ip = session.get('user_ip') 
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()

    context = {
                'user_ip': user_ip, 
                'todos': get_todos(user_id=username),
                'username': username,
                'todo_form': todo_form,
                'delete_form': delete_form,
               }
    
    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)

        flash('Tarea creada con exito!')

        return redirect(url_for('hello'))
    
    return render_template('hello.html', **context)


@app.route('/todos/delete/<todo_id>', methods=['POST']) #Rutas dinamicas, reciben parametros(sintaxis: <param1>) que despues son usadas en la funcion
def delete(todo_id):
    user_id = current_user.id 
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))
