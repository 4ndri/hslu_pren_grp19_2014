__author__ = 'endru'

from Dev.Test.DetectPicturePi import TargetCalculator
import numpy as np
import cv2
import cv2.cv as cv

target_calc = TargetCalculator("../cascades/lbpcascades/lbpcascade_frontalface.xml", True)
try:
    # pos = target_calc.showImage
    # print(pos)
    target_calc.play_video2()

    while True:
        if 0xFF & cv2.waitKey(5) == 27:
            break

finally:
    target_calc.close()
    cv2.destroyAllWindows()


