from helpers import recover_image, deleta_archive, FormularioJogo
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db
from models import Jogos
import time


@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('list.html', title='Jogos', jogos=lista)


@app.route('/novo')
def new():
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login', next=url_for('new')))
    form = FormularioJogo()
    return render_template('new.html', title="Novo jogo", form=form)


@app.route('/criar', methods=['POST', ])
def create():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('new'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    new_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(new_jogo)
    db.session.commit()

    archive = request.files['archive']
    if archive:
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_archive(jogo.id)
        archive.save(f'{upload_path}/capa{new_jogo.id}-{timestamp}.jpg')

    flash('Jogo cadastrado com sucesso')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def edit(id):
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login', next=url_for('edit', id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    jogo_capa = recover_image(id)
    return render_template('edit.html', title="Editando jogo", id=id, jogo_capa=jogo_capa, form=form)


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        archive = request.files['archive']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_archive(jogo.id)
        archive.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def delete(id):
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login'))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso')
    return redirect(url_for('index'))


@app.route('/uploads/<archive_name>')
def image(archive_name):
    return send_from_directory('uploads', archive_name)
