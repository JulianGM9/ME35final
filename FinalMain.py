#This code runs on the hub ESP. It sends the start message on boot, and lights up the LED's when it receives success messages from the
#peripheral ESPs. 

from now import Now
import time
from machine import Pin
from Tufts_ble import Sniff, Yell

LED_1 = 0
led1 = Pin(LED_1, Pin.OUT)

LED_2 = 1
led2 = Pin(LED_2, Pin.OUT)

LED_3 = 2
led3 = Pin(LED_3, Pin.OUT)

flag1=False
flag2=False
flag3=False
endflag=False
levelflag=1

def flash(led):
    print("flashing...")
    print(led)
    if led==1:
        led1.value(1)
        time.sleep(.5)
        led1.value(0)
        time.sleep(.5)
    if led==2:
        led2.value(1)
        time.sleep(.5)
        led2.value(0)
        time.sleep(.5)
    if led==3:
        led3.value(1)
        time.sleep(.5)
        led3.value(0)
        time.sleep(.5)

def allflash():
    for i in range(10):
        led1.value(1)
        led2.value(1)
        led3.value(1)
        time.sleep(.5)
        led1.value(0)
        led2.value(0)
        led3.value(0)
        time.sleep(.5)
    

def my_callback(msg, mac):
    print('callback run')
    global flag1
    global flag2
    global flag3
    
    if msg == b'1complete':
        flag1=True

        print('turning on led 1')
    if msg == b'2complete':
        flag2=True
        
        print('turning on led 2')
        
    if msg == b'3complete':
        flag3=True
        print('turning on led 3')
        
    else:
        pass
    msg=''
   
        
        
    

n = Now(my_callback)
n.connect()
print(n.wifi.config('mac'))

try:
    while True:
        flash(levelflag)
        if flag1==True and levelflag==1:
            led1.value(1)
            levelflag=2
            flag1=False
        else:
            pass
            
        if flag2==True and levelflag==2:
            led2.value(1)
            levelflag=3
            flag2=False
        else:
            pass

        if flag3==True and levelflag==3:
            led3.value(1)
            time.sleep(3)
            allflash()
            flag3=False
            endflag=True
        else:
            pass
        
        if endflag==True:
             led1.value(0)
             led2.value(0)
             led3.value(0)
             flag1=False
             flag2=False
             flag3=False
             endflag=False
             levelflag=1
             
        time.sleep(1)
        

        

except KeyboardInterrupt:
    print("Interrupted! Cleaning up...")
    led1.value(0)
    led2.value(0)
    led3.value(0)

finally:
    # Ensure interfaces are deactivated on exit
    n.close()
