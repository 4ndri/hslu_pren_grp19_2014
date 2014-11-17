__author__ = 'endru'
import camera
import cv2
import cv2.cv as cv

path = '/home/endru/Documents/OpenCV/CascadeClassifiers/TrashCan/negative_images/nocan'
cam = camera.get_camera()
i = 0
while True:
    img = cam.take_picture()

    cv2.imshow('facedetect', img)

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
