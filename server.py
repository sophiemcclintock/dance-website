from flask import Flask, render_template, request, redirect, url_for
from db_functions import run_search_query_tuples
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
    return render_template("classes.html")


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


@app.route('/news_cud')
def news_cud():
    return render_template("news_cud.html")



if __name__ == "__main__":
    app.run(debug=True)