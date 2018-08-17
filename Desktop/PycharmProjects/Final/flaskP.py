from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Ahoj světe..!'


@app.route('/cs')
def cs():
    return 'cs'


if __name__ == "__main__":
    app.run()
