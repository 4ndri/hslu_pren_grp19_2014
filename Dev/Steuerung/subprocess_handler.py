__author__ = 'endru'
import subprocess
from random import randint

def get_image(dirPath):
    cmd="sudo python /home/pi/PREN/hslu_pren_grp19_2014/Dev/Steuerung/run_zf.py "+dirPath
    print "command: "+cmd
    subprocess.call(cmd, shell=True)
    return '<img src="/images/image.jpg?' + str(randint(1, 10000)) + '" />'

def ausrichtung_with_detect(dirPath):
    cmd="sudo python /home/pi/PREN/hslu_pren_grp19_2014/Dev/Steuerung/run_ausrichtung.py "+dirPath
    print "command: "+cmd
    subprocess.call(cmd, shell=True)
    return '<img src="/images/image.jpg?' + str(randint(1, 10000)) + '" />'

def start():
    cmd="sudo python /home/pi/PREN/hslu_pren_grp19_2014/Dev/Steuerung/run_steuerung.py"
    print "command: "+cmd
    subprocess.call(cmd, shell=True)
    return '<img src="/images/image.jpg?' + str(randint(1, 10000)) + '" />'

p=None
def init2():
    print "process init"
    global p

    p = subprocess.Popen("sudo python /home/endru/Dev/hslu_pren_grp19_2014/Dev/Steuerung/test_subproc.py", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    print "popened"

    print "end init"


def start2():
    global p
    if p is None:
        print "process none"
        return
    out,err = p.communicate(input="start")
    print "communicate"
    print out
    p.wait()

# init2()
# start2()