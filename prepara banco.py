import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password=''
    )
    cursor = conn.cursor()

    cursor.execute("DROP DATABASE IF EXISTS 'jogateca_v1';")

    cursor.execute("CREATE DATABASE 'jogateca_v1';")

    cursor.execute("USE `jogateca_v1`;")

    # criando tabelas
    tables = {}
    tables['Games'] = ('''
          create table 'games' (
          'id' int(11) not null auto_increment
          'nome' varchar(50) not null,
          'categoria' varchar(40) not null,
          'console' varchar(20) not null,
          primary key ('id')
          ) engine=InnoDB default CHARSET=utf8 collate=utf8_bin;''')

    tables['users'] = ('''
          create table `users` (
          `name` varchar(20) NOT NULL,
          `nickname` varchar(8) NOT NULL,
          `password` varchar(100) NOT NULL,
          PRIMARY KEY (`nickname`)
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

    for table_name in tables:
        table_sql = tables[table_name]
        try:
            print('Criando tabela {}:'.format(table_name), end=' ')
            cursor.execute(table_sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('Já existe')
            else:
                print(err.msg)
        else:
            print('OK')

    # inserindo usuarios
    user_sql = 'INSERT INTO users (name, nickname, password) VALUES (%s, %s, %s)'
    users = [
        ("Pedro Miranda", "saitiay", "password"),
        ("Isabelli", "isaa_justi", "isa123"),
        ("Vitor Kato", "kami", "kami123"),
        ("Caio Precioso", "Caiudo", "caio123")
    ]
    cursor.executemany(user_sql, users)

    cursor.execute('select * from jogateca_v1.users')
    print(' -------------  usuarios:  -------------')
    for user in cursor.fetchall():
        print(user[1])

    # inserindo jogos
    games_sql = 'INSERT INTO games (name, category, console) VALUES (%s, %s, %s)'
    games = [
        ('Tetris', 'Puzzle', 'Atari'),
        ('God of War', 'Hack n Slash', 'PS2'),
        ('Mortal Kombat', 'Luta', 'PS2'),
        ('Valorant', 'FPS', 'PC'),
        ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
        ('Need for Speed', 'Corrida', 'PS2'),
    ]
    cursor.executemany(games_sql, games)

    cursor.execute('select * from jogateca_v1.games')
    print(' -------------  Jogos:  -------------')
    for game in cursor.fetchall():
        print(game[1])

    # commitando se não nada tem efeito
    conn.commit()

    cursor.close()
    conn.close()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)
