from flask import Flask, render_template, url_for, request
import xlrd3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lnu8b5v5ervdfgbhjnij987867c56erdg'

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


@app.route('/polls')
def polls_page():
    return render_template('polls.html',
                           school_name=SCHOOL_NAME, attention=at, polls=polls)


@app.route('/poll/<name>', methods=['POST', 'GET'])
def poll_page(name):
    doc = [i['document'] for i in polls if i['name'] == name][0]
    questions = []
    try:
        with open(f'static/documents/{doc}', encoding='utf8') as f:
            data = f.readlines()
            for i in data:
                questions.append(i.strip())
        if len(questions) == 0:
            raise Exception('Файл пустой')
        if request.method == 'GET':
            return render_template('poll.html', school_name=SCHOOL_NAME, attention=at, quest=questions, name=name)
        elif request.method == 'POST':
            return render_template('conclusion.html', school_name=SCHOOL_NAME,
                                   attention=at, con='Спасибо за прохождение опроса!')
    except Exception as e:
        print(e)
        return render_template('conclusion.html', school_name=SCHOOL_NAME,
                               attention=at, con='Произошли технические неполадки')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
