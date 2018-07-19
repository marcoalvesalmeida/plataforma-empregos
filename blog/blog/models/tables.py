from blog import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import backref
import enum

class EnumEstadoCivil(enum.Enum):
	solteiro = 'Solteiro'
	casado = 'Casado'
	divorciado = 'Divorciado'
	separado = 'Separado'
	viuvo = 'Viúvo'

class EnumSexo(enum.Enum):
    masculino = 'Masculino'
    feminino = 'Feminino'

class EnumEscolaridade(enum.Enum):
	superior_completo = 'Superior Completo'
	superior_incompleto = 'Superior Incompleto'
	medio_completo = 'Médio Completo'
	medio_incompleto = 'Médio Incompleto'
	fundamental_completo = 'Fundamental Completo'
	fundamental_incompleto = 'Fundamental Incompleto'

class EnumJornada(enum.Enum):
	integral = 'Integral'
	meio_periodo = 'Meio Período'
	estagio = 'Estágio'
	outra = 'Outra'

class Candidato(db.Model):
	__tablename__ = "candidato";
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(100))
	cpf = db.Column(db.String(15))
	email = db.Column(db.String(100), unique=True)
	senha = db.Column(db.String(50))
	data_nascimento = db.Column(db.Date)
	bio = db.Column(db.Text)
	escolaridade = db.Column(db.Enum(EnumEscolaridade))
	estado_civil = db.Column(db.Enum(EnumEstadoCivil))
	sexo = db.Column(db.Enum(EnumSexo))

	curriculo = db.relationship('Curriculo', backref="curriculox", passive_deletes=True)

	def __init__(self, nome, cpf, email, senha, bio, data_nascimento, escolaridade, estado_civil, sexo):
		self.senha = senha
		self.nome = nome
		self.cpf = cpf
		self.email = email
		self.data_nascimento = data_nascimento
		self.bio = bio
		self.escolaridade = escolaridade
		self.estado_civil = estado_civil
		self.sexo = sexo

	def __repr__(self):
		return "<Candidato %r>" % self.nome

	#Parte Responsável pelo Login abaixo
	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

class Empresa(db.Model):
	""" docstring for Empresa. """
	__tablename__ = "empresa"
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(100))
	descricao = db.Column(db.Text)
	cnpj = db.Column(db.String(20))
	email = db.Column(db.String(100))
	senha = db.Column(db.String(30))
	website = db.Column(db.String(100))

	categoria = db.relationship('Categoria', backref='categoriax', passive_deletes=True)
	anuncio = db.relationship('Anuncio', backref='anuncioax', passive_deletes=True)

	def __init__(self, nome, email, senha, cnpj, descricao, website):
		self.nome = nome
		self.email = email
		self.senha = senha
		self.cnpj = cnpj
		self.descricao = descricao
		self.website = website

	def __repr__(self):
		return "<Empresa %r>" % self.nome

	#Parte Responsável pelo Login abaixo
	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

class Categoria(db.Model):
	__tablename__ = "categoria"
	id = db.Column(db.Integer, primary_key=True)
	titulo = db.Column(db.String(200))
	id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id', ondelete='CASCADE'))

	anuncio = db.relationship('Anuncio', backref='anunciox', passive_deletes=True)

	def __init__(self,titulo, id_empresa):
		self.titulo = titulo
		self.id_empresa = id_empresa


class Anuncio(db.Model):
	__tablename__ = "anuncio"
	id = db.Column(db.Integer, primary_key=True)
	titulo = db.Column(db.String(200))
	jornada = db.Column(db.Enum(EnumJornada))
	qtde_vagas = db.Column(db.Integer())
	descricao = db.Column(db.Text)
	valor = db.Column(db.Numeric(10, 2))
	data_pub = db.Column(db.DateTime)
	id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id', ondelete='CASCADE'))
	id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id', ondelete='CASCADE'))


	def __init__(self, titulo, descricao, valor, qtde_vagas, id_empresa, id_categoria, jornada, data_pub):
		self.titulo = titulo
		self.descricao = descricao
		self.valor = valor
		self.qtde_vagas = qtde_vagas
		self.id_empresa = id_empresa
		self.id_categoria = id_categoria
		self.jornada = jornada
		self.data_pub = data_pub

	def __repr__(self):
		return "<Post %r>" % self.id

class Curriculo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	formacao_academica =  db.Column(db.String(100))
	cursos_realizados = db.Column(db.Text)
	experiencia_profissional = db.Column(db.Text)
	publico = db.Column(db.Boolean)
	id_candidato = db.Column(db.Integer, db.ForeignKey('candidato.id', ondelete='CASCADE'))

	def __init__(self, formacao_academica, cursos_realizados, experiencia_profissional, id_candidato, publico):
		self.formacao_academica = formacao_academica
		self.cursos_realizados = cursos_realizados
		self.experiencia_profissional = experiencia_profissional
		self.id_candidato = id_candidato
		self.publico = publico
