import Adafruit_BMP.BMP085 as BMP085
import time

pressure_sensor = BMP085.BMP085()
while True:
    print 'Temp = {0:0.2f} *C'.format(pressure_sensor.read_temperature())
    print 'Pressure = {0:0.2f} Pa'.format(pressure_sensor.read_pressure())
    print 'Altitude = {0:0.2f} m'.format(pressure_sensor.read_altitude())
    print 'Sealevel Pressure = {0:0.2f} Pa'.format(pressure_sensor.read_sealevel_pressure())
    time.sleep (.5)




