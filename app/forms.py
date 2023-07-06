from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField #Para importar los fields para el formulario
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')


class TodoForm(FlaskForm):
    description = StringField('Descripcion', validators=[DataRequired()])
    submit = SubmitField('Crear')


class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Borrar')