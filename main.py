from flask import Flask, render_template, redirect, url_for, send_from_directory # type: ignore
from flask_talisman import Talisman # type: ignore
from flask_wtf.csrf import CSRFProtect # type: ignore
from projects.project import project_loader
from classes.clazz import class_loader, clazz
from experiences.exp import experience_loader
from learnings.learner import learning_loader
from education.edu import education_loader
from utils import *
import os
import re

proj_loader = project_loader()
clazz_loader = class_loader()
exp_loader = experience_loader()
learn_loader = learning_loader()
edu_loader = education_loader()

app = Flask(__name__)
# Configure security headers with Flask-Talisman
Talisman(app, content_security_policy={
    'default-src': "'self'",
    'script-src': "'self'",
    'style-src': "'self' 'unsafe-inline'",
    'img-src': "'self' data: https:",
    'font-src': "'self' data:",
    'connect-src': "'self'",
    'media-src': "'self'",
    'frame-src': "'self'",
    'object-src': "'none'",
    'base-uri': "'self'",
    'form-action': "'self'",
    'frame-ancestors': "'none'",
    'sandbox': 'allow-same-origin allow-scripts allow-forms allow-popups'
})
csrf = CSRFProtect(app)

app_last_commit_date = Utilities.get_last_commit_date(os.path.dirname(os.path.abspath(__file__)))
version = Utilities.get_project_version(os.path.dirname(os.path.abspath(__file__)))

@app.route("/")
@app.route('/<name>')
def index(name=None):
    """
    Main index page. 
    Any invalid page will also just render index page.
    """
    return render_template('about.html', version=version, last_update=app_last_commit_date, class_loader=clazz_loader, project_loader=proj_loader, exp_loader=exp_loader, edu_loader=edu_loader) 

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_message="Internal server error"), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_message="Internal server error"), 500

# ------------------------------------------------ Courses ---------------------------------------------------------------

@app.route('/courses')
@app.route('/courses.html')
def courses(name=None):
    """
    Courses page for courses route.
    """
    return render_template('courses.html', class_loader=clazz_loader, version=version, last_update=app_last_commit_date) 

@app.route('/classes/<string:clazz>/projects/<string:project>')
def specific_classproject(clazz, project):
    """
    Specific project page for the said class project route.
    """
    # Basic validation to prevent path traversal
    if '..' in clazz or '..' in project or '/' in clazz or '/' in project or '\\' in clazz or '\\' in project:
        return render_template('error.html', error_message="Invalid class or project name"), 400
    
    if clazz_loader.hasClass(clazz):
        if clazz_loader.hasProject(clazz, project):
            return render_template('project.html', project=clazz_loader.getClassProject(project), version=version, last_update=app_last_commit_date) 
        else:
            return render_template('error.html', error_message="Project not found"), 404
    else:
        return render_template('error.html', error_message="Class not found"), 404

# ------------------------------------------------ Projects ---------------------------------------------------------------

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
    # Basic validation to prevent path traversal
    if '..' in project or '/' in project or '\\' in project:
        return render_template('error.html', error_message="Invalid project name"), 400
    
    if proj_loader.hasProject(project):
        return render_template('project.html', project=proj_loader.getProjectByName(project), version=version, last_update=app_last_commit_date) 
    return render_template('error.html', error_message="Project not found"), 404

# ------------------------------------------------ Learnings ---------------------------------------------------------------

@app.route('/learnings')
@app.route('/learnings.html')
def learnings():
    """
    Test route for testing purposes.
    """
    return render_template('learnings.html', version=version, last_update=app_last_commit_date, learn_loader=learn_loader)

@app.route('/learnings/<string:learn>')
@app.route('/learnings.html/<string:learn>')
def specific_learning(learn):
    """
    Specific learning page for the said learning route.
    """
    # Basic validation to prevent path traversal
    if '..' in learn or '/' in learn or '\\' in learn:
        return render_template('error.html', error_message="Invalid learning name"), 400
    
    if learn_loader.hasLearning(learn):
        return render_template('learning.html', learning=learn_loader.getLearningByName(learn), version=version, last_update=app_last_commit_date) 
    return render_template('error.html', error_message="Learning not found"), 404
# ------------------------------------------------ Experiences ---------------------------------------------------------------

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
    # Basic validation to prevent path traversal
    if '..' in experience or '/' in experience or '\\' in experience:
        return render_template('error.html', error_message="Invalid experience name"), 400
    
    if exp_loader.hasExperience(experience):
        return render_template('experience.html', experience=exp_loader.getExperienceByName(experience), version=version, last_update=app_last_commit_date)
    return render_template('error.html', error_message="Experience not found"), 404

# ------------------------------------------------ Education ---------------------------------------------------------------

@app.route('/education')
@app.route('/education.html')
def education_page():
    """
    Education page for education route.
    """
    return render_template('education.html', edu_loader=edu_loader, version=version, last_update=app_last_commit_date) 


@app.route('/education/<string:education>')
@app.route('/education.html/<string:education>')
def specific_education(education):
    """
    Specific education page for the said education route.
    """
    # Basic validation to prevent path traversal
    if '..' in education or '/' in education or '\\' in education:
        return render_template('error.html', error_message="Invalid education name"), 400
    
    if edu_loader.hasEducation(education):
        return render_template('education_detail.html', education=edu_loader.getEducationByName(education), version=version, last_update=app_last_commit_date) 
    return render_template('error.html', error_message="Education not found"), 404

# --------------------------------------------- Static Files & Routes ---------------------------------------------------------
@app.route('/resume')
def resume():
    """
    Resume route for my resume file.
    """
    return redirect(url_for('static', filename='resume.pdf'))  

if __name__ == "__main__":
    app.run(debug=True)