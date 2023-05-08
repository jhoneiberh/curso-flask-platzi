# python
from time import sleep

# flask
from flask import Flask
from flask import request, make_response, redirect, render_template, abort, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest


# Formulario
class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')




app = Flask(__name__)
bootstrap = Bootstrap(app)


app.config['SECRET_KEY'] = 'SUPER_SECRETO'

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)

todos = ['Comprar Café', 'Enviar Solicitud de Compra', 'Enviar reproductor']


@app.route('/')
def index():
    # abort(500) # levantar un error
    user_ip = request.remote_addr # ip del usuario

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip 
    
    # response.set_cookie('user_ip', user_ip)

    sleep(2)

    return response


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    user_ip = session.get('user_ip')
    
    login_form = LoginForm()

    username = session.get('username')

    # return f'Hello World Flask, tu IP es {user_ip}'
    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        flash('Nombre de usuario registrado con exito')

        return redirect(url_for('index'))

    return render_template('hello.html', **context)



if __name__ == '__main__':
    app.run(debug=True)