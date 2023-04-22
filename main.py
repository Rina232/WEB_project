from flask import Flask, render_template, request, redirect
from forms.login import LoginForm
from forms.user import RegisterForm
import xlrd3
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

with open('static/documents/information.txt', encoding='utf8') as f:
    data = f.readlines()

inf = {'school_name': data[0].strip(),
       'full_school_name': data[1].strip(),
       'address': data[2].strip(),
       'phone_number': data[3].strip(),
       'email': data[4].strip()}

lg = 0

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
    for i in range(0, 200):
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
    with open("static/documents/polls/polls.txt", encoding='utf8') as f:
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
                          'doc': i.strip()})
            k = -2
        k += 1
except Exception as e:
    print(e)

actual = []
try:
    with open("static/documents/actual/actual.txt", encoding='utf8') as f:
        data = f.readlines()
    k = 0
    name = ''
    doc = ''
    for i in data:
        if k == 0:
            name = i.strip()
        elif k == 1:
            doc = i.strip()
        elif k == 2:
            actual.append({'name': name,
                           'doc': doc,
                           'pic': i.strip()})
        elif k == 3:
            k = -1
        k += 1
except Exception as e:
    print(e)

news = []
try:
    with open("static/documents/news/news.txt", encoding='utf8') as f:
        data = f.readlines()
    k = 0
    name = ''
    date = ''
    pic = ''
    text = ''
    for i in data:
        if k == 0:
            name = i.strip()
        elif k == 1:
            date = i.strip()
        elif k == 2:
            text = i.strip()
        elif k == 3:
            pic = i.strip()
        elif k == 4:
            news.append({'name': name,
                         'date': date,
                         'text': text,
                         'pic': pic,
                         'doc': i.strip()})
        elif k == 5:
            k = -1
        k += 1
except Exception as e:
    print(e)


@login_manager.user_loader
def load_user(user_id):
    """Функция получения пользователя"""
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main_page():
    """Функция, отображающая главную страницу"""
    print('sdfg')
    return render_template('main.html', inf=inf, attention=at, actual=actual, news=news[:5])


@app.route('/schedule')
def schedule_page():
    """Функция, отображающая страницу с расписанием"""
    return render_template('schedule.html', inf=inf, attention=at, schdl=schedule)


@app.route('/polls')
def polls_page():
    """Функция, отображающая страницу с опросами"""
    return render_template('polls.html', inf=inf, attention=at, polls=polls)


@app.route('/poll/<name>', methods=['POST', 'GET'])
def poll_page(name):
    """Функция, отображающая страницу с одним опросом и записывающая его результаты"""
    doc = [i['doc'] for i in polls if i['name'] == name][0]
    questions = []
    keys = []
    try:
        with open(f'static/documents/polls/{doc}', encoding='utf8') as f:
            data = f.readlines()
            for i in data:
                questions.append(i.strip())
        if len(questions) == 0:
            raise Exception('Файл пустой')
        k = 0
        temp = []
        for i in questions:
            if k == 1 and i[:3] == 'кон':
                k = 0
                keys.append(temp)
                temp = []
            elif k == 1:
                temp.append(i)
            elif i[:6] == 'список':
                keys.append(i[7:])
            elif i[:6] == 'строка':
                keys.append(i[7:])
            elif i[:5] == 'текст':
                keys.append(i[6:])
            elif i[:5] == 'выбор':
                keys.append(i[6:])
            elif i[:10] == 'множ выбор':
                k = 1
                temp.append(i[11:])
        if request.method == 'GET':
            return render_template('poll.html', inf=inf, attention=at, quest=questions, name=name)
        elif request.method == 'POST':
            with open(f"static/documents/polls_answers/{doc[:-4]}_answers.txt", mode="a", encoding='utf8') as f:
                for i in keys:
                    if type(i) == list:
                        f.write(i[0] + '\n')
                        for j in i[1:]:
                            try:
                                f.write(request.form[j] + '\n')
                            except Exception as e:
                                pass
                    else:
                        f.write(i + '\n' + request.form[i] + '\n')
                f.write('\n')
            return render_template('conclusion_poll.html', inf=inf,
                                   attention=at, con='Спасибо за прохождение опроса!')
    except Exception as e:
        return render_template('conclusion_poll.html', inf=inf,
                               attention=at, con='Произошли технические неполадки')


@app.route('/actual/<name>')
def actual_page(name):
    """Функция, отображающая страницу с актуальной новостью"""
    doc = [i['doc'] for i in actual if i['name'] == name][0]
    try:
        with open(f'static/documents/actual/{doc}', encoding='utf8') as f:
            data = f.readlines()
        if data:
            return render_template('actual.html', inf=inf, attention=at, name=name, text=data)
        else:
            raise Exception
    except Exception as e:
        return render_template('conclusion_main.html', inf=inf, attention=at)


@app.route('/news')
def news_page():
    """Функция, отображающая страницу с одной новостью"""
    return render_template('news.html', inf=inf, attention=at, news=news)


@app.route('/news/<name>')
def news1_page(name):
    """Функция, отображающая страницу новостей и объявлений"""
    doc, date = [(i['doc'], i['date']) for i in news if i['name'] == name][0]
    try:
        with open(f'static/documents/news/{doc}', encoding='utf8') as f:
            data = f.readlines()
        if data:
            return render_template('news1.html', inf=inf, attention=at, name=name, date=date, text=data)
        else:
            raise Exception('Файл пустой')
    except Exception as e:
        return render_template('conclusion_news.html', inf=inf, attention=at)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Функция, отображающая страницу входа"""
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, inf=inf)
    return render_template('login.html', form=form, inf=inf)


@app.route('/register', methods=['GET', 'POST'])
def signup():
    """Функция, отображающая страницу регистрации и сохраняющая данные о пользователе"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", inf=inf)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", inf=inf)
        user = User(
            name=form.name.data,
            lastname=form.lastname.data,
            age=form.age.data,
            role=form.role.data,
            login=form.login.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)
        return redirect('/')
    return render_template('register.html', form=form, inf=inf)


@app.route('/home')
def home_page():
    """Функция, отображающая страницу личного кабинета"""
    return render_template('home.html', inf=inf, attention=at)


@app.route('/logout')
@login_required
def logout():
    """Функция для выхода из аккаунта"""
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/school.db")
    app.run(port=8080, host='127.0.0.1')
