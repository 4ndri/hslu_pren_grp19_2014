__author__ = 'endru'

from DetectPicture import TargetCalculator
import numpy as np
import cv2
import cv2.cv as cv

target_calc = TargetCalculator("../cascades/lbpcascades/lbpcascade_frontalface.xml", 0)
pos = target_calc.calculate_target
print(pos)
while True:
    if 0xFF & cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()
target_calc.cam.release()

