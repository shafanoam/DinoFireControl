from hx711 import HX711
from threading import *
import time


loadCell = HX711(dout_pin=23,
               pd_sck_pin=24,
               channel='A',
               gain=64)
loadCell.reset()

def loadCell_thread():
    with open("loadData.txt","a") as Loadfile:
        while True:
            i = 0
            for item in loadCell.get_raw_data():
                Loadfile.write("\nTime: " +  str(time.time() - i))
                Loadfile.write("\nRaw: " + str(item))
                Loadfile.write("\nLbs: " +  str((-item - 0.5*20000)/19191))
                print("\nLbs: " +  str((-item - 0.5*20000)/19191))
                Loadfile.write("\n")
                i = i - 0.1


loadCellThread = Thread(target=loadCell_thread)
loadCellThread.start()

i = 0
while True:
    #print(i)
    i += 1
    time.sleep(0.1)
