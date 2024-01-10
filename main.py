from flask import Flask, render_template, url_for
from projects import project
from classes import clazz

app = Flask(__name__)

@app.route("/")
@app.route('/<name>')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/projects')
@app.route('/projects.html')
def projects():
    x=project.project_loader()
    return render_template('projects.html', project_loader=x)

@app.route('/courses')
@app.route('/courses.html')
def courses(name=None):
    x=clazz.class_loader()
    return render_template('courses.html', class_loader=x)

@app.route('/about')
@app.route('/about.html')
def about(name=None):
    return render_template('about.html', name=name)

@app.route('/contacts')
@app.route('/contacts.html')
def contacts(name=None):
    return render_template('contacts.html', name=name)

if __name__ == "__main__":
    app.run(debug=True)