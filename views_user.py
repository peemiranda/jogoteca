from app import app
from models import Usuarios
from helpers import FormularioUsario
from flask import render_template, request, redirect, session, flash, url_for
from flask_bcrypt import check_password_hash


@app.route('/login')
def login():
    proximo = request.args.get('next')
    form = FormularioUsario()
    return render_template('login.html', next=proximo, form=form)


@app.route('/autenticar', methods=['POST', ])
def authenticate():
    form = FormularioUsario(request.form)

    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)

    if usuario and senha:
        session['logged_in_user'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso!')
        next_page = request.form['next']
        return redirect(next_page)
    flash('Usuario não logado!')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['logged_in_user'] = None
    flash('Logout efetudado com sucesso!!')
    return redirect(url_for('index'))
