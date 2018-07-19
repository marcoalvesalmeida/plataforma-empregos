from flask import Flask, session, render_template, flash, url_for, redirect, jsonify, request
from blog import blog, db, lm, basebd
from blog.models.forms import LoginForm, CandidatoForm, EmpresaForm, AnuncioForm, CategoriaForm, CurriculoForm
from flask_login import login_user, logout_user, current_user
from blog.models.tables import Candidato, Empresa, Anuncio, Categoria, Curriculo
from datetime import date


''' --------------  Métodos da API Rest para Anúncio ------------------ '''
@blog.route("/anuncio", methods=['GET'])
def returnAllAnuncio():
    anuncios = Anuncio.query.filter_by(id_empresa=current_user.id).all()
    lista = []
    for i in anuncios:
        lista.append({'id':i.id, 'titulo':i.titulo, 'qtde_vagas': i.qtde_vagas, 'valor': float(i.valor)})
    return jsonify({'anuncios':lista})

@blog.route("/anuncio/<string:id>", methods=['GET'])
def returnOneAnuncio(id):
    anuncio = Anuncio.query.filter_by(id=id).first()
    lista = []
    lista.append({'id':anuncio.id, 'titulo':anuncio.titulo, 'qtde_vagas': anuncio.qtde_vagas, 'valor': float(anuncio.valor), 'descricao': anuncio.descricao, 'jornada': anuncio.jornada.name, 'categoria': anuncio.id_categoria})
    return jsonify({'anuncios':lista})


@blog.route("/anuncio", methods=['POST'])
def insertAnuncio():
    titulo = request.json['titulo']
    valor = request.json['valor']
    qtde_vagas = request.json['qtde_vagas']
    descricao = request.json['descricao']
    categoria = request.json['categoria']
    jornada = request.json['jornada']
    empresa = request.json['empresa']
    data_pub = date.today()
    resultado = {"status":0}
    if titulo and empresa:
        try:
            anuncio = Anuncio(titulo, descricao, valor, qtde_vagas, empresa, categoria, jornada, data_pub)
            db.session.add(anuncio)
            db.session.commit()
            resultado = {"status":1}
        except Exception as e:
            db.session.rollback()
    return jsonify({"resultado":resultado})


@blog.route("/anuncio/<string:id>", methods=['PUT'])
def updateAnuncio(id):
    resultado = {'status':0}
    titulo = request.json['titulo']
    valor = request.json['valor']
    qtde_vagas = request.json['qtde_vagas']
    descricao = request.json['descricao']
    categoria = request.json['categoria']
    jornada = request.json['jornada']
    empresa = request.json['empresa']
    anuncio = Anuncio.query.filter_by(id=id).first()
    if str(anuncio.id_empresa) == empresa:
        anuncio.titulo = titulo
        anuncio.valor = valor
        anuncio.qtde_vagas = qtde_vagas
        anuncio.descricao = descricao
        anuncio.id_categoria = categoria
        anuncio.jornada = jornada
        try:
            db.session.add(anuncio)
            db.session.commit()
            resultado = {'status': 1}
        except Exception as e:
            db.session.rollback()

    return jsonify({"resultado":resultado})

@blog.route("/anuncio/<string:id>", methods=['DELETE'])
def deleteAnuncio(id):
    resultado = {"status":0}
    empresa = request.json['empresa']
    anuncio = Anuncio.query.filter_by(id=id).first()
    if str(anuncio.id_empresa) == empresa:
        try:
            db.session.delete(anuncio)
            db.session.commit()
            resultado = {"status":1}
        except Exception as e:
            db.session.rollback()
    return jsonify({"resultado":resultado})


@blog.route("/listar_anuncios", methods=['GET'])
def listar_anuncios():
    if current_user.is_authenticated and session['tipo']=='empresa':
        lista = Anuncio.query.filter_by(id_empresa=current_user.id).all()
        return render_template('listaranuncios.html', lista=lista)
    else:
        return render_template('error_403.html')

@blog.route("/editar_anuncio", methods=['GET'])
def editar_anuncio():
    if current_user.is_authenticated and session['tipo']=='empresa':
        id = request.args['id']
        lista = Anuncio.query.filter_by(id=id).first().id
        return render_template('editaranuncio.html', current_anuncio=lista, form=AnuncioForm())
    else:
        return render_template('error_403.html')


@blog.route("/detalhes", methods=['GET'])
def detalhes():
    if current_user.is_authenticated:
        id = request.args['id']
        current_anuncio = Anuncio.query.filter_by(id=id).first()
        current_empresa = Empresa.query.filter_by(id=current_anuncio.id_empresa).first()
        categoria = Categoria.query.filter_by(id=current_anuncio.id_categoria).first().titulo
        return render_template('detalhes.html', current_anuncio=current_anuncio, current_empresa=current_empresa, anuncio_categoria=categoria)
