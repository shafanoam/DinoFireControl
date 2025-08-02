# firingState and timeStartFireing relate to Dawn Runner and its firing sequence. This involves powering the ignitors, wawiting a short time, and then setting the valves to a configuration in which nitrous flows from the main tank into the engine, with the purge valve closed. Midway through the fire, the ignitor is turned off, and after the prescribed length of the fire the main valve is closed and the purge opened, cutting off the flow of oxidizer to the engine.
# For Archaeopteryx, the sequence is different: when the sequence begins, the variable xxxxx and xxxxx are set. The purge valve is kept closed, continious data sending to serial is initiated, and the main valve switches from open to closed. After 0.1 seconds the deluge servo is pulled(we don't know if the battery can power all 3 at once). At 2 seconds, the ignitor is fired. at 3 seconds, the ignitor is stopped. After 12 seconds, stop sending stream of data.


import RPi.GPIO as GPIO
import time
import Adafruit_MAX31855.MAX31855 as MAX31855
import serial
import Adafruit_ADS1x15
from hx711 import HX711
from threading import *
print("finished imports")
GPIO.setwarnings(False)

# setup servo control
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.LOW)
GPIO.output(18,GPIO.LOW)

# setup igniter control GPIO
GPIO.setup(22,GPIO.OUT)





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

lastWeight = 0

def loadCell_thread():
    # setting up the load cell
    loadCell = HX711(dout_pin=23,
                     pd_sck_pin=24,
                     channel='A',
                     gain=64)
    # TODO: Misha pls explain
    loadCell.reset()
    global lastWeight
    
    with open("loadData.txt","a") as Loadfile:
        while True:
            i = 0
            for item in loadCell.get_raw_data():
                Loadfile.write("\nTime: " +  str(time.time() - i))
                Loadfile.write("\nRaw: " + str(item))
                Loadfile.write("\nLbs: " +  str((-item - 1.15*20000)/10191))
                Loadfile.write("\n")
                i = i - 0.1
                lastWeight = (-item - 1.15*20000)/10191

# the reason there's no provision to stop the thread, is that it writes data slowly enough that space isn't a concern. Stretch goal is to have one, though.
loadCellThread = Thread(target=loadCell_thread)
loadCellThread.start()


