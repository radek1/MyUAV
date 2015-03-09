import Adafruit_BMP.BMP085 as BMP085
import time

def write_pressure():
    while True:
        print 'Temp = {0:0.2f} *C'.format(pressure_sensor.read_temperature())
        print 'Pressure = {0:0.2f} Pa'.format(pressure_sensor.read_pressure())
        print 'Altitude = {0:0.2f} m'.format(pressure_sensor.read_altitude())
        print 'Sealevel Pressure = {0:0.2f} Pa'.format(pressure_sensor.read_sealevel_pressure())
        time.sleep(.5)
    f = open("/home/ondra/python_code_ondra/test.txt","a")
    f.write(str(pressure_sensor.read_pressure())+"\n")
    f.close

def loop1():
    loop += 1
    seconds = 0
    write_pressure()
    
def loop2():
    loop = 0
    seconds = 0
    time.sleep(1)
    
def main():
    seconds = 0
    loop = 0
    interval = 1
    pressure_sensor = BMP085.BMP085()
    running = True
    print "%d \t %d" % (seconds,loop)
    time.sleep(1)
    seconds += 1
    if seconds == 20:
        loop1()
        time.sleep(20)
    if seconds == 20:
        loop1()
        time.sleep(20)
    if seconds == 20:
        loop1()
        time.sleep(20)
    if loop == 3:
        loop2()
        print "start"
    if seconds == 20:
        loop1()
        time.sleep(20)
    if seconds == 20:
        loop1()
        time.sleep(20)
    if seconds == 20:
        loop1()
        time.sleep(20)
    print "end"
main()






