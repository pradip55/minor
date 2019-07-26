import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)
def THRESHOLD():
    return 30

class ultraSound:
	TRIG = 20 
	ECHO = 21
	#LED=16
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.TRIG,GPIO.OUT)
		GPIO.setup(self.ECHO,GPIO.IN)
                #GPIO.setup(self.LED,GPIO.OUT)
	
	def readData(self):
		GPIO.output(self.TRIG, False)
		#print "Waitng For Sensor To Settle"
		time.sleep(2)
		GPIO.output(self.TRIG, True)
		time.sleep(0.00001)                      
		GPIO.output(self.TRIG, False)                 
		pulse_start=0;
		pulse_end=0;
		while GPIO.input(self.ECHO)==0:               
			pulse_start = time.time()              
		while GPIO.input(self.ECHO)==1:               
			pulse_end = time.time()                
		
		pulse_duration = pulse_end - pulse_start 
		distance = pulse_duration * 17150        
		distance = round(distance, 2)
		print "Distance:",distance,"cm" 
		time.sleep(0.4) 
		return distance;
               



sensor=ultraSound();
while True:
	sensor.readData();
        if(sensor.readData()<=THRESHOLD()):
		GPIO.output(16,GPIO.HIGH)
		print "WARNING THE LEVEL OF WATER HAS RAISED BEYOND THE THRESHOLD LEVEL"
        else:
		GPIO.output(16,GPIO.LOW)
