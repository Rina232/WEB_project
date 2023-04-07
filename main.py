from flask import Flask, render_template
import xlrd3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

SCHOOL_NAME = 'МАОУ "Лицей 44"'

with open("static/documents/attention.txt", encoding='utf8') as f:
    data = f.readlines()
at = ''
for i in data:
    at += i.strip() + ' '

schedule = []
lst = []
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

with open("static/documents/polls.txt", encoding='utf8') as f:
    data = f.readlines()
polls = []
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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
