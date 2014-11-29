import numpy as np
import cv2
import matplotlib.pyplot as plt

testDir = "testFiles/"


img = cv2.imread(testDir+'exampleFinger.png')

def test_edges():
    edges = cv2.Canny(img,100,200)
    plt.imshow(edges,cmap= 'gray')
    plt.show()

def test_optFlowPyrLK():

    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))



    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()
    old_col = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame)
    hsv[...,1] = 255

    while(1):
        ret,frame = cap.read()
        frame_col = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(old_col,frame_col, 0.5, 3, 15, 3, 5, 1.2, 0)
        old_col = frame_col.copy()


        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

        cv2.imshow('flow',rgb)
        


    cap.release()

if __name__ == '__main__':
        test_optFlowPyrLK()
        







