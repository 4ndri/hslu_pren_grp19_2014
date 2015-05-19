from Dev.Treiber.Zielerfassung.IZielerfassung import IZielerfassung

__author__ = 'Flavio Boss'


import Dev.Treiber.Zielerfassung.config as CFG
import Dev.Treiber.Zielerfassung.ContourFinder as CF
import Dev.Hardware.Camera.camera as camera
import cv2
import numpy as np
import math

class Zielerfassung(IZielerfassung):

    def __init__(self):
        self.config = CFG.ZFConfig()
        self.cam = camera.get_camera()


    def detect(self):

        #Bild einlesen (GrayScale)
        #self.input = cv2.imread('../../../precision_images/640_480_pic00012.jpg',cv2.CV_LOAD_IMAGE_GRAYSCALE)
        self.input = cv2.cvtColor(self.cam.take_picture, cv2.COLOR_RGB2GRAY);

        #Bildverarbeitungsbereich einschraenken (Y, X Coordinaten)
        self.searcharea = self.input[self.config.field_y:self.config.field_y+self.config.field_height, self.config.field_x:self.config.field_x+self.config.field_width]

        #Canny Kanten Erkennung
        self.canny = cv2.Canny(self.searcharea, self.config.threshold_min, self.config.threshold_max, apertureSize=3)

        #Hough Linien erkennung
        lines = cv2.HoughLines(self.canny,1,np.pi/180,self.config.hough_threshold)

        self.distance = self.searcharea.shape[1]

        #Linien Selektierung
        for rho,theta in lines[0]:
            #1. Linie ca. senkrecht
            if math.fabs(math.cos(theta - math.pi)) > 0.95:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))

                #2. Naechste Linie zum hitpoint
                dist = int(self.config.hitpoint_y*(-b)+x0)-self.config.hitpoint_x
                #print dist
                if abs(dist) < abs(self.distance):
                    self.distance = dist

                cv2.line(self.searcharea,(x1,y1),(x2,y2),(0,0,255),2)

        #print "Distanz:" +  str(distance)

        if self.distance < 0:
           self.distance -= self.config.approx_rect_w/2
        else:
            self.distance += self.config.approx_rect_w/2

        return np.arctan(self.distance)

    def get_image(self):
        self.detect()

        #Distanz anzeige
        cv2.line(self.searcharea,(int(self.config.hitpoint_x),int(self.config.hitpoint_y)),
                 (int(self.config.hitpoint_x+self.distance),int(self.config.hitpoint_y)),(255,255,255),2)

        #Zielfadenkreuz
        cv2.line(self.searcharea,(int(self.config.hitpoint_x-20),int(self.config.hitpoint_y)),
                 (int(self.config.hitpoint_x+20),int(self.config.hitpoint_y)),(0,0,255),1)
        cv2.line(self.searcharea,(int(self.config.hitpoint_x),int(self.config.hitpoint_y-20)),
                 (int(self.config.hitpoint_x),int(self.config.hitpoint_y+20)),(0,0,255),1)

        #Print HitRectangle
        cv2.rectangle(self.searcharea,
                (int(self.config.hitpoint_x+self.distance-self.config.approx_rect_w/2), int(self.config.hitpoint_y)),
                (int(self.config.hitpoint_x+self.distance+self.config.approx_rect_w/2), int(self.config.hitpoint_y+self.config.approx_rect_h)),
                (255,255,255),3)


        output = np.concatenate((self.input, self.canny), axis=0)

        return output

    def get_threshold(self):
        return self.config.threshold

    def set_threshold(self, threshold):
        self.config.set_threshold(threshold)

    def set_field(self):
        raise NotImplementedError()

    def save_config(self):
        self.config.save_config()


zf = Zielerfassung()
print "Angle: " + str(zf.detect())

cv2.imshow('image',zf.get_image())
cv2.waitKey(0)
cv2.destroyAllWindows()
