from flask import Flask, render_template

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


@app.route('/enrol')
def enrol():
    return render_template("enrol.html")


if __name__ == "__main__":
    app.run(debug=True)