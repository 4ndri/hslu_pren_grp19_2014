__author__ = 'endru'
import Dev.Treiber.Zielerfassung.zielerfassung as ZF
import os
import cv2
import sys
import time

work_path ="/home/pi/PREN/hslu_pren_grp19_2014/Dev/Kommunikation/static/images"
if len(sys.argv) > 1:
    img_path = sys.argv[1]

detector = ZF.Zielerfassung()

while True:
    detector.dir = 0
    cnt_info = detector.get_image()
    cv2.imwrite(work_path+"/image.jpg", cnt_info.img)
    with open(work_path+"/detect.txt", 'w') as detect_file:
        detect_file.write(str(cnt_info.center_distance.x))
        detect_file.close()
    time.sleep(1)
    #print "detect: " + str(cnt_info.center_distance.x)
print "done"
