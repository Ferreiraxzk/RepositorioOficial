from flask import Flask, render_template, request
from flask import redirect, url_for, flash, session
from functools import wraps
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text
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
    perfil= db.Column(db.String(20), nullable=False, default='professor')

class Kits(db.Model):
    __tablename__='kits_chromebooks'
    IDchromebooks = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    nome= db.Column(db.String(25), nullable=False)
    quantidade= db.Column(db.Integer, nullable=False)
    agendamentos = db.relationship("Agendamento", backref="kit", lazy=True)
class Agendamento(db.Model):
    __tablename__='agendamentos'
    IDagendamentos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    iDusuario = db.Column(db.Integer, db.ForeignKey('usuario.IDusuario'), nullable=False)
    IDchromebooks = db.Column(db.Integer, db.ForeignKey('kits_chromebooks.IDchromebooks'), nullable=False)
    professor = db.Column(db.String(45), nullable=False)
    turma = db.Column(db.String(10), nullable=False)  
    data = db.Column(db.Date, nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
  




#FUNÇÃO QUE SÓ PERMITE ADMINISTRADORES
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        uid = session.get('IDusuario')
        if not uid:
            flash('Faça login para continuar.', 'warning')
            return redirect(url_for('login'))
        user = Usuario.query.get(uid)
        if not user or user.perfil != 'adm':
            flash('Acesso restrito ao administrador.', 'danger')
            return redirect(url_for('inicio'))
        return f(*args, **kwargs)
    return wrapper

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('IDusuario'):
            flash('Faça login para continuar.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper





#CADASTRAR USUARIOS_____________________________
@app.route('/usuarios/registrar', methods=['POST'])
def registrarUsuario():
    nome = (request.form.get('nome') or '').strip()
    email = (request.form.get('email') or '').strip()
    senha = (request.form.get('senha') or '').strip()
    login = (request.form.get('login') or '').strip()
    perfil = (request.form.get('perfil') or 'professor').strip()

    print(f"[DEBUG] Recebido: nome={nome}, email={email}, login={login}")
        
    if not login or not nome:
        flash('Campos obrigatórios: login e nome', 'warning')
        return redirect(url_for('registrar'))

    if not senha:
        flash('Informe uma senha para cadastrar', 'warning')
        return redirect(url_for('registrar'))

    if perfil not in ['professor', 'adm']:
        perfil = 'professor'

    # validações de duplicidade antes de persistir
    if Usuario.query.filter_by(email=email).first():
        flash('E-mail já cadastrado', 'danger')
        return redirect(url_for('registrar'))

    if Usuario.query.filter_by(login=login).first():
        flash('Login já cadastrado', 'danger')
        return redirect(url_for('registrar'))

    try:
        u = Usuario(login=login, nome=nome, email=email, senha=senha, perfil=perfil)
        db.session.add(u)
        db.session.commit()
        print("[DEBUG] Usuário inserido com sucesso!")
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('login'))
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


#VALIDAR LOGIN_____________________________
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        user = Usuario.query.filter_by(email=email).first()
        if user and user.senha == senha:
            session['IDusuario'] = user.IDusuario
            session['perfil'] = user.perfil
            session['nome'] = user.login
            return redirect(url_for('inicio'))  
        else:
            return render_template('login.html', erro="Email ou senha incorretos")
    
    return render_template('login.html')







#CADASTRAR KITS_____________________________
@app.route('/registrar/kits', methods=['POST'])
@admin_required
def CadastrarKit():
    nome = (request.form.get('lote') or '').strip()
    quantidade = (request.form.get('quantidade_kit') or '').strip()

    print(f"[DEBUG] Recebido: lote={nome}, quantidade_kit={quantidade}")

    if not nome or not quantidade:
        flash('Campos obrigatórios: nome e quantidade', 'warning')
        return redirect(url_for('kits'))

    try:
        novo_kit = Kits(nome=nome, quantidade=int(quantidade))
        db.session.add(novo_kit)
        db.session.commit()

        print("[DEBUG] Kit inserido com sucesso!")
        flash('Kit criado com sucesso!', 'success')
        return redirect(url_for('inicio'))

    except Exception as e:
        db.session.rollback()
        print(f"[DEBUG] Erro ao cadastrar kit: {e}")
        flash(f'Erro ao cadastrar: {str(e)}', 'danger')
        return redirect(url_for('inicio'))







#rota de cadastro de agendamentos
@app.route('/registrar/agendamentos', methods=['POST'])
@login_required
def CadastrarAgendar():
    professor = request.form.get('professor')
    turma = request.form.get('turma')
    data_str = request.form.get('data')
    horario_raw = request.form.get('horario')
    quantidade = request.form.get('quantidade_agendar')
    kit = request.form.get('kit')

    if session.get('perfil') != 'professor':
        flash('Apenas professores podem agendar.', 'danger')
        return redirect(url_for('meusagendamentos'))

    # separar horario inicio e fim
    inicio_str, fim_str = horario_raw.split("|")

    horario_inicio = datetime.strptime(inicio_str, "%H:%M").time()
    horario_fim = datetime.strptime(fim_str, "%H:%M").time()

    data = datetime.strptime(data_str, "%Y-%m-%d").date()

    # Verifica conflitos de mesmo agendamento em um mesmo dia e horário para um kit
    conflitos = Agendamento.query\
        .filter(Agendamento.IDchromebooks == int(kit))\
        .filter(Agendamento.data == data)\
        .filter(Agendamento.horario_inicio < horario_fim)\
        .filter(Agendamento.horario_fim > horario_inicio)\
        .all()

    if conflitos:
        flash("Conflito de horário: já existe agendamento para este kit neste intervalo.", "danger")
        return redirect(url_for("agendar"))

    novo = Agendamento(
        professor=professor,
        turma=turma,
        data=data,
        horario_inicio=horario_inicio,
        horario_fim=horario_fim,
        quantidade=int(quantidade),
        IDchromebooks=int(kit),
        iDusuario=session.get('IDusuario')
    )

    db.session.add(novo)
    db.session.commit()

    flash("Agendamento criado com sucesso!", "success")
    return redirect(url_for("meusagendamentos"))





#rota de excluir agendamento
@app.route('/agendamento/excluir/<int:id>', methods=['POST'])
def excluir_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    #alter table status ativado para desativado
    db.session.delete(agendamento)
    db.session.commit()

    flash("Agendamento excluído com sucesso!", "success")
    return redirect(url_for("meusagendamentos"))





#rota de excluir kit
@app.route("/kits/excluir/<int:id>", methods=["POST"])
@admin_required
def excluir_kit(id):
    kit = Kits.query.get_or_404(id)

    try:
        db.session.delete(kit)
        db.session.commit()
        flash("Kit excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir kit: {e}", "danger")

    return redirect(url_for("kits"))  # Certifique-se de que existe uma rota chamada "kits"








#ROTA PARA FAZER BUTÃO SAIR DESLOGAR_____________________________
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('IDusuario', None)
    session.pop('perfil', None)
    session.pop('nome', None)
    flash('Você saiu da sessão.', 'info')
    return redirect(url_for('login'))
                            #pega função inicial da rota '/'






#SEÇÃO DE ROTAS_________________________________________________________________________
@app.route('/')
def inicial():
    return render_template('index.html')



@app.route("/kits")
@admin_required
def kits():
    lista_kits = Kits.query.all()
    return render_template("kits.html", kits=lista_kits)




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
   

# Realizar agendamento
@app.route('/agendar')
@login_required
def agendar():
    if session.get('perfil') != 'professor':
        flash('Apenas professores podem acessar o agendamento.', 'warning')
        return redirect(url_for('agendamentos_todos'))
    kits = Kits.query.all()
    return render_template('agendar.html', kits=kits)

# Exibe apenas os agendamentos do usuário logado para o perfil "adm"
@app.route('/meusagendamentos')
@login_required
def meusagendamentos():
    if session.get('perfil') == 'adm':
        return redirect(url_for('agendamentos_todos'))
    uid = session.get('IDusuario')
    agendamentos = Agendamento.query.filter_by(iDusuario=uid).all()
    return render_template("meusagendamentos.html", agendamentos=agendamentos, titulo="Meus Agendamentos")

# Exibe todos os agendamentos
@app.route('/agendamentos')
@login_required
def agendamentos_todos():
    agendamentos = Agendamento.query.all()
    return render_template("meusagendamentos.html", agendamentos=agendamentos, titulo="Agendamentos")


if __name__ == '__main__':
    host= os.getenv('HOST','127.0.0.1')
    port= int(os.getenv('PORT','5000'))
    app.run(host=host, port=port ,debug=True)
