from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

SCHOOL_NAME = 'МАОУ "Лицей 44"'


@app.route('/')
def main_page():
    with open("static/documents/attention.txt", encoding='utf8') as f:
        data = f.readlines()
    at = ''
    for i in data:
        at += i.strip() + ' '
    return render_template('main_page.html',
                           school_name=SCHOOL_NAME, attention=at)


@app.route('/chess')
def chess_page():
    with open("static/documents/attention.txt", encoding='utf8') as f:
        data = f.readlines()
    at = ''
    for i in data:
        at += i.strip() + ' '
    return render_template('chess_page.html',
                           school_name=SCHOOL_NAME, attention=at)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
