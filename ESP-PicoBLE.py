#This program is for the communication between the Hopscotch peripheral esp and the pico controlling the hopscotch game. The code listens for a start message from
#the main hub before broadcasting to the pico over ble telling it to start. It then listens for a ble message back from the pico indicating the game has been
#completed and then broadcasts on ESP-Now back to the main hub that hopscotch is complete. 

import time
from Tufts_ble import Sniff, Yell
from now import Now

mac='' #add the mac address of the main hub esp (julians esp)

def central():
    c = Sniff('%', verbose = False)
    c.scan(0) 
    flag=True
    while flag==True:
        print("listening...")
        latest = c.last
        if latest:
            c.last='' 
            print('Got: ' + latest)
            flag=False
        time.sleep(0.1)
        #print("listening...")
    print("done listening")


def ble_broadcast(msg, dur):
    p=Yell()
    for i in range(10*dur):
        p.advertise(f'{msg}')
        print('advertising...')
        time.sleep(.1)
    p.stop_advertising()
    print("broadcasting stopped")

def my_callback(msg, mac):
    if msg==b'hopscotchstart':
        ble_broadcast('%hopscotch', 5)
        central()
        n.publish(b'4complete', mac)
        print(mac, msg)
    

n = Now(my_callback)
n.connect()
try:
    while True:
        #print('waiting...')
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted! Cleaning up...")

finally:
    # Ensure interfaces are deactivated on exit
    n.close()

