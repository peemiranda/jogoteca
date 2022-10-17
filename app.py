from flask import Flask, render_template, request, redirect, session, flash, url_for


class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console


game1 = Game('Counter-Strike', 'FPS', 'Computer')
game2 = Game('Fortnite', 'Battle-Royale', 'Cross plataform')
game3 = Game('Lol', 'Moba', 'Computer')
list = [game1, game2, game3]


class User:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = password


user1 = User("Pedro Miranda", "saitiay", "password")
user2 = User("Isabelli", "isaa_justi", "isa123")
user3 = User("Vitor Kato", "kami", "kami123")
user4 = User("Caio Precioso", "Caiudo", "caio123")

users = {user1.nickname: user1,
         user2.nickname: user2,
         user3.nickname: user3,
         user4.nickname: user4,
         }

app = Flask(__name__)
app.secret_key = 'password'


@app.route('/')
def index():
    return render_template('list.html', title='Jogos', games=list)


@app.route('/novo')
def new():
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login', next=url_for('new')))
    return render_template('new.html', title="Novo jogo")


@app.route('/criar', methods=['POST', ])
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    game = Game(name, category, console)
    list.append(game)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)


@app.route('/autenticar', methods=['POST', ])
def authenticate():
    if request.form['user'] in users:
        user = users[request.form['user']]
        if request.form['password'] == user.password:
            session['logged_in_user'] = user.nickname
            flash(user.nickname + ' logado com sucesso!')
            next_page = request.form['next']
            return redirect('/{}'.format(next_page))
            # return redirect(next_page)
    else:
        flash('Usuario não logado!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['logged_in_user'] = None
    flash('Logout efetudado com sucesso!!')
    return redirect(url_for('index'))


app.run(debug=True)
