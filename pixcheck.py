import cv2, sys, math, numpy

def pixcheck(imgs):
    global cv2
    if len(imgs)>1:
        #Find overlap between first two images
        overlap = cv2.bitwise_and(imgs[0],imgs[1])
        imgs.pop(0)
        imgs.pop(0)
        if(len(imgs)>0):
            for img in imgs:
                overlap = cv2.bitwise_and(overlap,img)
        return overlap
    else:
        #Not enough images
        return False
