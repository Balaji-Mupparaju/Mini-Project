import BlynkLib
import RPi.GPIO as GPIO
import time
import Adafruit_DHT

BLYNK_AUTH = 'YourAuthToken'

blynk = BlynkLib.Blynk(BLYNK_AUTH)

GPIO.setmode(GPIO.BOARD)
DHT_PIN = 12
BUZZER_PIN = 11
PIR_PIN = 4
MQ2_PIN = 17
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(MQ2_PIN, GPIO.IN)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

@blynk.on("readV1")
def readDHT():
    humidity, temperature = Adafruit_DHT.read_retry(11, DHT_PIN)
    if humidity is not None and temperature is not None:
        blynk.virtual_write(1, humidity)
        blynk.virtual_write(2, temperature)
        if temperature > 25:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)


@blynk.on("readV2")
def readPIR():
    value = GPIO.input(PIR_PIN)
    blynk.virtual_write(1, value)
    if value == 1:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
    else:
        GPIO.output(BUZZER_PIN, GPIO.LOW)

@blynk.on("readV3")
def readMQ2():
    value = GPIO.input(MQ2_PIN)
    blynk.virtual_write(1, value)
    if value == 1:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
    else:
        GPIO.output(BUZZER_PIN, GPIO.LOW)

@blynk.on("readV4")
def read_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == False:
        start = time.time()
    while GPIO.input(ECHO) == True:
        end = time.time()
    duration = end - start
    distance = duration * 17150
    blynk.virtual_write(0, distance)

    if distance <= 50:
         GPIO.output(BUZZER, GPIO.HIGH)
    else:
         GPIO.output(BUZZER, GPIO.LOW)

while True:
    print('temprature:',temprature)
    print('humidity:',humudity)
    distance = read_distance()
    print('Distance:', distance, 'cm')
    gaslevel=readmq2()
    print('gas level:' gaslevel)
    blynk.run() # Add this line to start the Blynk connection
    time.sleep(1)