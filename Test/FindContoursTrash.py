__author__ = 'endru'
import camera
import cv2
import cv2.cv as cv

cam = camera.get_camera()
i = 0
while True:
    img = cam.take_picture
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0,255,0), 3)
    cv2.imshow('asdf', img)

    k = 0xFF & cv2.waitKey(5)
    if k == 27:
        print 'escape'
        break
cam.close()
cv2.destroyAllWindows()

