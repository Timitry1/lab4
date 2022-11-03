import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="PlayBoy100",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


# @app.route('/login/', methods=['POST'])
# def loginn():
#     username = request.form.get('username')
#     password = request.form.get('password')
    # if len("".join(username.split())) == 0 or len("".join(password.split())) == 0:
    #     error = 'ошибка №1'
    #     return render_template('login.html', error=error)
    # cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    # records = list(cursor.fetchall())
    # if len(records) == 0:
    #     errorLogin = 'ошибка №2'
    #     return render_template('login.html', errorLogin=errorLogin)
    # return render_template('account.html', full_name=records[0][1], username=records[0][2], password=records[0][3])


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')

            if len("".join(username.split())) == 0 or len("".join(password.split())) == 0:
                error = 'ошибка №1'
                return render_template('login.html', error=error)
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())

            if len(records) == 0:
                errorLogin = 'ошибка №2'
                return render_template('login.html', errorLogin=errorLogin)
            # cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            # records = list(cursor.fetchall())

            return render_template('account.html', full_name=records[0][1], username=records[0][2], password=records[0][3])
        elif request.form.get("registration"):
            return render_template("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(login),))
        records = list(cursor.fetchall())
        if len(records) > 0:
            errorLogin = 'ошибка №2'
            return render_template('registration.html', errorLogin=errorLogin)

        if len("".join(name.split())) == 0 or len("".join(password.split())) == 0:
            erRor = 'Заполните поля правильно'
            return render_template('login.html', error=erRor)
        if records[0][2] == login:
            print('error!!!')
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        return render_template('/login.html')

    return render_template('registration.html')

