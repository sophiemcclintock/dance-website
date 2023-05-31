from flask import Flask, render_template, request, redirect, url_for
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime

app = Flask(__name__)
db_path = 'data/dance_db.sqlite'


@app.template_filter()
def news_date(sqlite_dt):
    # create a date object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %y %I:%M %p")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/classes')
def classes():
    # query for page
    sql = """select classes.classes_id, classes.title, classes.content, classes.image, member.name
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
            sql = "delete from classes where classes_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('classes'))
        elif data['task'] == 'update':
            sql = """ select title, content from classes where classes_id=? """
            values_tuple = (data['id'])
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("classes_cud.html",
                                   **result,
                                   id=data['id'],
                                   task=data['task'])
        elif data['task'] == 'add':
            temp = {'title':'Test Title', 'content':'Test Content'}
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
            sql = """insert into classes(title, content, member_id, image)
                        values(?,?,2,?)"""
            values_tuple = (f['title'], f['content'], 'lucy_molly.jpg')
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('classes'))
        elif data['task'] == 'update':
            sql = """update classes set title=?, content=? where classes_id=?"""
            values_tuple = (f['title'], f['content'], data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # collect the data from the form and update the database at the sent id
            return redirect(url_for('classes'))
        else:
            message = "Unrecognised task coming from classes page"
            return render_template('error.html', message=message)
    return render_template("classes_cud.html")


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


@app.route('/enrol', methods=["GET", "POST"])
def enrol():
    if request.method == "POST":
        f = request.form
        print(f)
        return render_template("confirm.html", form_data=f)

    elif request.method == "GET":
        temp_form_data={
            "firstname" : "James",
            "secondname" : "Harvey",
            "age" : "14",
            "email" : "jh@gmail.com",
            "typeofdance" : "I am interested in jazz and contemporary"
        }
        return render_template("enrol.html", **temp_form_data)


@app.route('/log_in')
def log_in():
    return render_template("log_in.html")


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
            sql = "delete from news where news_id = ?"
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
                        values(?,?,?, datetime('now', 'localtime'),2)"""
            values_tuple = (f['title'], f['subtitle'], f['content'])
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
        elif data['task'] == 'update':
            sql = """update news set title=?, subtitle=?, content=?, newsdate=datetime('now', 'localtime') where news_id=?"""
            values_tuple = (f['title'], f['subtitle'], f['content'], data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # collect the data from the form and update the database at the sent id
            return redirect(url_for('news'))
    return render_template("news_cud.html")



if __name__ == "__main__":
    app.run(debug=True)