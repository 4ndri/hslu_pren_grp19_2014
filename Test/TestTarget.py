__author__ = 'endru'

from DetectPicture import TargetCalculator

target_calc = TargetCalculator("../cascades/lbpcascades/lbpcascade_frontalface.xml")
target_calc.calculate_target()