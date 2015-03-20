__author__ = 'endru'
from flask import Flask
from flask import render_template
import Dev.Steuerung.steuerung as ctrl


app = Flask(__name__)
control = ctrl.Steuerung()
# control = None


@app.route("/")
def index(name=None):
    return render_template('index.html', name=name)


@app.route("/get_position")
def get_position():
    return "Hello World!"


@app.route("/init_control")
def init_control():
    control = ctrl.Steuerung()
    return render_template('index.html', name=None)


@app.route("/test_balldepot")
def test_balldepot():
    balls = control.get_balldepot.load
    print "number of Balls: " + str(balls)
    data = {'msg': balls}
    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)