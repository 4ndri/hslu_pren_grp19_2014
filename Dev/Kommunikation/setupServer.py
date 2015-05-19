__author__ = 'endru'
from flask import Flask
from flask import render_template, request, redirect
import Dev.Steuerung.steuerung as ctrl
import cv2
import os
import subprocess
from random import randint


app = Flask(__name__, static_url_path='')
# control = ctrl.Steuerung()
control = None
running=False

@app.route("/")
def index(name=None):
    return render_template('index.html', name=name)


@app.route("/config")
def config():
    zfconfig = []
    noAttr = ["config", "dirPath", "file_name"]
    for attr, value in control.get_zielerfassung.config.__dict__.iteritems():
        if not any(attr in s for s in noAttr):
            zfconfig.append({'attr': attr, 'value': value})
    bdconfig = []
    for attr, value in control.get_balldepot.config.__dict__.iteritems():
        if not any(attr in s for s in noAttr):
            bdconfig.append({'attr': attr, 'value': value})
    bfconfig = []
    for attr, value in control.get_ballbefoerderung.config.__dict__.iteritems():
        if not any(attr in s for s in noAttr):
            bfconfig.append({'attr': attr, 'value': value})
    arconfig = []
    for attr, value in control.get_ausrichtung.config.__dict__.iteritems():
        if not any(attr in s for s in noAttr):
            arconfig.append({'attr': attr, 'value': value})
    configData = {'zfconfig': zfconfig,
                  'bdconfig': bdconfig,
                  'bfconfig': bfconfig,
                  'arconfig': arconfig}
    return render_template('config.html', configData=configData)

@app.route("/testing")
def testing():
    return render_template('testing.html')


@app.route("/start")
def start():
    control.start()
    str_data = "fertig schluss schuss"
    return str_data

@app.route("/reset")
def reset():
    control.reset()
    str_data="control reset"
    return str_data

# @app.route("/detect")
# def detect():
#     pos = control.get_zielerfassung.detect
#     return str(pos)

@app.route("/detect")
def detect():
    dirPath = os.path.dirname(os.path.abspath(__file__))
    cmd="sudo python /home/pi/PREN/hslu_pren_grp19_2014/Dev/Steuerung/run_steuerung.py "+dirPath
    print "command: "+cmd
    subprocess.call(cmd, shell=True)
    return '<img src="/images/image.jpg?' + str(randint(1, 10000)) + '" />'

@app.route("/images/img")
def return_img():
    return app.send_static_file('/images/image.jpg')


@app.route("/get_picture")
def get_picture():
    cnt_info = control.get_zielerfassung.get_image
    dirPath = os.path.dirname(os.path.abspath(__file__))
    print dirPath
    cv2.imwrite(dirPath + "/static/images/image.jpg", cnt_info.img)
    data = {'msg': "success"}
    return "success"


@app.route("/init_control")
def init_control():
    control.reset_all()
    data = {'msg': 'steuerung reset_all'}
    return render_template('index.html', data=data)


@app.route("/test_balldepot")
def test_balldepot():
    balls = control.get_balldepot.load
    print "number of Balls: " + str(balls)
    data = {'msg': balls}
    return str(data)

@app.route("/run_ballbefoerderung")
def run_ballbefoerderung():
    print "dc start running"
    control.get_ballbefoerderung.run()
    data = {'msg': 'dc running'}
    return str(data)

@app.route("/stop_ballbefoerderung")
def stop_ballbefoerderung():
    print "dc start running"
    control.get_ballbefoerderung.stop()
    data = {'msg': 'dc stop'}
    return str(data)

@app.route("/set_bfspeed", methods=['POST'])
def set_bfspeed():
    print "set ballbefoerderung speed"
    speed = get_int_from_request('speed')
    control.get_ballbefoerderung.set_speed(speed)
    data = {'msg': 'dc speed set'}
    return str(data)

@app.route("/test_ausrichtung")
def test_ausrichtung():
    print "test_ausrichtung"
    control.get_ausrichtung.moveXAngle(6.28)
    control.get_ausrichtung.moveXAngle(-6.28)
    data = {'msg': 'ausrichtung moveXAngle 6.28, -6.28 finished'}
    return str(data)

@app.route("/test_ausrichtung_detect")
def test_ausrichtung_with_detect():
    print "test_ausrichtung with detection"
    angle = control.get_zielerfassung.detect
    control.get_ausrichtung.moveXAngle(angle)
    data = {'msg': 'ausrichtung moveXAngle: '+str(angle)+' finished'}
    return str(data)

@app.route("/test_ausrichtung_steps", methods=['POST'])
def test_ausrichtung_steps():
    print "test_ausrichtung_steps"
    steps=get_int_from_request('steps')
    print "posted steps: "+str(steps)
    control.get_ausrichtung.move_steps(steps)
    control.get_ausrichtung.move_steps(-steps)
    data = {'msg': 'ausrichtung move steps: '+str(steps)+', '+str(-steps)+' finished'}
    return str(data)

@app.route("/save_config_zielerfassung", methods=['POST'])
def save_cam_config():
    zf = control.get_zielerfassung
    zf.config.approx_rect_h = get_int_from_request('approx_rect_h')
    zf.config.approx_rect_w = get_int_from_request('approx_rect_w')
    zf.config.field_x = get_int_from_request('field_x')
    zf.config.field_y = get_int_from_request('field_y')
    zf.config.field_height = get_int_from_request('field_height')
    zf.config.field_width = get_int_from_request('field_width')
    zf.config.resolution_h = get_int_from_request('resolution_h')
    zf.config.resolution_w = get_int_from_request('resolution_w')
    zf.config.threshold = get_int_from_request('threshold')
    zf.config.pixelToCMFactor = float(request.form['pixelToCMFactor'])
    zf.save_config()
    return config()

@app.route("/save_config_balldepot", methods=['POST'])
def save_config_balldepot():
    bd = control.get_balldepot
    bd.config.timeForBall = float(request.form['timeForBall'])
    bd.config.duty = float(request.form['duty'])
    bd.config.gpio_pin = get_int_from_request('gpio_pin')
    bd.save_config()
    return config()

@app.route("/save_bfconfig", methods=['POST'])
def save_bfconfig():
    bf = control.get_ballbefoerderung
    bf.config.pulse_length = float(request.form['pulse_length'])
    bf.config.freq = get_int_from_request('freq')
    bf.config.gpio_port = get_int_from_request('gpio_port')
    bf.save_config()
    return config()

@app.route("/save_arconfig", methods=['POST'])
def save_arconfig():
    ar = control.get_ausrichtung
    ar.config.angle2Step = float(request.form['angle2Step'])
    ar.config.pulse_pin = get_int_from_request('pulse_pin')
    ar.config.dir_pin = get_int_from_request('dir_pin')
    ar.config.enable_pin=get_int_from_request('enable_pin')
    ar.config.microsteps1_pin=get_int_from_request('microsteps1_pin')
    ar.config.microsteps2_pin=get_int_from_request('microsteps2_pin')
    ar.config.acc = get_int_from_request('acc')
    ar.config.max_delay = get_int_from_request('max_delay')
    ar.config.min_delay= get_int_from_request('min_delay')
    ar.config.max_steps= get_int_from_request('max_steps')
    ar.save_config()
    return config()

def get_int_from_request(name):
    return int(float(request.form[name]))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)