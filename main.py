from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
@app.route('/<name>')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/projects')
def projects():
    return render_template('projects.html', name=name)

@app.route('/about')
def about():
    return render_template('about.html', name=name)
    
@app.route('/contacts')
def contacts():
    return render_template('contacts.html', name=name)

if __name__ == "__main__":
    app.run(debug=True)