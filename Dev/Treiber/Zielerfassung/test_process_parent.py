__author__ = 'endru'
import subprocess
import time
import collections
import threading
import os
def read_output(process, append):
    for line in iter(process.stdout.readline, ""):
        if line.startswith("detect: "):
            str_pos=line.replace("detect: ","")
            append(str_pos)
    print "t done"
dir_path = os.path.dirname(os.path.abspath(__file__))
print dir_path
proc = subprocess.Popen(['python','test_process_child.py'],stdout=subprocess.PIPE)
try:
    time.sleep(5)
    number_of_lines = 1
    q = collections.deque(maxlen=number_of_lines)
    t = threading.Thread(target=read_output, args=(proc, q.append))
    t.daemon = True
    t.start()


    # print saved lines
    for i in range(0,5):
        time.sleep(1)
        print len(q)
        pos=int(float("".join(q)))

        print pos

    proc.kill()

    proc = subprocess.Popen(['python','test_process_child.py'],stdout=subprocess.PIPE)
    number_of_lines = 1
    q = collections.deque(maxlen=number_of_lines)
    t = threading.Thread(target=read_output, args=(proc, q.append))
    t.daemon = True
    t.start()
    time.sleep(5)

    # print saved lines
    for i in range(0,5):
        time.sleep(1)
        pos=int(float("".join(q)))

        print pos
finally:
    proc.kill()
    print "proc killed"