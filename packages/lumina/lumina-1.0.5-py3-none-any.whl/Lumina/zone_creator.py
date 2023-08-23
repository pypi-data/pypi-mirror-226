import cv2
import numpy as np
from Lumina.lumina import Lumina
from typing import NewType , Union
import os
from datetime import datetime

video = NewType('video',str)
image = NewType('image',str)

lumina = Lumina()
poly_points = []

def mouseCall(event,x,y,flag,param):
    global poly_points 

    if event == cv2.EVENT_LBUTTONDOWN:
        poly_points.append([x,y])
     
        
    if event == cv2.EVENT_RBUTTONDOWN:
        
        if len(poly_points) >= 1:
            poly_points.pop(-1)
            
cv2.namedWindow('image')          
cv2.setMouseCallback('image',mouseCall)


def information_show():
    txt_pos = 50
    demo = np.zeros((400,800,3),np.uint8)
    text = ['Click on the image to start the polygon boundary', 
            'left click to create a  point and right click to undo the' ,
            'selection after creating a polygon press "s" to save the first polygon zone,',
            'you can create multiple zones and save it using "s"',
            'press "q" to quite the program. your points will be saved in "polygonpoints.txt"',
            'mask=True will create a polygon BW mask',
            'DISCLAMIER : YOU CAN CREATE ONLY A SINGLE POLYGON MASK FOR NOW']
    
    for i , texts in enumerate(text):
        if i == 6:
            lumina.putText(demo,texts
                    ,bbox=(20,txt_pos),scale=1,thickness=1,border=False,textcolors=(0,0,255))
        else:
            lumina.putText(demo,texts
                        ,bbox=(20,txt_pos),scale=1,thickness=1,border=False)
        txt_pos += 20
    cv2.imshow('information',demo)
    
    
def information_show_1():
    txt_pos = 50
    demo = np.zeros((400,800,3),np.uint8)
    text = ['Click on the image to start the line boundary', 
            'left click to create a  point and right click to undo the' ,
            'selection after creating a line press "s" to save the first line zone,',
            'you can create multiple line zones and save it using "s"',
            'press "q" to quite the program. your points will be saved in "linepoints.txt"',
          ]
    
    for i , texts in enumerate(text):
    
        lumina.putText(demo,texts,bbox=(20,txt_pos),scale=1,thickness=1,border=False)
        txt_pos += 20
    cv2.imshow('information',demo)






def live_polygon_zone(type:Union[image,video],path:os.PathLike,createMask:bool=False,information_view:bool=True):
    
    
    if information_view:
        information_show()
        
    with open('polypoints.txt','a+') as ff:
        ff.write(f'============ CREATED AT : {str(datetime.now())} ============ \n ')   
    
    counter = 1
    if type == 'image':

        image = cv2.imread(path)
        
    elif type == 'video':
        cap = cv2.VideoCapture(path)
        _ , image = cap.read()
        
    while True:
        
        # Display the image with points
        display_image = image.copy()
        
        # Draw the points
        for i , (px, py) in enumerate(poly_points):
            cv2.circle(display_image, (px, py), 6, (0, 0, 255), -1)
            
            if i == 0:
                cv2.line(display_image,(px,py),(px,py),(0,255,0),2,cv2.LINE_AA)
            
            cv2.line(display_image,tuple(poly_points[i-1]),tuple(poly_points[i]),(0,255,0),2,cv2.LINE_AA)
        # print(mask)
        if createMask:   
            if len(poly_points) >=3:

                    mask = lumina.create_mask(image,poly_points)
                    cv2.imwrite('mask.jpg',mask)
                    cv2.imshow('image_mask',mask)
    

        cv2.imshow('image', display_image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            
            if poly_points != []:
                print(f'[+] poly points area {counter} saved !')
                
                with open('polypoints.txt','a+') as f:
                    f.write(f'poly points area {counter} : {poly_points} \n')
                
    
                counter += 1
                poly_points.clear()
        
            
        if key == ord('q'):
            if createMask:
                print("Mask saved as mask.jpg")
            print('coordinates saved in "polypoints.txt"  file')
            break

    cv2.destroyAllWindows()
    
    
def live_line_zone(type:Union[image,video],path:os.PathLike,information_view:bool=True):
    
    
    if information_view:
        information_show_1()
    with open('linepoints.txt','a+') as ff:
        ff.write(f'============ CREATED AT : {str(datetime.now())} ============ \n')
        
    counter = 1
    if type == 'image':

        image = cv2.imread(path)
        
    elif type == 'video':
        cap = cv2.VideoCapture(path)
        _ , image = cap.read()
        
    while True:
        

        display_image = image.copy()
        
    
        if len(poly_points) <= 2:
            for i , (px, py) in enumerate(poly_points):
                cv2.circle(display_image, (px, py), 6, (0, 0, 255), -1)
                
                if i == 0:
                    cv2.line(display_image,(px,py),(px,py),(0,255,0),2,cv2.LINE_AA)
                
                cv2.line(display_image,tuple(poly_points[i-1]),tuple(poly_points[i]),(0,255,0),2,cv2.LINE_AA)
        else:
            print('[-] More than TWO points were created for line !!')
            print('[-] Create Only two points and press "s" to save the points, and do it again for more lines.')
            poly_points.clear()
       
 
        cv2.imshow('image', display_image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            
            
            if poly_points != []:
                print(f'[+] line coordinates area {counter} saved !')
                with open('linepoints.txt','a+') as f:
                    f.write(f'line coordinates area {counter} : {poly_points} \n')
                
    
                counter += 1
                poly_points.clear()
        
            
        if key == ord('q'):
     
            print('coordinates saved in "linepoints.txt"  file')
            break

    cv2.destroyAllWindows()