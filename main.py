from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
@app.route('/<name>')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/projects')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
    
@app.route('/contacts')
def contacts():
    return 'The contact page'

if __name__ == "__main__":
    app.run(debug=True)