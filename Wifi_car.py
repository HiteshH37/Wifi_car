import time
import network
from machine import Pin,PWM
import BlynkLib
from servo import Servo

led=Pin('LED',Pin.OUT)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID","PASSWORD")      #Type your wifi name/SSID and password
 
BLYNK_AUTH = 'ATHENTICATION_TOKEN'     #type your authentication token from blynk application
 
# Wait for network connection
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    led.value(1)
    time.sleep(2)
    led.value(0)
    raise RuntimeError('network connection failed')

else:
    led.value(1)
    print('connected')
    ip = wlan.ifconfig()[0]
    print('IP: ', ip)
 
# Connect to Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Motor driver pins
motor_pwm = PWM(Pin(2))
motor_dir1 = Pin(3, Pin.OUT)                 #motor pins 
motor_dir2 = Pin(4, Pin.OUT)

# Initialize motor speed
motor_pwm.freq(1500)
motor_pwm.duty_u16(0)

#Servo pin
servo_=Servo(0)                                     #servo motor pin

# Register virtual pin handler
@blynk.on("V0")
def set_servo_angle_handler(value): #read the value
    ang=int(value[0])
    y=((60/127)*ang)+90
    servo_.angle(int(y))
    print("angle:",y)
    
@blynk.on("V1")
def set_motor_speed_handler(value): #read the value
     speed = int(value[0])
     duty_cycle=int((257*speed))
     if speed >128:
         motor_dir1.high()
         motor_dir2.low()
         motor_pwm.duty_u16(duty_cycle)
         print("speed , on , off ",speed,duty_cycle)
     elif speed == 128:
         motor_dir1.low()
         motor_dir2.low()
         motor_pwm.duty_u16(0)
         print("speed , off , off ",speed)
     else:
         duty_cycle=65536-duty_cycle
         motor_dir1.low()
         motor_dir2.high()
         motor_pwm.duty_u16(duty_cycle)
         print("speed, off , on ",speed,duty_cycle)
         
       
while True:
    blynk.run()
    time.sleep(0.01)
    

