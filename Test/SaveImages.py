__author__ = 'endru'
import camera
import cv2
import cv2.cv as cv

path = '/home/pi/OpenCV/Development/precision_images/640_480_'
cam = camera.get_camera()
cam.set_resolution(640, 480)
i = 0
while True:
    img = cam.take_picture

    cv2.imshow('save with space', img)

    k = 0xFF & cv2.waitKey(5)
    if k == 32:
        print 'space'
        cv2.imwrite(path + 'pic{:>05}.jpg'.format(i), img)
        i += 1
    if k == 27:
        print 'escape'
        break
cam.close()
cv2.destroyAllWindows()
