'''
Name: Ultimate object detector
'''
import cv2, time
#import pixcheck as pxc

def giveCount(img, low_threshold, high_threshold):
    #Faulty pixel check
    start = time.time()
    #faulty = pxc.pixcheck(img,img,img)#Change to check last 3 imgs
    #img = cv2.subtract(img,faulty)

    #Object count in faulty
    #fimgblur = cv2.GaussianBlur(faulty, (3,3), 0)
    #CHECK WHAT HAPPENS IF DON'T THRESHOLD
    #fret1, fthresh = cv2.threshold(fimgblur,low_threshold,255,3) #Needs to autoThreshold
    #fimage, fcontours, fhierachy = cv2.findContours(fthresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    #print("Faulty objects: "+str(len(fcontours)))
    
    #blur (to minimise noise)
    imgblur = cv2.GaussianBlur(img, (3,3), 0) #Gaussian (s = 0 means auto)
    #imgblur = cv2.bilateralFilter(img, 3, sigmaColor,25) #Bilateral
    end = time.time()
    blurtime = end-start
    print("Blur time: "+str(blurtime))

    start = time.time()
    #Don't think thresholding is necessary with Canny!!
    #ret1, thresh = cv2.threshold(imgblur,low_threshold,255,3)
    #ret,thresh = cv2.adaptiveThreshold(imgblur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,0)
    end = time.time()
    print("1st Threshold time: "+str(end-start)+"s")
    
    start = time.time()
    edges = cv2.Canny(imgblur,low_threshold,high_threshold)
    end = time.time()
    print("Canny time: "+str(end-start)+"s")
    image, contours, hierachy = cv2.findContours(edges, cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    count = len(contours)
    print("Objects detected: "+str(len(contours)))
    return count
    
    #cv2.imshow("preview",out)

def main():
    low_threshold = 0
   
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:", ["image="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    src = ""
    for o, a in opts:
        if o in ("-i","--image"):
            src = a
        else:
            assert False, "unhandled option"
    global img
    img = cv2.imread(src,cv2.IMREAD_GRAYSCALE)
    cv2.namedWindow("preview",cv2.WINDOW_NORMAL)
    cv2.imshow("preview",img)
    cv2.createTrackbar("Min threshold", "preview", low_threshold, 255, findContours)
    #cv2.createTrackbar("Standard dev", "preview", std, 2, findContours)
    #cv2.createTrackbar("sigmaColor", "preview", sigmaColor, 100, findContours)
    cv2.waitKey(0)
if __name__ == "__main__":
    print ("loaded libraries")
    main() 
