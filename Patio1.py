from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
#from matplotlib import pyplot as plt
import numpy as np
import serial

camera = PiCamera()
camera.resolution = (640, 368)
rawCapture = PiRGBArray(camera, size=(640, 368))

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
#while(True):
    
#    ret, img = cap.read()
    
    #img = cv.flip(img, -1) # Flip camera vertically
    height, width = img.shape[:2]
    #size = (int(width*0.5), int(height*0.5))  
    #shrink = cv.resize(img, size, interpolation=cv.INTER_AREA) 
    blurred = cv.GaussianBlur(img, (3, 3), 1)
    blurred = cv.GaussianBlur(img, (3, 3), 1)
    gray = cv.cvtColor(blurred, cv.COLOR_RGB2GRAY)
    #xgrad = cv.Sobel(gray, cv.CV_16SC1, 1, 0) #x方向梯度
    #ygrad = cv.Sobel(gray, cv.CV_16SC1, 0, 1) #y方向梯度
    #edge_output = cv.Canny(xgrad, ygrad, 125, 250)
    canny = cv.Canny(gray, 120, 230)    
    #cropped = canny[0:height, int(width*0.2):int(width*0.8)]  # 裁剪坐标为[y0:y1, x0:x1]
    arr = np. zeros(int(width))
    i = 0
    while i < int(width):
        arr[i] = canny[:,i].sum()
        i += 1
    average_arr = np.mean(arr)
    print('the average value is',average_arr)
    x = np.zeros(int(width))
    j = 0
    while j < int(width):
        x[j] = j
        j += 1
    arr_valid = np.where(arr<=1.35*average_arr,0,1)
    x_sum = np.sum(arr_valid*x)
    x_num = np.sum(arr_valid)
    
    x_coor1 = x_sum/(x_num+1)
    x_coor = x_coor1.astype(np.int)
    print('the x coordinate is ',x_coor)
    error = int(width*0.5)-x_coor
    print('the error is',error)
    ERR = str(error)
    ser.write(ERR.encode())
    cv.line(img, (int(width*0.5),0 ), (int(width*0.5),height ), (255,0,0),5)
    cv.line(img, ((x_coor),0 ), ((x_coor),height ), (0,0,255),5)
    cv.imshow('frame',canny)
    cv.imshow('camera',img)  
    rawCapture.truncate(0)  
    key = cv.waitKey(1) & 0xFF 
    if key == ord("q"):
        break