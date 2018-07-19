from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from sqlalchemy.orm import sessionmaker
from flask_migrate import Migrate, MigrateCommand
from flask_login  import LoginManager
from sqlalchemy import create_engine



blog = Flask(__name__)
blog.config.from_object('config')
db = SQLAlchemy(blog)
migrate = Migrate(blog, db)

manager = Manager(blog)
manager.add_command('db', MigrateCommand)

lm = LoginManager()
lm.init_app(blog)

engine = create_engine('mysql://marco:0000@localhost/uruk')
Session = sessionmaker(bind=engine)
basebd = Session()

from blog.models import tables, forms
from blog.controllers import default, candidato, empresa, categoria, anuncio, curriculo
