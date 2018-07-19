from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, DecimalField, IntegerField, DateField
from wtforms.validators import DataRequired, Email

class LoginForm(Form):
    email = StringField("email", validators=[DataRequired("É necessário informar seu nome!")])
    senha = PasswordField("senha", validators=[DataRequired("É necessário informar uma senha!")])
    tipo_usuario = SelectField('tipo_usuario', choices=[('candidato', 'Candidato'), ('empresa', 'Empresa')])

class CandidatoForm(Form):
    nome = StringField("nome", validators=[DataRequired("É necessário informar seu nome!")])
    cpf = StringField("cpf", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired("É necessário informar seu email!"), Email("Esse não é um email válido!")])
    senha = PasswordField("senha", validators=[DataRequired("É necessário informar uma senha!")])
    ocupacao = StringField("ocupacao")
    bio = TextAreaField("bio")
    data_nascimento = DateField("data_nascimento")
    escolaridade = SelectField('escolaridade', choices=[('superior_completo','Superior Completo'), ('superior_incompleto','Superior Incompleto'), ('medio_completo', 'Médio Completo'),( 'medio_incompleto','Médio Incompleto'), ('fundamental_completo', 'Fundamental Completo'), ('fundamental_incompleto', 'Fundamental Incompleto')])
    sexo = SelectField('sexo', choices=[('masculino','Masculino'), ('feminino','Feminino')])
    estado_civil = SelectField('estado_civil', choices=[('solteiro','Solteiro'), ('casado','Casado'), ('divorciado', 'Divorciado'), ('separado','Separado'), ('viuvo', 'Viúvo')])

class EmpresaForm(Form):
    nome = StringField("nome", validators=[DataRequired("É necessário informar o nome da sua empresa!")])
    cnpj = StringField("cnpj")
    email = StringField("email", validators=[DataRequired("É necessário informar um email da sua empresa!"), Email("Esse não é um email válido!")])
    senha = PasswordField("senha", validators=[DataRequired("É necessário informar uma senha!")])
    descricao = TextAreaField("descricao")
    website = StringField("website")

class AnuncioForm(Form):
    id = IntegerField('id')
    titulo = StringField("titulo", validators=[DataRequired("É necessário informar um título para o anúncio!")])
    valor = DecimalField("valor",  validators=[DataRequired("É necessário informar um valor para o anúncio!")], places=2, rounding=None, use_locale=False, number_format=None)
    qtde_vagas = IntegerField("qtde_vagas",  validators=[DataRequired("É necessário informar a quantidade vagas!")])
    descricao = TextAreaField("descricao", validators=[DataRequired("É necessário informar uma descrição para o anúncio!")])
    jornada = SelectField("jornada", choices=[('integral','Integral'), ('meio_periodo','Meio Período'),('estagio','Estágio'),('outro', 'Outra')])
    categoria =  StringField("categoria")

class CategoriaForm(Form):
    id = IntegerField('id')
    titulo = StringField("titulo", validators=[DataRequired("É necessário informar um título para a categoria!")])

class CurriculoForm(Form):
    id = IntegerField('id')
    formacao_academica =  StringField('formacao_academica')
    cursos_realizados = TextAreaField('cursos_realizados')
    experiencia_profissional = TextAreaField('experiencia_profissional')
