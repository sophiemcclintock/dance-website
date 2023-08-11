from flask import Flask, render_template, request

app = Flask(__name__)

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
    return render_template("news.html")


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


@app.route('/login')
def login():
    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True)
