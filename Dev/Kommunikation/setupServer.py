__author__ = 'endru'
from flask import Flask
from flask import render_template
import Dev.Steuerung.steuerung as ctrl


app = Flask(__name__)
control = ctrl.Steuerung()


@app.route("/")
def index(name=None):
  return render_template('index.html', name=name)

@app.route("/get_position")
def get_position():

  return "Hello World!"


@app.route("/hello")
def hello():
  return "Hello World!"

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80, debug=True)