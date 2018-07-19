from flask import Flask, session, render_template, flash, url_for, redirect, jsonify, request
from blog import blog, db, lm, basebd
from blog.models.forms import LoginForm, CandidatoForm, EmpresaForm, AnuncioForm, CategoriaForm, CurriculoForm
from flask_login import login_user, logout_user, current_user
from blog.models.tables import Candidato, Empresa, Anuncio, Categoria, Curriculo
from datetime import date


''' --------------  Métodos da API Rest para Currículo  ------------------ '''
@blog.route("/curriculo", methods=['GET'])
def returnAllCurriculo():
    curriculos = Curriculo.query.filter_by().all()
    lista = []
    for i in curriculos:
        lista.append({'id':i.id, 'nome':i.candidato.nome, 'escolaridade':i.candidato.escolaridade.name})
    return jsonify({'curriculos':lista})


@blog.route("/curriculo/<string:id>", methods=['GET'])
def returnOneCurriculo(id):
    curriculo = Curriculo.query.filter_by(id_candidato=current_user.id).first()
    candidato = Candidato.query.filter_by(id=current_user.id).first()
    lista = []
    lista.append({'id':curriculo.id, 'nome':candidato.nome, 'cpf':candidato.cpf, 'email':candidato.email, 'sexo':candidato.sexo.value, 'data_nascimento':candidato.data_nascimento, 'escolaridade':candidato.escolaridade.value, 'estado_civil':candidato.estado_civil.value, 'bio' : candidato.bio, 'formacao_academica':curriculo.formacao_academica, 'cursos_realizados':curriculo.cursos_realizados, 'experiencia_profissional': curriculo.experiencia_profissional})
    return jsonify({'curriculo':lista})


@blog.route("/curriculo/<string:id>", methods=['PUT'])
def updateCurriculo(id):
    publico = True
    resultado = {"status":0}
    try:
        curriculo = Curriculo.query.filter_by(id_candidato=id).first()
        curriculo.formacao_academica = request.json['formacao_academica']
        curriculo.cursos_realizados = request.json['cursos_realizados']
        curriculo.experiencia_profissional = request.json['experiencia_profissional']
        db.session.add(curriculo)
        db.session.commit()
        resultado = {"status":1}
    except Exception as e:
        db.session.rollback()
        return str(e)
    return jsonify({"resultado":resultado})


@blog.route("/curriculo/<string:id>", methods=['DELETE'])
def deleteCurriculo(id):
    resultado = {"status":0}
    curriculo = Curriculo.query.filter_by(id=id).first()
    if str(curriculo.id_candidato) == current_user.id:
        try:
            db.session.delete(curriculo)
            db.session.commit()
            resultado = {"status":1}
        except Exception as e:
            db.session.rollback()
    return jsonify({"resultado":resultado})

@blog.route("/mudar_status_curriculo", methods=['GET'])
def mudar_status_curriculo():
    if current_user.is_authenticated and session['tipo']=='candidato':
        curriculo = Curriculo.query.filter_by(id_candidato=current_user.id).first()
        if curriculo.publico:
            curriculo.publico = False
        else:
            curriculo.publico = True
        try:
            db.session.add(curriculo)
            db.session.commit()
            return render_template('painelcandidato.html', form=CurriculoForm(), current_curriculo=curriculo, msg="Visibilidade do currículo modificada!", tipo_msg="text-success")
        except Exception as e:
            db.session.rollback()
            return render_template('error_unknown.html')


@blog.route("/detalhes_curriculo", methods=['GET'])
def detalhes_curriculo():
    if current_user.is_authenticated:
        id = request.args['id']
        current_curriculo = Curriculo.query.filter_by(id=id).first()
        if(current_curriculo.publico == True):
            current_candidato = Candidato.query.filter_by(id=current_curriculo.id_candidato).first()
            return render_template('detalhescurriculo.html', current_curriculo=current_curriculo, current_candidato=current_candidato)
        else:
            return render_template('error_403.html')

@blog.route("/pesquisar_curriculos")
def pesquisar_curriculos():
    if current_user.is_authenticated and session['tipo'] == 'empresa':
        pesquisa = request.args['pesquisa']
        curriculo = basebd.query(Curriculo).join(Curriculo.id_candidato)
        print(curriculo.formacao_academica)
        return render_template('buscarcurriculos.html', lista=lista_curriculos)

@blog.route("/buscar_curriculos")
def buscar_curriculos():
    if current_user.is_authenticated and session['tipo'] == 'empresa':
        lista_curriculos = Curriculo.query.filter_by(publico=True).all()
        for i in lista_curriculos:
            i.id_candidato = Candidato.query.filter_by(id=i.id_candidato).first().nome
        return render_template('buscarcurriculos.html', lista=lista_curriculos)
