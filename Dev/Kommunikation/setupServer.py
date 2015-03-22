__author__ = 'endru'
from flask import Flask
from flask import render_template
import Dev.Steuerung.steuerung as ctrl
import cv2
import os

app = Flask(__name__,static_url_path='')
control = ctrl.Steuerung()
# control = None


@app.route("/")
def index(name=None):
    return render_template('index.html', name=name)


@app.route("/detect")
def detect():
    pos = control.get_zielerfassung.detect
    data = {'msg': pos}
    return render_template('index.html', data=data)

@app.route("/images/img")
def return_img():
    return app.send_static_file('image.jpg')

@app.route("/get_picture")
def get_picture():
    cnt_info = control.get_zielerfassung.get_image
    dirPath = os.path.dirname(os.path.abspath(__file__))
    cv2.imwrite(dirPath + "/static/images/image.jpg", cnt_info.img)
    data = {'msg': "success"}
    return render_template('showpicture.html', data=data)

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