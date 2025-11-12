from flask import Flask, render_template, request
from flask import redirect, url_for, flash, session
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

app=Flask(__name__)

app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://root:root@localhost:3306/projeto?charset=utf8mb4'
)


db=SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__='usuario'
    IDusuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    print(f"[DEBUG] Recebido: nome={nome}, email={email}, login={login}")

    if not login or not nome:
        flash('Campos obrigatórios: login e nome', 'warning')
        return redirect(url_for('registrar'))

    if not senha:
        flash('Informe uma senha para cadastrar', 'warning')
        return redirect(url_for('registrar'))

    try:
        u = Usuario(login=login, nome=nome, email=email, senha=senha)
        db.session.add(u)
        db.session.commit()
        print("[DEBUG] Usuário inserido com sucesso!")
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('login_page'))
    except IntegrityError as e:
        db.session.rollback()
        print(f"[DEBUG] IntegrityError: {e}")
        flash('Login já cadastrado', 'danger')
        return redirect(url_for('registrar'))
    except Exception as e:
        db.session.rollback()
        print(f"[DEBUG] Erro geral: {e}")
        flash(f'Erro ao cadastrar: {str(e)}', 'danger')
        return redirect(url_for('registrar'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        user = Usuario.query.filter_by(email=email).first()
        if user and user.senha == senha:
            # login bem-sucedido, redireciona
            return redirect(url_for('inicio'))  
        else:
            return render_template('login.html', erro="Email ou senha incorretos")
    
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    # Destruição da sessão
    session.pop('usuario_id', None)
    flash('Você saiu da sessão.', 'info')
    return redirect(url_for('index.html'))



@app.route('/')
def inicial():
    return render_template('index.html')



   

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