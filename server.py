from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime

app = Flask(__name__)
app.secret_key = "heyhowyadoing"
db_path = 'data/dance_db.sqlite'


@app.template_filter()
def news_date(sqlite_dt):
    # create a date object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %y %I:%M %p")


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        f = request.form
        sql = """insert into contact(contact_name, email, message)
                                   values(?,?,?)"""
        values_tuple = (f['name'], f['email'], f['comment'])
        result = run_commit_query(sql, values_tuple, db_path)
        return render_template("index.html")
    elif request.method == "GET":
        temp_form_data = {
            "name": "James Harvey",
            "email": "jh@gmail.com",
            "comment": "I want to book a private lesson"
        }
        return render_template("index.html", **temp_form_data)
    else:
        # return the page with an error message
        message = "Unrecognised command coming from classes page"
        return render_template("error.html", message=message)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/classes')
def classes():
    # query for page
    sql = """select classes.classes_id, classes.classes_title, classes.content, classes.image, member.name
        from classes
        join member on classes.member_id= member.member_id;
        """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("classes.html", classes=result)


@app.route('/classes_cud', methods =['GET', 'POST'])
def classes_cud():
    # collect data from the web address
    data = request.args
    required_keys = ['id','task']
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create read update on news (key not present)"
            return render_template('error.html', message=message)
    # have an id and a task key
    if request.method == "GET":
        if data['task'] == 'delete':
            if data['task'] == 'delete':
                sql = """delete from classes where classes_id = ?"""
                values_tuple = (data['id'],)
                result = run_commit_query(sql, values_tuple, db_path)
                sql = """delete from registration where classes_id = ?"""
                values_tuple = (data['id'],)
                result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('classes'))
        elif data['task'] == 'update':
            sql = """ select classes_title, content from classes where classes_id=? """
            values_tuple = (data['id'])
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("classes_cud.html",
                                   **result,
                                   id=data['id'],
                                   task=data['task'])
        elif data['task'] == 'add':
            temp = {'classes_title':'Test Title', 'content':'Test Content'}
            return render_template("classes_cud.html", id=0, task=data['task'],
                                   **temp)
        else:
            message = "Unrecognised task coming from classes page"
            return render_template('error.html', message=message)
    elif request.method == "POST":
        # collected the information from the form
        f = request.form
        print(f)
        if data['task'] == 'add':
            # add the classes entry to the database
            # member is fixed for now
            sql = """insert into classes(classes_title, content, member_id, image)
                        values(?,?,?,?)"""
            values_tuple = (f['classes_title'], f['content'], session['member_id'], 'lucy_molly.jpg')
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('classes'))
        elif data['task'] == 'update':
            sql = """update classes set classes_title=?, content=? where classes_id=?"""
            values_tuple = (f['classes_title'], f['content'], data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # collect the data from the form and update the database at the sent id
            return redirect(url_for('classes'))
        else:
            message = "Unrecognised task coming from classes page"
            return render_template('error.html', message=message)
    else:
        # return the page with an error message
        message = "Unrecognised command coming from classes page"
        return render_template("error.html", message=message)


@app.route('/news')
def news():
    # query for page
    sql = """select news.news_id, news.title, news.subtitle, news.content, news.newsdate, member.name
    from news
    join member on news.member_id= member.member_id
    order by news.newsdate desc;
    """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("news.html", news=result)


@app.route('/news_cud', methods =['GET', 'POST'])
def news_cud():
    # collect data from the web address
    data = request.args
    required_keys = ['id','task']
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create read update on news (key not present)"
            return render_template('error.html', message=message)
    # have an id and a task key
    if request.method == "GET":
        if data['task'] == 'delete':
            sql = """delete from news where news_id = ?"""
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
        elif data['task'] == 'update':
            sql = """ select title,subtitle, content from news where news_id=? """
            values_tuple = (data['id'])
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("news_cud.html",
                                   **result,
                                   id=data['id'],
                                   task=data['task'])
        elif data['task'] == 'add':
            temp = {'title':'Test Title', 'subtitle':'Test Subtitle', 'content':'Test Content'}
            return render_template("news_cud.html", id=0, task=data['task'],
                                   **temp)
        else:
            message = "Unrecognised task coming from news page"
            return render_template('error.html', message=message)
    elif request.method == "POST":
        # collected the information from the form
        f = request.form
        print(f)
        if data['task'] == 'add':
            # add the news news entry to the database
            # member is fixed for now
            sql = """insert into news(title, subtitle, content, newsdate, member_id)
                        values(?,?,?, datetime('now', 'localtime'),?)"""
            # add some more validation around if the member_id is there or not
            values_tuple = (f['title'], f['subtitle'], f['content'], session['member_id'])
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
        elif data['task'] == 'update':
            sql = """update news set title=?, subtitle=?, content=?, newsdate=datetime('now', 'localtime') where news_id=?"""
            values_tuple = (f['title'], f['subtitle'], f['content'], data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # collect the data from the form and update the database at the sent id
            return redirect(url_for('news'))
        else:
            message = "Unrecognised task coming from news page"
            return render_template('error.html', message=message)
    else:
        # return the page with an error message
        message = "Unrecognised command coming from news page"
        return render_template("error.html", message=message)


@app.route('/enrol', methods=["GET", "POST"])
def enrol():
    if request.method == "POST":
        f = request.form
        print(f)
        session['new_member'] = f
        return render_template("confirm.html", form_data=f)
    elif request.method == "GET":
        temp_form_data={
            "firstname": "James",
            "lastname": "Harvey",
            "age": "14",
            "email": "jh@gmail.com",
            "birthday": "2006-09-05",
            "phonenumber": "+64 21 4565 8464",
            "comment": "No"
        }
        return render_template("enrol.html", **temp_form_data)
    else:
        # return the page with an error message
        message = "Unrecognised command coming from enrol page"
        return render_template("error.html", message=message)


@app.route('/members', methods=["GET"])
def members():
    data = request.args
    if request.method == "GET":
        if 'task' in data.keys():
            if data['task'] == 'delete':
                sql = """delete from classes where member_id = ?"""
                values_tuple = (data['member_id'],)
                result = run_commit_query(sql, values_tuple, db_path)
                sql = """delete from news where member_id = ?"""
                values_tuple = (data['member_id'],)
                result = run_commit_query(sql, values_tuple, db_path)
                sql = """delete from registration where member_id = ?"""
                values_tuple = (data['member_id'],)
                result = run_commit_query(sql, values_tuple, db_path)
                sql = """delete from member where member_id = ?"""
                values_tuple = (data['member_id'],)
                result = run_commit_query(sql, values_tuple, db_path)
            else:
                return render_template('error.html', message="Members task not understood")
        sql = """ select member_id, name, email, authorisation from member"""
        result = run_search_query_tuples(sql, (), db_path, True)
        return render_template("members.html", members=result)
    else:
        # return the page with an error message
        message = "Unrecognised command coming from news page"
        return render_template("error.html", message=message)


@app.route('/contact')
def contact():
    data = request.args
    sql = """select contact_name, email, message from contact"""
    result = run_search_query_tuples(sql, (), db_path, True)
    return render_template("contact.html", contact=result)


@app.route('/registration', methods=["GET","POST"])
def registration():
    data = request.args
    print(data.keys())
    if request.method == "GET":
        if 'task' in data.keys():
            if data['task'] == 'delete':
                sql = """delete from registration where member_id = ? and classes_id = ?"""
                values_tuple = (data['member_id'], data['classes_id'])
                result = run_commit_query(sql, values_tuple, db_path)
                print('delete')
                print(result)
            else:
                return render_template('error.html' , message="Registrations task not understood")
        sql = """select  m.member_id, m.name, m.email
         from member m
         join registration r on m.member_id = r.member_id
         where r.classes_id = ?
         order by m.name asc"""
        values_tuple = (data['classes_id'],)
        result = run_search_query_tuples(sql, values_tuple, db_path, True)
        sql = """select  m.member_id, m.name, m.email
         from member m
         order by m.name asc
         """
        memberset = run_search_query_tuples(sql, (), db_path, True)
        return render_template("registration.html", registration=result, memberset=memberset, classes_id=data['classes_id'])
    elif request.method == "POST":
        f = request.form
        if data['task'] == 'add':
            sql = """insert into registration(member_id, classes_id)
            values((select member_id from member where name = ?), ?)"""
            values_tuple = (f['student'], data['classes_id'])
            result = run_commit_query(sql, values_tuple, db_path)
            if result is False:
                message = "Failed to add, most likely the member is already registered"
                return render_template("error.html", message=message)
            return redirect(url_for('registration', classes_id=data['classes_id']))
        else:
            return render_template('error.html', message="Registrations task not understood")
    else:
        # return the page with an error message
        message = "Unrecognised command coming from news page"
        return render_template("error.html", message=message)


@app.route('/login', methods=["GET", "POST"])
def login():
    print(session)
    error = "Your crewentials are not recognised"
    if request.method == "GET":
        return render_template("login.html", email='sophiecatemcclintock@gmail.com', password="temp")
    elif request.method == "POST":
        f = request.form
        sql = """ select member_id, name, password, authorisation from member where email = ? """
        values_tuple = (f['email'],)
        result = run_search_query_tuples(sql, values_tuple, db_path, True)
        if result:
            # collect the result
            result = result[0]
            # check if the password is equal to what is in the database
            if result['password'] == f['password']:
                # start the session
                session['name'] = result['name']
                session['authorisation'] = result['authorisation']
                session['member_id'] = result['member_id']
                print(session)
                # return to the main page
                return redirect(url_for('index'))
            else:
                # return the page with an error message
                return render_template("login.html", email='sophiecatemcclintock@gmail.com', password="temp", error=error)

        else:
            # return the page with an error message
            return render_template("login.html", email='sophiecatemcclintock@gmail.com', password="temp", error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/confirm', methods=["GET", "POST"])
def confirm():
    if request.method == "GET":
        return render_template("confirm.html")
    elif request.method == "POST":
        f = session['new_member']
        name = f['firstname'] + " " + f['lastname']
        sql = """insert into member(name, email, password, authorisation)
            values(?, ?, ?, ?) """
        values_tuple = (name, f['email'], 'temp', '1')
        print(values_tuple)
        result = run_commit_query(sql, values_tuple, db_path)
        session['new_member'].clear()
        return redirect(url_for('index'))
    else:
        # return the page with an error message
        message = "Unrecognised command coming from enrol page"
        return render_template("error.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)