from flask import Flask, render_template, redirect, url_for # type: ignore
from projects.project import project_loader
from classes.clazz import class_loader, clazz
from experiences.exp import experience_loader
from utils import *
import os

proj_loader = project_loader()
clazz_loader = class_loader()
exp_loader = experience_loader()

app = Flask(__name__)
app_last_commit_date = Utilities.get_last_commit_date(os.path.dirname(os.path.abspath(__file__)))
version = Utilities.get_project_version(os.path.dirname(os.path.abspath(__file__)))

@app.route("/")
@app.route('/<name>')
def index(name=None):
    """
    Main index page. 
    Any invalid page will also just render index page.
    """
    return render_template('about.html', version=version, last_update=app_last_commit_date, class_loader=clazz_loader, project_loader=proj_loader, exp_loader=exp_loader) 


@app.route('/experiences')
@app.route('/experiences.html')
def experiences():
    """
    Experience page for experience route.
    """
    return render_template('experiences.html', exp_loader=exp_loader, version=version, last_update=app_last_commit_date) 


@app.route('/experiences/<string:experience>')
@app.route('/experiences.html/<string:experience>')
def specific_experience(experience):
    """
    Specific experience page for the said experience route.
    """
    if exp_loader.hasExperience(experience):
        return render_template('experience.html', experience=exp_loader.getExperienceByName(experience), version=version, last_update=app_last_commit_date) 
    return "404 not found"


@app.route('/projects')
@app.route('/projects.html')
def projects():
    """
    Projects page for project route.
    """
    return render_template('projects.html', project_loader=proj_loader, version=version, last_update=app_last_commit_date) 


@app.route('/projects/<string:project>')
@app.route('/projects.html/<string:project>')
def specific_project(project):
    """
    Specific project page for the said project route.
    """
    if proj_loader.hasProject(project):
        return render_template('project.html', project=proj_loader.getProjectByName(project), version=version, last_update=app_last_commit_date) 
    return "404 not found"


@app.route('/classes/<string:clazz>/projects/<string:project>')
def specific_classproject(clazz, project):
    """
    Specific project page for the said class project route.
    """
    if clazz_loader.hasClass(clazz):
        if clazz_loader.hasProject(clazz, project):
            return render_template('project.html', project=clazz_loader.getClassProject(project), version=version, last_update=app_last_commit_date) 
        else:
            return "Project not found"
    else:
        return "Class not found"


@app.route('/courses')
@app.route('/courses.html')
def courses(name=None):
    """
    Courses page for courses route.
    """
    return render_template('courses.html', class_loader=clazz_loader, version=version, last_update=app_last_commit_date) 


@app.route('/resume')
def resume():
    """
    Resume route for my resume file.
    """
    return redirect(url_for('static', filename='resume.pdf'))  

@app.route('/test')
def test():
    """
    Test route for testing purposes.
    """
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)