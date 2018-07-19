from flask import Flask, session, render_template, flash, url_for, redirect, jsonify, request
from blog import blog, db, lm, basebd
from blog.models.forms import LoginForm, CandidatoForm, EmpresaForm, AnuncioForm, CategoriaForm, CurriculoForm
from flask_login import login_user, logout_user, current_user
from blog.models.tables import Candidato, Empresa, Anuncio, Categoria, Curriculo
from datetime import date

@blog.route("/cadastrar_candidato_form", methods=['GET'])
def cadastrar_candidato_form():
    return render_template('cadastrarcandidato.html', form=CandidatoForm())



@blog.route("/painel_candidato", methods=['GET','POST'])
def painel_candidato():
    if current_user.is_authenticated:
        if session['tipo']=='candidato':
            curriculo = Curriculo.query.filter_by(id_candidato=current_user.id).first()
            return render_template('painelcandidato.html', form=CurriculoForm(), current_curriculo=curriculo)
        elif session['tipo']=='empresa':
            return render_template('error_403.html')
    else:
        return render_template('login.html', msg="Você deve estar logado!", form=LoginForm())

@blog.route("/buscar_vagas")
def buscar_vagas():
    if current_user.is_authenticated and session['tipo'] == 'candidato':
        lista_vagas = Anuncio.query.order_by(Anuncio.data_pub).all()
        for i in lista_vagas:
            lista_empresas = Empresa.query.filter_by(id=i.id_empresa).first().nome
        return render_template('buscarvagas.html', lista=lista_vagas, lista_empresas=lista_empresas)



''' --------------  Métodos da API Rest para Categorias  ------------------ '''
@blog.route("/candidato", methods=['GET'])
def returnAllCandidato():
    candidatos = Candidato.query.filter_by().all()
    lista = []
    for i in candidatos:
        lista.append({'id':i.id, 'nome':i.nome, 'cpf':i.cpf, 'escolaridade':i.escolaridade.name})
    return jsonify({'candidatos':lista})

@blog.route("/candidato/<string:id>", methods=['GET'])
def returnOneCandidato(id):
    candidato = Candidato.query.filter_by(id=id).first()
    lista = []
    lista.append({'id':candidato.id, 'nome':candidato.nome, 'cpf':candidato.cpf, 'escolaridade':candidato.escolaridade.name,  'email':candidato.email,  'bio':candidato.bio,  'data_nascimento':candidato.data_nascimento,  'sexo':candidato.sexo.name,  'estado_civil':candidato.estado_civil.name})
    return jsonify({'candidato':lista})


@blog.route("/candidato", methods=['POST'])
def insertCandidato():
    resultado = {"status":0}
    nome = request.json['nome']
    cpf = request.json['cpf']
    email = request.json['email']
    senha = request.json['senha']
    escolaridade = request.json['escolaridade']
    bio = request.json['bio']
    data_nascimento = request.json['data_nascimento']
    sexo = request.json['sexo']
    estado_civil = request.json['estado_civil']
    if nome and email and senha and escolaridade:
        try:
            candidato = Candidato(nome, cpf, email, senha, bio, data_nascimento, escolaridade, estado_civil, sexo)
            db.session.add(candidato)
            db.session.commit()
            resultado = {"status":1}
        except Exception as e:
            db.session.rollback()
    return jsonify({"resultado":resultado})


@blog.route("/candidato/<string:id>", methods=['PUT'])
def updateCandidato(id):
    resultado = {'status':0}
    nome = request.json['nome']
    cpf = request.json['cpf']
    email = request.json['email']
    senha = request.json['senha']
    escolaridade = request.json['escolaridade']
    bio = request.json['bio']
    data_nascimento = request.json['data_nascimento']
    sexo = request.json['sexo']
    estado_civil = request.json['estado_civil']
    candidato = Candidato.query.filter_by(id=id).first()
    if nome and email and senha and escolaridade:
        candidato.nome = nome
        candidato.cpf = cpf
        candidato.email = email
        candidato.senha = senha
        candidato.escolaridade = escolaridade
        candidato.bio = bio
        candidato.data_nascimento = data_nascimento
        candidato.sexo = sexo
        candidato.estado_civil = estado_civil
        try:
            db.session.add(candidato)
            db.session.commit()
            resultado = {'status': 1}
        except Exception as e:
            db.session.rollback()

    return jsonify({"resultado":resultado})
