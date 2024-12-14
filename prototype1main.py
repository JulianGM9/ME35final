#this code runs on the main hub. It sends the start message on a button press, and listens for success messages from the peripheral ESPs to light up the LEDs. 

from now import Now
import time
from machine import Pin
from Tufts_ble import Sniff, Yell

def ble_broadcast(msg, dur):
    p=Yell()
    for i in range(10*dur):
        p.advertise(f'{msg}')
        print('advertising...')
        time.sleep(.1)
    p.stop_advertising()
    print("broadcasting stopped")

BUTTON_PIN = 21
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

LED_1 = 2
led1 = Pin(LED_1, Pin.OUT)

LED_2 = 3
led2 = Pin(LED_2, Pin.OUT)

LED_3 = 4
led3 = Pin(LED_3, Pin.OUT)

LED_4 = 5
led4 = Pin(LED_4, Pin.OUT)

flag1=False
flag2=False
flag3=False
flag4=False
toggleflag=True


def my_callback(msg, mac):
    print('callback run')
    global flag1
    global flag2
    global flag3
    global flag4
    if msg == b'1complete':
        flag1=True
        print('turning on led 1')
    if msg == b'2complete':
        flag2=True
        print('turning on led 2')
    if msg == b'3complete':
        flag3=True
        print('turning on led 3')
    if msg == b'4complete':
        flag4=True
        print('turning on led 4')
    else:
        pass
    if flag1 and flag2 and flag3 and flag4:
        ble_broadcast('game done', 5)
    else:
        pass
        
        
    

n = Now(my_callback)
n.connect()
print(n.wifi.config('mac'))

try:
    while True:
        print('button value is ' + str(button.value()))
        if button.value()==0:
            n.publish(b'marblestart')
            print("publishing start command")
        else:
            pass

        if flag1==True:
            led1.value(1)
        else:
            led1.value(0)
            
        if flag2==True:
            led2.value(1)
        else:
            led2.value(0)

        if flag3==True:
            led3.value(1)
        else:
            led3.value(0)

        if flag4==True:
            led4.value(1)
        else:
            led4.value(0)

        if flag1==True and flag2==True and flag3==True and toggleflag==True:
            n.publish(b'hopscotchstart')
            print('publishing hopscotch')
            toggleflag=False
        time.sleep(1)
        

        

except KeyboardInterrupt:
    print("Interrupted! Cleaning up...")

finally:
    # Ensure interfaces are deactivated on exit
    n.close()
