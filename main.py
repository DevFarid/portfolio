from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello World</p>"

@app.route('/projects')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
    
@app.route('/contacts')
def contacts():
    return 'The contact page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == "__main__":
    app.run(debug=True)