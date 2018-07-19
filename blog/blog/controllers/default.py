from flask import Flask, session, render_template, flash, url_for, redirect, jsonify, request
from blog import blog, db, lm, basebd
from blog.models.forms import LoginForm, CandidatoForm, EmpresaForm, AnuncioForm, CategoriaForm, CurriculoForm
from flask_login import login_user, logout_user, current_user
from blog.models.tables import Candidato, Empresa, Anuncio, Categoria, Curriculo
from datetime import date


client_id = '0c4587638f771f3eb41f'
secret_id = 'a175acd8452e6c41b8ada4818de60be9cdb31e6e'

@lm.user_loader
def load_user(id):
    if session['tipo'] == 'empresa':
        return Empresa.query.filter_by(id=id).first()
    elif session['tipo'] == 'candidato':
        return Candidato.query.filter_by(id=id).first()

@blog.route("/")
def index():
    if current_user.is_authenticated and session['tipo']=='empresa':
    	return render_template('painelempresa.html', form=AnuncioForm())
    elif current_user.is_authenticated and session['tipo']=='candidato':
        curriculo = Curriculo.query.filter_by(id_candidato=current_user.id).first().id
        return render_template('painelcandidato.html', form=CurriculoForm(), current_curriculo=curriculo)
    else:
        return render_template('inicio.html')

@blog.route("/configuracoes")
def configuracoes():
	return render_template('configuracoes.html')

@blog.route("/remover_conta")
def remover_conta():
    objeto = None
    if session['tipo'] == 'empresa':
        objeto = Empresa.query.filter_by(id=current_user.id).first()
    elif session['tipo'] == 'candidato':
        objeto = Candidato.query.filter_by(id=current_user.id).first()
    try:
        db.session.delete(objeto)
        db.session.commit()
        return render_template('login.html', form=LoginForm())
    except Exception as e:
        db.session.rollback()
        return render_template('error_unknown.html')

@blog.route("/perfil")
def perfil():
    if session['tipo'] == 'empresa':
        return render_template('perfilempresa.html', form=EmpresaForm())
    elif session['tipo'] == 'candidato':
        return render_template('perfilcandidato.html', form=CandidatoForm())

@blog.route("/anuncio_form", methods=['GET'])
def returnAll():
    lista = Anuncio.query.order_by(Anuncio.id).all()
    categorias = []
    for k in lista:
        categorias.append(k.titulo)

    a = jsonify({'categorias': categorias} )

    return render_template('error_403.html')


@blog.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        if session['tipo']=='candidato':
            return render_template('painelcandidato.html', form=CurriculoForm())
        elif session['tipo']=='empresa':
            return render_template('painelempresa.html', form=AnuncioForm())
    else:
        return render_template('login.html', form=form)

@blog.route("/logout")
def logout():
    logout_user()
    flash("Você saiu do sistema!")
    session.pop('tipo', None)
    return redirect(url_for("login"))

@blog.route('/verifica_login', methods=['POST'])
def verifica_login():
    form = LoginForm()
    valido = False
    email = form.email.data
    senha = form.senha.data
    tipo = form.tipo_usuario.data
    if tipo == 'empresa':
        empresa = Empresa.query.filter_by(email=email).first()
        if empresa and senha==empresa.senha:
            valido = "Empresa"
            tipo_usuario('empresa')
            login_user(empresa)
            return redirect('/painel_empresa')
        else:
            return render_template('login.html', msg="Email ou senha incorretos", tipo_msg="text-danger", form=form)
    elif tipo == 'candidato':
        candidato = Candidato.query.filter_by(email=email).first()
        if candidato and senha==candidato.senha:
            valido = "Candidato"
            tipo_usuario('candidato')
            curriculo = Curriculo.query.filter_by(id_candidato=candidato.id).first()
            if not curriculo:
                curriculo = Curriculo("","","",candidato.id, True)
                db.session.add(curriculo)
                db.session.commit()
            login_user(candidato)
            return redirect('/painel_candidato')
        else:
            return render_template('login.html', msg="Email ou senha incorretos", tipo_msg="text-danger", form=form)

def tipo_usuario(usuario):
    session['tipo'] = usuario
