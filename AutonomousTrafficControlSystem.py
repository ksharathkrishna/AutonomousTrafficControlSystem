import urllib.request
import sys
import RPi.GPIO as GPIO
import random


import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#declarations
TRIG1 = 23

ECHO1 = 24

TRIG2 = 26

ECHO2 = 19

TRIG3 = 17

ECHO3 = 27

TRIG4 = 3

ECHO4 = 2

n=0
e=0
w=0
s=0
f=[0]*4




#cloud 
myAPI='1GBHTIXHNXSV92ST'

baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
def tscloud(n,e,s,w):
    conn = urllib.request.urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field4=%s' %(n,e,s,w))
    print (conn.read())
    # Closing the connection
    conn.close() 







#algorithm
def distance(TRIG,ECHO):
     print ("Distance Measurement In Progress\n")

     
     global pulse_star
     GPIO.setup(TRIG,GPIO.OUT)

     GPIO.setup(ECHO,GPIO.IN)

     GPIO.output(TRIG, False)

     print ("Waiting For Sensor To Settle")
     print()

     time.sleep(0.5)


     GPIO.output(TRIG, True)

     time.sleep(0.00001)

     GPIO.output(TRIG, False)

     while GPIO.input(ECHO)==0:

         pulse_star = time.time()


     while GPIO.input(ECHO)==1:
 
         pulse_end = time.time()      

     pulse_duration = pulse_end - pulse_star
     distance = pulse_duration * 17150



     distance = round(distance, 2)
     time.sleep(2)
     if distance<30 :
         return 1

     return 0

def detect(mv):
    time.sleep(2)
    n = distance(TRIG1,ECHO1)
    s = distance(TRIG2,ECHO2)
    e = distance(TRIG3,ECHO3)
    w = distance(TRIG4,ECHO4)
    if(n==1):
        if(mv!=0):
            f[0]+=1
    if(e==1):
        if(mv!=1):
            f[1]+=1
    if(s==1):
        if(mv!=2):
            f[2]+=1
    if(w==1):
        if(mv!=3):
            f[3]+=1
    tscloud(f[0],f[1],f[2],f[3])
            
    print(f)
    print ("Sensor 1 = %d\n" % n)
    time.sleep(1)
    print ("Sensor 2 = %d\n" % e)
    time.sleep(1)
    print ("Sensor 3 = %d\n" % w)
    time.sleep(1)
    print ("Sensor 4 = %d\n" % s)
    print()
    time.sleep(1)
    return


def gled(mv,f):
        pno=[25,1,20,22]
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        print("inside led")
        GPIO.setup(pno[mv],GPIO.OUT)
        print ("LED on"+str(mv))
        GPIO.output(pno[mv],GPIO.HIGH)
        f[mv]=0

        detect(mv)
        time.sleep(1)
        print ("LED off")
        GPIO.output(pno[mv],GPIO.LOW)
        time.sleep(2)
   
    
         return


if __name__ == '__main__':
    
    try:
        f[0]=1
        while True:
            mv=f.index(max(f))
            if max(f)==0 :
                mv=random.randint(1,3)
            print(mv)
            #led code
            gled(mv,f)
            
            
            
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    GPIO.cleanup()










