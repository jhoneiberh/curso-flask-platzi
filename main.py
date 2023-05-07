# python
from time import sleep

# flask
from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import render_template
from flask import abort

app = Flask(__name__)


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
    
    response.set_cookie('user_ip', user_ip)

    sleep(3)

    return response


@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    # return f'Hello World Flask, tu IP es {user_ip}'
    context = {
        'user_ip': user_ip,
        'todos': todos
    }
    return render_template('hello.html', **context)
