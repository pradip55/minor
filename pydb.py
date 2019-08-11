import RPi.GPIO as GPIO
import dht11
import time
import datetime
import MySQLdb

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin=14)
GPIO.setup(16,GPIO.OUT)
def THRESHOLD():
    return 20


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
        time.sleep(0.4) 
        return distance;

sensor=ultraSound();
while True:
    remarks_val="Nothing to Worry"
    result = instance.read()
    distance=sensor.readData();
    dateandtime=datetime.datetime.now() 
    if result.is_valid():
            print("Time: " + str(datetime.datetime.now()))
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
            print "Distance:",distance,"cm" 
            time.sleep(3)
            print"----------------------------------------------------"
    if(distance<=THRESHOLD()):
            GPIO.output(16,GPIO.HIGH)
            print "WARNING THE LEVEL OF WATER HAS RAISED BEYOND THE THRESHOLD LEVEL"
            remarks_val="WARNING THE LEVEL OF WATER HAS RAISED BEYOND THE THRESHOLD LEVEL"
    else:
            GPIO.output(16,GPIO.LOW)
            print"----------------------------------------------------"
           
    conn=MySQLdb.connect(host="localhost",user="root",passwd="shrestha5555",db="minor")
    cur=conn.cursor()
    sql_query="""INSERT INTO Data (DateTime,Temperature,Humidity,Distance,Remarks) VALUES (%s,%s,%s,%s,%s)"""
    cur.execute(sql_query,(dateandtime,result.temperature,result.humidity,distance,remarks_val))
    conn.commit()
    conn.close()  
    
   
