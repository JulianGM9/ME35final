#this code listens for a start message from the main hub in order to open a servo

import machine
import time
from now import Now
servo_flag = False

def my_callback(msg, mac):
    if msg==b'marblestart':
        global servo_flag
        servo_flag=True
        time.sleep(2)
        print(mac, msg)
        print('servo flag is ' + str(servo_flag))
n = Now(my_callback)
#n.connect()

# Create a PWM object on GPIO18
servo_pin = machine.Pin(18)  # Pin GPIO18
pwm = machine.PWM(servo_pin)

# Set the PWM frequency (50 Hz is typical for most servos)
pwm.freq(50)

# initialize the servo position
set_servo_angle(0)

# Function to set servo angle (0 to 180 degrees)
def set_servo_angle(angle):
    # Servo angle to pulse width conversion (duty cycle)
    duty = int((angle / 180) * 1023 + 40)  # 40-115 is the typical duty range for 0-180 degrees
    pwm.duty(duty)

# Main loop
try:
    while True:
        print(servo_flag)
        if servo_flag:
            # Move the servo to 90 degrees if the flag is True
            set_servo_angle(90)
            print("Servo moved to 90 degrees!")
            time.sleep(3)
            # Reset the flag (optional - to stop continuously moving to 90 degrees)
            servo_flag = False
            set_servo_angle(0)
            
            
        time.sleep(0.1)  # Check the flag every 100ms
except KeyboardInterrupt:
    print("Interrupted! Cleaning up...")

finally:
    # Ensure interfaces are deactivated on exit
    n.close()
