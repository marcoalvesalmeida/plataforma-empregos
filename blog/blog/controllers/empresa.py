from flask import Flask, session, render_template, flash, url_for, redirect, jsonify, request
from blog import blog, db, lm, basebd
from blog.models.forms import LoginForm, CandidatoForm, EmpresaForm, AnuncioForm, CategoriaForm, CurriculoForm
from flask_login import login_user, logout_user, current_user
from blog.models.tables import Candidato, Empresa, Anuncio, Categoria, Curriculo
from datetime import date

@blog.route("/alterar_empresa")
def alterar_empresa():
	return render_template('perfilempresa.html')

@blog.route("/cadastrar_empresa_form")
def cadastrar_empresa_form():
	return render_template('cadastrarempresa.html', form=EmpresaForm())


@blog.route("/painel_empresa", methods=['GET'])
def painel_empresa():
    if current_user.is_authenticated:
        if session['tipo']=='candidato':
            return render_template('error_403.html')
        elif session['tipo']=='empresa':
            lista_categorias = Categoria.query.filter_by(id_empresa = current_user.id).all()
            return render_template('painelempresa.html', form=AnuncioForm(), categorias = lista_categorias)
    else:
        return render_template('login.html',form=LoginForm())

''' --------------  Métodos da API Rest para Empresa  ------------------ '''
@blog.route("/empresa", methods=['GET'])
def returnAllEmpresa():
    empresas = Empresa.query.filter_by().all()
    lista = []
    for i in empresas:
        lista.append({'id': i.id, 'nome': i.nome})
    return jsonify({'empresas':lista})


@blog.route("/empresa/<string:id>", methods=['GET'])
def returnOneEmpresa(id):
    empresa = Empresa.query.filter_by(id=current_user.id).first()
    lista = []
    lista.append({'id':empresa.id, 'nome':empresa.nome, 'cnpj':empresa.cnpj, 'email':empresa.email,'descricao': empresa.descricao, 'website': empresa.website})
    return jsonify({'empresa':lista})

@blog.route("/empresa/<string:id>", methods=['PUT'])
def updateEmpresa(id):
	resultado = {"status":0}
	try:
		empresa = Empresa.query.filter_by(id=id).first()
		empresa.nome = request.json['nome']
		empresa.email = request.json['email']
		empresa.senha = request.json['senha']
		empresa.descricao = request.json['descricao']
		empresa.website = request.json['website']
		db.session.add(empresa)
		db.session.commit()
		resultado = {"status":1}
	except Exception as e:
		db.session.rollback()
		return e
	return jsonify({"resultado":resultado})

@blog.route("/empresa", methods=['POST'])
def insertEmpresa():
	resultado = {"status":0}
	nome = request.json['nome']
	cnpj = request.json['cnpj']
	email = request.json['email']
	senha = request.json['senha']
	descricao = request.json['descricao']
	website = request.json['website']
	if nome and email and senha:
		try:
			empresa = Empresa(nome, email, senha, cnpj, descricao, website)
			db.session.add(empresa)
			db.session.commit()
			resultado = {"status":1}
		except Exception as e:
		    db.session.rollback()
		return jsonify({"resultado":resultado})
