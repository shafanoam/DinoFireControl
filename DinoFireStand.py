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
GPIO.output(17,GPIO.LOW)
GPIO.output(18,GPIO.LOW)

# setup igniter control GPIO
GPIO.setup(22,GPIO.OUT)




loadCell = HX711(dout_pin=23,
               pd_sck_pin=24,
               channel='A',
               gain=64)
loadCell.reset()
# print((loadCell.get_raw_data()))
# 
# exit()

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

with open("testData.txt","a") as file:


    # ser = serial.Serial('/dev/ttyUSB0')
    lastReadTime=0
    with serial.Serial('/dev/ttyUSB0', 9600) as ser:
    #      x = ser.read()          # read one byte
    #      s = ser.read(10)        # read up to ten bytes (timeout)
        
        i = 0
        
    # firing state variable lets loop know if it's currently firing
        firingState = 0
        
        while(True):
    #         print("hi")
            line=""
            if(ser.inWaiting()>0):
                line = ser.readline()   # read a '\n' terminated line
            elif("time" in str(line)):#
                file.write("\n"+str(line)+" "+str(time.time()))        
            
            
            if("cancel" in str(line)):
                pass
            
            elif("purge" in str(line)):
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
                if firingState:
                    GPIO.output(22,GPIO.LOW)
                    igniterOn = 0
                    file.write("Turning off igniter: "+str(time.time()))
                    ser.write(("\rTurning off igniter: "+str(time.time()) + "\n\r").encode("utf-8"))
                    print("Turning off igniter: "+str(time.time()))
                
            
            elif("FIRE" in str(line)):
                if("92130" in str(line)):
                    if not firingState:
                        GPIO.output(22,GPIO.HIGH)
                        timeStartFiring = time.time()
                        file.write("Igniting: "+str(time.time()))
                        ser.write(("\rIgniting: "+str(time.time()) + "\n\r").encode("utf-8"))
                        print("Igniting: "+str(time.time()))
                        firingState = 1
                        igniterOn = 1
                    else:
                        file.write("Note: 'FIRE' command recieved but already firing.")
                        ser.write(("\r'FIRE' command recieved but already firing." + "\n\r").encode("utf-8"))
                        print("'FIRE' command recieved but already firing.")
                else:
                    file.write("Wrong firing password entered! Recieved: " + str(line))
                    ser.write(("\rWrong firing password entered!\n\r").encode("utf-8"))
                    print("Wrong firing password entered! Recieved: " + str(line))
                
                
            elif("exit" in str(line)):
                ser.write("\rexiting program\n\n".encode("utf-8"))
                break
            
            elif("ABORT" in str(line)):#abort
                GPIO.output(18,GPIO.LOW)
                GPIO.output(17,GPIO.LOW)
                # turn off igniter signal
                GPIO.output(22,GPIO.LOW)
                igniterOn = 0
                ser.write(("\rABORTING!\n\r").encode("utf-8"))
                
            elif("pressure_get" in str(line)):
                ser.write(("\rPressure data: "+str(readPressure())+"\r\n").encode("utf-8"))
                
            elif("temperature_get" in str(line)):
                ser.write(("\rTemp: "+str(sensor.readTempC())+"\r\n").encode("utf-8"))
                
            elif("loadcell_get" in str(line)):
                ser.write(("\rLoad Cell Values: " + str(loadCell.get_raw_data()) + " in lbs:" + str((-loadCell.get_raw_data()[0]+20383)/19191)).encode("utf-8"))
            
            # while firing, keep making sure valves are in correct position
            if firingState:
                GPIO.output(18,GPIO.HIGH)
                GPIO.output(17,GPIO.HIGH)
            
            # turn off igniter signal after 2 seconds, because it's possible for a short to happen and we don't want any fires
            if(firingState and igniterOn and (time.time()>timeStartFiring + 2)):
                GPIO.output(22,GPIO.LOW)
                igniterOn = 0
                file.write("Turned off igniter signal: "+str(time.time()))
                ser.write(("\rTurned off igniter signal: "+str(time.time()) + "\n\r").encode("utf-8"))
                print("Turned off igniter signal: "+str(time.time()))
            
            # once five seconds have elapsed, close main / open purge and notify user.
            if(firingState and (time.time()>timeStartFiring + 5)):
                GPIO.output(18,GPIO.LOW)
#                 GPIO.output(17,GPIO.LOW)
                firingState = 0
                file.write("Engine fired successfully: "+str(time.time()))
                ser.write(("\rEngine fired successfully: "+str(time.time()) + "\n\r").encode("utf-8"))
                print("Engine fired successfully: "+str(time.time()))
            
                
            if(time.time()>lastReadTime+0.01):
#                 data=("Time:"+str(time.time()))+("\nPressure data:"+str(readPressure()))+("\nTemp:"+str(sensor.readTempC()))+("\nForce:"+str(loadCell.get_raw_data())+"\n\n")
                data=("Time:"+str(time.time()))+("\nPressure data:"+str(readPressure()))+("\nTemp:"+str(sensor.readTempC()))+("\n\n")
            
                file.write(data)
#                 print("h")
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