#!/usr/bin/env python
__author__ = 'endru'
from flask import Flask
from flask import render_template, request, redirect
import Dev.Steuerung.steuerung as ctrl
import cv2
import os
import subprocess

app = Flask(__name__, static_url_path='')
control = ctrl.Steuerung()
# control = None
running = False


@app.route("/")
def index(name=None):
    global control
    # control=None
    return render_template('index.html', name=name)


@app.route("/config")
def config():
    global control
    # control=None
    # control = ctrl.Steuerung()
    zfconfig = []
    noAttr = ["config", "dirPath", "file_name"]
    for attr, value in control.get_zielerfassung.config.__dict__.iteritems():
        if not any(attr in s for s in noAttr):
            zfconfig.append({'attr': attr, 'value': value})
    zfconfig = sorted(zfconfig)

    bdconfig = []
    for attr, value in control.get_balldepot.config.__dict__.iteritems():
        if not any(attr in s for s in noAttr):
            bdconfig.append({'attr': attr, 'value': value})
    bdconfig = sorted(bdconfig)

    bfconfig = []
    for attr, value in control.get_ballbefoerderung.config.__dict__.iteritems():
        if not any(attr in s for s in noAttr):
            bfconfig.append({'attr': attr, 'value': value})
    bfconfig = sorted(bfconfig)

    arconfig = []
    for attr, value in control.get_ausrichtung.config.__dict__.iteritems():
        if not any(attr in s for s in noAttr):
            arconfig.append({'attr': attr, 'value': value})
    arconfig = sorted(arconfig)

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

@app.route("/start_camera")
def start_camera():
    control.zielerfassung.stop_subproc()
    control.zielerfassung.start_subproc()
    str_data = "camera started"
    return str_data

@app.route("/stop_camera")
def stop_camera():
    control.zielerfassung.stop_subproc()
    str_data = "camera stopped"
    return str_data

@app.route("/reset")
def reset():
    if control is None:
        return "no control"
    control.reset()
    str_data = "control reset"
    return str_data




@app.route("/detect")
def detect():
    angle = control.get_zielerfassung.detect()
    return str(angle)

@app.route("/shut_down")
def shut_down():
    cmd="sudo killall python && sudo shutdown -h now"
    subprocess.Popen(cmd, shell=True)
    return "killall"

@app.route("/images/img")
def return_img():
    return app.send_static_file('/images/image.jpg')


@app.route("/get_picture")
def get_picture():
    cnt_info = control.get_zielerfassung.get_image()
    # dirPath = os.path.dirname(os.path.abspath(__file__))
    # print dirPath
    # cv2.imwrite(dirPath + "/static/images/image.jpg", cnt_info.img)

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
    angle = control.get_zielerfassung.detect()
    control.get_ausrichtung.moveXAngle(angle)
    data = {'msg': 'ausrichtung moveXAngle: ' + str(angle) + ' finished'}
    return str(data)


@app.route("/test_ausrichtung_steps", methods=['POST'])
def test_ausrichtung_steps():
    print "test_ausrichtung_steps"
    steps = get_int_from_request('steps')
    print "posted steps: " + str(steps)
    control.get_ausrichtung.move_steps(steps)
    control.get_ausrichtung.move_steps(-steps)
    data = {'msg': 'ausrichtung move steps: ' + str(steps) + ', ' + str(-steps) + ' finished'}
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
    zf.config.hitpoint_x=get_int_from_request('hitpoint_x')
    zf.config.hitpoint_y=get_int_from_request('hitpoint_y')
    zf.save_config()
    return config()


@app.route("/save_config_balldepot", methods=['POST'])
def save_config_balldepot():
    bd = control.get_balldepot
    bd.config.timeForBall = float(request.form['timeForBall'])
    bd.config.waitTime1 = float(request.form['waitTime1'])
    bd.config.waitTimeOther = float(request.form['waitTimeOther'])
    bd.config.duty = float(request.form['duty'])
    bd.config.gpio_pin = get_int_from_request('gpio_pin')
    bd.save_config()
    return config()


@app.route("/save_bfconfig", methods=['POST'])
def save_bfconfig():
    bf = control.get_ballbefoerderung
    bf.config.pulse_length = float(request.form['pulse_length'])
    bf.config.pulse_length_max = float(request.form['pulse_length_max'])
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
    ar.config.enable_pin = get_int_from_request('enable_pin')
    ar.config.microsteps1_pin = get_int_from_request('microsteps1_pin')
    ar.config.microsteps2_pin = get_int_from_request('microsteps2_pin')
    ar.config.acc = get_int_from_request('acc')
    ar.config.max_delay = get_int_from_request('max_delay')
    ar.config.min_delay = get_int_from_request('min_delay')
    ar.config.max_steps = get_int_from_request('max_steps')
    ar.save_config()
    return config()


def get_int_from_request(name):
    return int(float(request.form[name]))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
