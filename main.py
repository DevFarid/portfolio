from flask import *
from projects.project import project_loader
from classes.clazz import *
from utils import *
import os

project_loader = project_loader()
clazz_loader = class_loader()
app = Flask(__name__)
app_last_commit_date = Utilities.get_last_commit_date(os.path.dirname(os.path.abspath(__file__)))

@app.route("/")
@app.route('/<name>')
def index(name=None):
    return render_template('index.html', version=Utilities.get_project_version(os.path.dirname(os.path.abspath(__file__))), last_update=app_last_commit_date)

@app.route('/projects')
@app.route('/projects.html')
def projects():
    return render_template('projects.html', project_loader=project_loader)

@app.route('/projects/<string:project>')
@app.route('/projects.html/<string:project>')
def specific_project(project):
    if project_loader.hasProject(project):
        return render_template('project.html', project=project_loader.getProjectByName(project))
    return "404 not found"

@app.route('/classes/<string:clazz>/projects/<string:project>')
def specific_classproject(clazz, project):
    if clazz_loader.hasClass(clazz):
        if clazz_loader.hasProject(clazz, project):
            return render_template('project.html', project=clazz_loader.getClassProject(project))
        else:
            return "Project not found"
    else:
        return "Class not found"
    return "404 not found"

@app.route('/courses')
@app.route('/courses.html')
def courses(name=None):
    return render_template('courses.html', class_loader=clazz_loader)

@app.route('/resume')
def resume():
    return redirect(url_for('static', filename='resume.pdf'))

if __name__ == "__main__":
    app.run(debug=True)