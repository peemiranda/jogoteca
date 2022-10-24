import os
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField


class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.data_required(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.data_required(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.data_required(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')


class FormularioUsario(FlaskForm):
    nickname = StringField('Nickname', [validators.data_required(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.data_required(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')


def recover_image(id):
    for archive_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in archive_name:
            return archive_name

    return 'capa_padrao.jpg'


def deleta_archive(id):
    archive = recover_image(id)
    if archive != 'capa_padrao':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], archive))