# MAIN RUNTIME CODE
print("about to open file")
with open("testData.txt","a") as file:
    print("FROG")
    # ser = serial.Serial('/dev/ttyUSB0')
    lastReadTime=0
    with serial.Serial('/dev/ttyUSB0', 9600) as ser:
    #      x = ser.read()          # read one byte
    #      s = ser.read(10)        # read up to ten bytes (timeout)
        
        i = 0
        
    # firing state variable lets loop know if it's currently firing
        firingState = 0
        
        firingState2=0


        
        # now that everything's ready to enter the loop, we let the operator know
        ser.write("\rDinoFireStand initialized successfully, awaiting commands.\n\r".encode("utf-8"))
        
        while(True):
    #         print("hi")
            line="n-o-n-e"
            #n one written like this will never be a command.
            # it may thus be used as the default string so that an empty line recieved from the serial can be used to poll for data
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
                    file.write("opening purge valve\n")
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
                        file.write("Igniting: " + str(time.time()) + "\n")
                        ser.write(("\rIgniting: "+str(time.time()) + "\n\r").encode("utf-8"))
                        print("Igniting: "+str(time.time()))
                        firingState = 1
                        igniterOn = 1
                    else:
                        file.write("Note: 'FIRE' command recieved but already firing.\n")
                        ser.write(("\r'FIRE' command recieved but already firing." + "\n\r").encode("utf-8"))
                        print("'FIRE' command recieved but already firing.")
                else:
                    file.write("Wrong firing password entered! Recieved: " + str(line) + "\n")
                    ser.write(("\rWrong firing password entered!\n\r").encode("utf-8"))
                    print("Wrong firing password entered! Recieved: " + str(line))
                    
                    
            
            elif("ignite" in str(line)): # for second engine Archaeopteryx
                if("92130" in str(line)):
                    if not firingState2:
                        firingState2=1
                        timeStartFiring = time.time()
                        GPIO.output(17,GPIO.LOW) # open "purge" (wired to deluge system)
                        # GPIO.output(18,GPIO.LOW) # close main after 0.15 seconds
                        
                        file.write("Igniting in 2 seconds. Now: " + str(timeStartFiring) + "\n")
                        ser.write(("\rIgniting in 2 seconds. Now: "+str(timeStartFiring) + "\n\r").encode("utf-8"))
                        print("Igniting in 2 seconds. Now: "+str(timeStartFiring))
                        igniterOn = 0
                    else:
                        file.write("Note: 'ignite' command recieved but already started.\n")
                        ser.write(("\r'ignite' command recieved but already started." + "\n\r").encode("utf-8"))
                        print("'ignite' command recieved but already started.")
                else:
                    file.write("Wrong ignition password entered! Recieved: " + str(line) + "\n")
                    ser.write(("\rWrong ignition password entered!\n\r").encode("utf-8"))
                    print("Wrong ignition password entered! Recieved: " + str(line))
                    
                        
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
            
                
            
            
            # elif("loadcell_get" in str(line)):
            #     ser.write(("\rLoad Cell Values: " + str(loadCell.get_raw_data()) + " in lbs:" + str((-loadCell.get_raw_data()[0]+20383)/19191)).encode("utf-8"))
            
            # while firing, keep making sure valves are in correct position
            if (firingState and (time.time()>(timeStartFiring+0.15))):
                GPIO.output(18,GPIO.HIGH)
                GPIO.output(17,GPIO.HIGH)
                
            if (firingState2):
                GPIO.output(18,GPIO.LOW)
                if(time.time()>(timeStartFiring+0.15)):
                    GPIO.output(17,GPIO.LOW)
                
            
            # turn off igniter signal after 2 seconds, because it's possible for a short to happen and we don't want any fires
            if(firingState and igniterOn and (time.time()>timeStartFiring + 2)):
                GPIO.output(22,GPIO.LOW)
                igniterOn = 0
                file.write("Turned off igniter signal: "+str(time.time())+"\n")
                ser.write(("\rTurned off igniter signal: "+str(time.time()) + "\n\r").encode("utf-8"))
                print("Turned off igniter signal: "+str(time.time()))
                
            if(firingState2 and igniterOn==0 and (time.time()>timeStartFiring + 2) and (time.time()<=timeStartFiring + 4)):
                GPIO.output(22,GPIO.HIGH)
                igniterOn = 1
                file.write("Turned on igniter signal: "+str(time.time())+"\n")
                ser.write(("\rTurned on igniter signal: "+str(time.time()) + "\n\r").encode("utf-8"))
                print("Turned on igniter signal: "+str(time.time()))
                
            if(firingState2 and igniterOn==1 and (time.time()>timeStartFiring + 4)):
                GPIO.output(22,GPIO.LOW)
                igniterOn = 0
                file.write("Turned off igniter signal: "+str(time.time())+"\n")
                ser.write(("\rTurned off igniter signal: "+str(time.time()) + "\n\r").encode("utf-8"))
                print("Turned off igniter signal: "+str(time.time()))
            
            # once five seconds have elapsed, close main / open purge and notify user.
            if(firingState and (time.time()>timeStartFiring + 5.15)):
                GPIO.output(18,GPIO.LOW)
#                 GPIO.output(17,GPIO.LOW)
                firingState = 0
                file.write("Engine fired successfully: " + str(time.time()) + "\n")
                ser.write(("\rEngine fired successfully: "+str(time.time()) + "\n\r").encode("utf-8"))
                print("Engine fired successfully: "+str(time.time()))
                
            if(firingState2 and (time.time()>timeStartFiring + 22)):
                firingState2 = 0
                file.write("Engine fired successfully: " + str(time.time()) + "\n")
                ser.write(("\rEngine fired successfully: "+str(time.time()) + "\n\r").encode("utf-8"))
                print("Engine fired successfully: "+str(time.time()))
            
            if(str(line)!="n-o-n-e"):
                ser.write(("\rPressure data: "+str(readPressure())+"\r\n").encode("utf-8"))
                ser.write(("\rTemp: "+str(sensor.readTempC())+"\r\n").encode("utf-8"))
                ser.write(("\rLoad Cell data: "+str(lastWeight)+"\r\n").encode("utf-8"))
                
            if(time.time()>lastReadTime+0.01):
#                 data=("Time:"+str(time.time()))+("\nPressure data:"+str(readPressure()))+("\nTemp:"+str(sensor.readTempC()))+("\nForce:"+str(loadCell.get_raw_data())+"\n\n")
                data=("Time:"+str(time.time()))+("\nPressure data:"+str(readPressure()))+("\nTemp:"+str(sensor.readTempC()))+("\nLbs: "+str(lastWeight))+("\n\n")
                
                if(firingState2):
                    ser.write(("\rTime elapsed: "+str(round(time.time()-timeStartFiring, 6))+"\t\tPressure data: "+str(readPressure())+"\t\tTemp: "+str(sensor.readTempC())+"\t\tLoad Cell data: "+str(lastWeight)+"\r\n").encode("utf-8"))
                
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