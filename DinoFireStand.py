import RPi.GPIO as GPIO
import time
import Adafruit_MAX31855.MAX31855 as MAX31855
import serial
import Adafruit_ADS1x15
from hx711 import HX711

GPIO.setwarnings(False)

# setup servo control
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.output(17,GPIO.LOW)
GPIO.output(18,GPIO.LOW)



loadCell=HX711(dout_pin=23,
               pd_sck_pin=24,
               channel='A',
               gain=64)
loadCell.reset()
while(True):
    print(loadCell.get_raw_data())
    time.sleep(0.1)

exit()

# setup temp sensor
sensor = MAX31855.MAX31855(11,5,9)

#setup pressure sensor
adc = Adafruit_ADS1x15.ADS1015()

def readPressure():
    values = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = adc.read_adc(i, gain=2/3, data_rate=3300)#data rate 128 or 3300
    return values    

file=open("testData.txt","a")


# ser = serial.Serial('/dev/ttyUSB0')
lastReadTime=0
with serial.Serial('/dev/ttyUSB0', 9600) as ser:
#      x = ser.read()          # read one byte
#      s = ser.read(10)        # read up to ten bytes (timeout)
    
    i = 0
    
    while(True):
#         print("hi")
        line=""
        if(ser.inWaiting()>0):
            line = ser.readline()   # read a '\n' terminated line
        elif("time" in str(line)):#
            file.write("\n"+str(line)+" "+str(time.time()))        
        if("purge" in str(line)):
            if("open" in str(line)):
                GPIO.output(17,GPIO.LOW)
                ser.write("\ropening purge valve\n\r".encode("utf-8"))
                file.write("opening purge valve")
            elif("close" in str(line)):
                GPIO.output(17,GPIO.HIGH)
                ser.write("\rclosing purge valve\n\r".encode("utf-8"))
                file.write("closing purge valve")
                print("Closing purge!\n")
        elif("main" in str(line)):
            if("close" in str(line)):
                GPIO.output(18,GPIO.LOW)
                ser.write("\rclosing main valve\n\r".encode("utf-8"))
                file.write("closing main valve")
            elif("open" in str(line)):
                GPIO.output(18,GPIO.HIGH)
                ser.write("\ropening main valve\n\r".encode("utf-8"))
                file.write("opening main valve")
        elif("UNFIRE" in str(line)):
            GPIO.output(22,GPIO.LOW)
            file.write("Turning off ignitor: "+str(time.time()))
        elif("FIRE" in str(line)):
            GPIO.output(22,GPIO.HIGH)
            file.write("igniting: "+str(time.time()))
            print("igniting: "+str(time.time()))
        elif("exit" in str(line)):
            ser.write("\rexiting program\n\n".encode("utf-8"))
            break
        elif("ABORT" in str(line)):#abort
            GPIO.output(18,GPIO.LOW)
            GPIO.output(17,GPIO.LOW)
        elif("p" in str(line)):#has p and not purge
            ser.write(("\rPressure data:"+str(readPressure())+"\r\n").encode("utf-8"))
        elif("t" in str(line)):#has p and not purge
            ser.write(("\rTemp:"+str(sensor.readTempC())+"\r\n").encode("utf-8"))
        
            
        if(time.time()>lastReadTime+0.01):
            data=("Time:"+str(time.time()))+("\nPressure data:"+str(readPressure()))+("\nTemp:"+str(sensor.readTempC())+"\n\n")
            file.write(data)
            lastReadTime=time.time()

ser.close()
GPIO.cleanup()





# 
# p = GPIO.PWM(12,50)
# p.start(10)
# 
# 
# 
# 
# 
# p.ChangeDutyCycle(7.5)
# time.sleep(2)
# p.ChangeDutyCycle(12)
# time.sleep(2)
# p.ChangeDutyCycle(7.5)
# time.sleep(2)
# p.ChangeDutyCycle(12)
# time.sleep(2)
# 
# 
# 
# 
# GPIO.cleanup()

#while True:
#	x=input("angle ")
#	servo x