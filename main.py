from flask import Flask, render_template, url_for
from projects.project import project_loader
from classes.clazz import *
from utils import *
import os

project_loader = project_loader()
clazz_loader = class_loader()
app = Flask(__name__)

@app.route("/")
@app.route('/<name>')
def index(name=None):
    return render_template('index.html', version=Utilities.get_project_version(os.path.dirname(os.path.abspath(__file__))))

@app.route('/projects')
@app.route('/projects.html')
def projects():
    return render_template('projects.html', project_loader=project_loader)

@app.route('/projects/<string:project>')
@app.route('/projects.html/<string:project>')
def specific_project(project):
    if project_loader.hasProject(project):
        return "yes it was found"
    return "nope"

@app.route('/classes/<string:clazz>/projects/<string:project>')
def specific_classproject(clazz, project):
    if clazz_loader.hasProject(project):
        return "yes it was found"
    return "nope"

@app.route('/courses')
@app.route('/courses.html')
def courses(name=None):
    return render_template('courses.html', class_loader=clazz_loader)

if __name__ == "__main__":
    app.run(debug=True)