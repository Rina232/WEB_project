from flask import Flask, render_template, url_for, request
import xlrd3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

SCHOOL_NAME = 'МАОУ "Лицей 44"'

at = ''
try:
    with open("static/documents/attention.txt", encoding='utf8') as f:
        data = f.readlines()
    for i in data:
        at += i.strip() + ' '
except Exception as e:
    print(e)

schedule = []
try:
    workbook = xlrd3.open_workbook("static/documents/schedule.xlsx")
    worksheet = workbook.sheet_by_index(0)
    for i in range(0, 230):
        lst = []
        for j in range(0, 11):
            if type(worksheet.cell_value(i, j)) is float:
                lst.append(int(worksheet.cell_value(i, j)))
            else:
                lst.append(worksheet.cell_value(i, j))
        schedule.append(lst)
except Exception as e:
    print(e)

polls = []
try:
    with open("static/documents/polls.txt", encoding='utf8') as f:
        data = f.readlines()
    k = 0
    date = ''
    name = ''
    description = ''
    for i in data:
        if k == 0:
            date = i.strip()
        elif k == 1:
            name = i.strip()
        elif k == 2:
            description = i.strip()
        elif k == 3:
            polls.append({'date': date,
                          'name': name,
                          'description': description,
                          'document': i.strip()})
            k = -2
        k += 1
except Exception as e:
    print(e)


@app.route('/')
def main_page():
    return render_template('main.html',
                           school_name=SCHOOL_NAME, attention=at)


@app.route('/chess')
def chess_page():
    return render_template('chess.html',
                           school_name=SCHOOL_NAME, attention=at)


@app.route('/schedule')
def schedule_page():
    return render_template('schedule.html',
                           school_name=SCHOOL_NAME, attention=at, schdl=schedule)


@app.route('/poll')
def poll_page():
    return render_template('poll.html',
                           school_name=SCHOOL_NAME, attention=at, polls=polls)


@app.route('/polls/<name>', methods=['POST', 'GET'])
def poll_pages(name):
    doc = [i['document'] for i in polls if i['name'] == name][0]
    try:
        with open(doc, encoding='utf8') as f:
            data = f.readlines()
        if request.method == 'GET':
            return f'''<!doctype html>
                        <html lang="en" xmlns="http://www.w3.org/1999/html">
                        <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/
                                            css/bootstrap.min.css"
                                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjK
                                            Hr8RbDVddVHyTfAAsrekwKmP1"
                                            crossorigin="anonymous">
                            <title>{SCHOOL_NAME}</title>
                            <link rel="stylesheet"
                                  href="{url_for('static', filename='css/style.css')}" type="text/css">
                            <link rel="shortcut icon" href="static/img/logo.jpg" type="image/jpg">
                        
                        </head>
                        <body>
                            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha38
                            4-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossori
                            gin="anonymous"></script>
                            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/poppe
                            r.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakF
                            PskvXusvfa0b4Q" crossorigin="anonymous"></script>
                            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
                             integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76P
                             VCmYl" crossorigin="anonymous"></script>
                            <img src="/static/img/school.jpg" alt="Здесь должна быть картинка, но она не нашлась.">
                            <div class="bottomleft">
                                    <span style="padding: 0.5vw;">{SCHOOL_NAME}</span>
                            </div>
                            <marquee behavior="scroll" direction="left">{at}</marquee>
                            <p style="margin-top: 4vw; margin-left: 7vw;"><a href="/">Главная</a>
                            <a href="/poll"> / Опросы</a><a> / {name}</a></p>
                            <section>
                                <nav>
                                    <form action="/">
                                        <button>Новости и объявления</button>
                                    </form>
                                    <form action="/">
                                        <button>Информация</button>
                                    </form>
                                    <form action="/schedule">
                                        <button>Расписание</button>
                                    </form>
                                    <form action="/chess">
                                        <button>Шахматы</button>
                                    </form>
                                    <form action="/poll">
                                        <button>Опросы</button>
                                    </form>
                                </nav>
                                <article>
                                </article>
                            </section>
                            <footer>
                                <h2 style="margin-top: 2vw; margin-left: 2vw; margin-bottom: 1.5vw;">КОНТАКТЫ</h2>
                                <h3 style="margin-left: 2vw; margin-bottom: 1.5vw;"><b>МАОУ «ЛИЦЕЙ 44»
                                 Г. ЛИПЕЦКА</b></h3>
                                <p style="margin-left: 2vw; ">398050, Россия, Липецкая обл., г. Липецк, ул.
                                 Плеханова, д. 51А, 49 <br> +7 (4742) 28-02-02 (приёмная), 27-04-63 <br>
                                  sc44lip@schools48.ru</p>
                            </footer>
                        </body>
                        </html>'''
        if request.method == 'POST':
            pass
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
