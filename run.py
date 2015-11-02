import sys, getopt, time, picamera.array, cv2, os, numpy, errno
import counter, pixcheck, show
#Set some variables:

#Get options
try:
    opts, args = getopt.getopt(sys.argv[1:], "n:", ["name="])
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

for o, a in opts:
    if o in("-n","--name"):
         name = a
    else:
        assert False, "unhandled option"
#Start camera
with picamera.PiCamera() as camera:
    #LED automatically turns on, this turns it off
    camera.led = False
    #display a big c on screen!
    show.calibrateMessage()
    framerate = 1
    
    time.sleep(1) # Allows automatic gain control to settle
    #Now fix auto white balance
    camera.awb_mode = "off"
    g = camera.awb_gains
    camera.awb_gains = g
    camera.framerate = framerate
    camera.shutter_speed = int(1000000/camera.framerate) #Shutter speed is in microseconds
    camera.exposure_mode = "off"
    camera.iso = 800

    #take 4 startup pictures for faulty pixel check and analysis on ground later
    
    filename=name+"/"
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True) #Sometimes this doesn't work find out why!!
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    #Saves in bmp format
    camera.capture_sequence([filename+'start%03d.bmp' % i for i in range(4)], format="bmp")
    i1 = cv2.imread(name+"/start000.bmp",cv2.IMREAD_GRAYSCALE)
    i2 = cv2.imread(name+"/start001.bmp",cv2.IMREAD_GRAYSCALE)
    i3 = cv2.imread(name+"/start002.bmp",cv2.IMREAD_GRAYSCALE)
    i4 = cv2.imread(name+"/start003.bmp",cv2.IMREAD_GRAYSCALE)
    gallery = [i1,i2,i3,i4]
    faulty = pixcheck.pixcheck(list(gallery))
    cv2.imwrite(name+"/faulty.bmp",faulty)
    #Start stream
    with picamera.array.PiRGBArray(camera) as stream:
        i = 0
        while True:
            #Capture
            camera.capture(stream, "rgb")
            img=stream.array
            #Convert to intensity
            grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            
            #Remove faulty pixels
            start = time.time()
            #Load images cached
            gallery.append(grey)
            if (len(gallery) > 4):
                gallery.pop(0) 
            faulty = pixcheck.pixcheck(list(gallery))
            subtracted = numpy.count_nonzero(faulty)
            print("Subtracted pixels: "+str(subtracted))
            #save this
            cv2.imwrite(name+"/faulty.bmp",faulty)
            end= time.time()
            print("Faulty/noisy pixel check time: "+str(end-start))
            
            #find objects
            high_threshold = 100
            low_threshold = 5
            counts = counter.giveCount(img,low_threshold,high_threshold)
            rate = counts*framerate
            print("Rate: "+str(rate))
            show.draw(rate,subtracted)
            
            print ("Img "+str(i))
            i+=1
            stream.seek(0)
            stream.truncate()