from flask import Flask, render_template, request
from flask import redirect, url_for, flash, session
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

app=Flask(__name__,
          static_folder='assets',
          static_url_path='/assets',
          template_folder='templates')

app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://root:root@localhost:3306/projeto?charset=utf8mb4'
)


db=-SQLAlchemy(app)

class Usuario(db.model):
    __tablename__='usuarios'
    id = db.Column(db.integer, primary_key=True, unique=True, nullable=False,autoincrement=True)
    nome= db.Column(db.String(100), nullable=False)
    email= db.Column(db.String(100), nullable=False, unique=True)
    senha= db.Column(db.String(50), nullable=False)
    login= db.Column(db.String(45), unique=True, nullable=False)
    


@app.route('/usuarios/registrar', methods=['POST'])
def registrarUsuario():
    nome = (request.form.get('nome') or '').strip()
    email = (request.form.get('email') or '').strip()
    senha = (request.form.get('senha') or '').strip()
    login = (request.form.get('login') or '').strip()
  

    try:
        u = Usuario(login=login, nome=nome, email=email, senha=senha)
        db.session.add(u)
        db.session.commit()
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('login'))
    except IntegrityError:
        db.session.rollback()
        flash('Login já cadastrado', 'danger')
        return redirect(url_for('login'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cadastrar: {str(e)}', 'danger')
        return redirect(url_for('login'))




@app.route('/')
def inicial():
    return render_template('index.html')
   


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registrar')
def registrar():
    return render_template('registrar.html')



@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')


@app.route('/redefinir')
def redefinir():
    return render_template('redefinir.html')


@app.route('/codigo')
def codigo():
    return render_template('codigo.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')
   
@app.route('/agendar')
def agendar():
    return render_template('agendar.html')

@app.route('/meusagendamentos')
def meusagendamentos():
    return render_template('meusagendamentos.html')




if __name__ == '__main__':
    host= os.getenv('HOST','127.0.0.1')
    port= int(os.getenv('PORT','5000'))
    app.run(host=host, port=port ,debug=True)