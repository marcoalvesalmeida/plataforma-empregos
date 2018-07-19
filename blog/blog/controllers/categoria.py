from flask import Flask, session, render_template, jsonify, request
from blog import blog, db, lm, basebd
from blog.models.forms import CategoriaForm
from flask_login import current_user
from blog.models.tables import Empresa, Categoria

@blog.route("/categorias_form", methods=['GET'])
def categorias_form():
    if current_user.is_authenticated and session['tipo']=='empresa':
        return render_template('categorias.html', form=CategoriaForm())
    else:
        return render_template('error_403.html')


''' --------------  Métodos da API Rest para Categorias  ------------------ '''
@blog.route("/categoria", methods=['GET'])
def returnAllCategoria():
    categorias = Categoria.query.filter_by(id_empresa=current_user.id).all()
    lista = []
    for i in categorias:
        lista.append({'id':i.id, 'titulo':i.titulo})
    return jsonify({'categorias':lista})

@blog.route("/categoria", methods=['POST'])
def insertCategoria():
    titulo = request.json['titulo']
    empresa = request.json['empresa']
    resultado = {"status":0}
    if titulo and empresa:
        try:
            categoria = Categoria(titulo, empresa)
            db.session.add(categoria)
            db.session.commit()
            resultado = {"status":1}
        except Exception as e:
            db.session.rollback()
    return jsonify({"resultado":resultado})

@blog.route("/categoria/<string:id>", methods=['PUT'])
def updateCategoria(id):
    titulo = request.json['titulo']
    empresa = request.json['empresa']
    resultado = {"status":0}
    if titulo and empresa:
        categoria = Categoria.query.filter_by(id=id).first()
        categoria.titulo = titulo
        if str(categoria.id_empresa) == empresa:
            try:
                db.session.add(categoria)
                db.session.commit()
                print("CHegou aqui o danado")
                resultado = {"status":1}
            except Exception as e:
                db.session.rollback()
    return jsonify({"resultado":resultado})

@blog.route("/categoria/<string:id>", methods=['DELETE'])
def deleteCategoria(id):
    resultado = {"status":0}
    empresa = request.json['empresa']
    categoria = Categoria.query.filter_by(id=id).first()
    if str(categoria.id_empresa) == empresa:
        try:
            db.session.delete(categoria)
            db.session.commit()
            resultado = {"status":1}
        except Exception as e:
            db.session.rollback()
    return jsonify({"resultado":resultado})
