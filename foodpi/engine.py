import spidev
import time
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
spi = spidev.SpiDev()
spi.open(0,0)

#Channel ID for Sensors
sen1 = 0
sen2 = 1
sen3 = 2

# GPIO signals to use
dht_pin = '18'

# Physical pins 11,15,16,18 for Stepper Motor
# GPIO17,GPIO22,GPIO23,GPIO24
StepPins = [17,22,23,24]
# Set all pins as output
for pin in StepPins:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

def sprayOxi():

	# Define advanced sequence
	# as shown in manufacturers datasheet
	Seq = [[1,0,0,1],
	       [1,0,0,0],
    	   [1,1,0,0],
    	   [0,1,0,0],
    	   [0,1,1,0],
    	   [0,0,1,0],
    	   [0,0,1,1],
    	   [0,0,0,1]]
       
	StepCount = len(Seq)

#Full torque
#StepCount3 = 4
#Seq3 = [[0,0,1,1],
#		[1,0,0,1],
#		[1,1,0,0],
#		[0,1,1,0]]

	StepDir = 1 # Set to 1 or 2 for clockwise
	            # Set to -1 or -2 for anti-clockwise

	# Read wait time from command line
	WaitTime = 10/float(1000)

	# Initialise variables
	StepCounter = 0

	# Start main loop
	while True:
		print StepCounter,
		print Seq[StepCounter]

		for pin in range(0, 4):
			xpin = StepPins[pin]
	    	if Seq[StepCounter][pin]!=0:
	      		print " Enable GPIO %i" %(xpin)
	      		GPIO.output(xpin, True)
	    	else:
	    		GPIO.output(xpin, False)

		StepCounter += StepDir
		# If we reach the end of the sequence
  		# start again
		if (StepCounter>=StepCount):
    		StepCounter = 0
  		if (StepCounter<0):
    		StepCounter = StepCount+StepDir

		# Wait before moving on
		time.sleep(WaitTime)
	GPIO.cleanup();
	for pin in StepPins:
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin, False)


#To read data from ADC given Channel Number as 'adcnum'
def readadc(adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        r = spi.xfer2([1,(8+adcnum)<<4,0])
        adcout = ((r[1]&3) << 8) + r[2]
        return adcout
 
 #To read temperature and humidity
def readdht():
	sensor_args = { '11': Adafruit_DHT.DHT11,
					'22': Adafruit_DHT.DHT22,
					'2302': Adafruit_DHT.AM2302 }
	dht_sensor = sensor_args['22']
	humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
	return humidity, temperature

 
while 1:
        #Read channel
        ammonia = readadc(sen1)
        voc1 = readadc(sen2)
        voc2 = readadc(sen3)

        #Read humidity and temperature
        hum,temp = readdht()

        #Wait, do nothing for 5 seconds
        time.sleep(2000)

        #PLOT REGRESSION LINE
        #CALCULATE HYGEINE LEVEL
        #EXECUTE sprayOxi()
        #PLOT GRAPH & CALCULATE INTERPOLATION
        #SHOW THE DATA