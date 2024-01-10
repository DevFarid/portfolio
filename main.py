from flask import Flask, render_template, url_for
from projects.project import project_loader
from classes.clazz import *
from utils import *
import os

app = Flask(__name__)

@app.route("/")
@app.route('/<name>')
def index(name=None):
    return render_template('index.html', version=Utilities.get_project_version(os.path.dirname(os.path.abspath(__file__))))

@app.route('/projects')
@app.route('/projects.html')
def projects():
    return render_template('projects.html', project_loader=project_loader())

@app.route('/courses')
@app.route('/courses.html')
def courses(name=None):
    return render_template('courses.html', class_loader=class_loader())

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