from flask import Flask, redirect, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/test1/')
def test1():
    print("this is test 1")
    return render_template('first/one.html')

@app.route('/test2/')
def test2():
    return redirect('/test1/')

if __name__ == '__main__':
    app.run()
