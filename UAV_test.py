import time
from pubsub import pub
from Adafruit_LSM303 import Adafruit_LSM303
import Adafruit_BMP.BMP085 as BMP085 
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import atexit

def exit_handler():
    print 'My UAV is stopping!'
    uav.stop_motor("M1")
    uav.stop_motor("MLeft")
    uav.stop_motor("MRight")
    PWM.cleanup()

    
class Listener():
    def onTopic1(self, msg, depth=None):
        pass
#        print 'depth: ',  msg + '= ',depth
#       if depth <= -10 and uav.get_motor_status("M1"):
#            uav.stop_motor("M1")
#        elif depth >= -8 and (uav.get_motor_status("M1") == False):            
#            uav.enable_motor("M1")

 
    def onTopic2(self, msg, acceleration = None):
        accZ = acceleration[2]   #acceleration component in z-axis
#       print 'acceleration: ', msg + '= ', accZ
#        if accZ > 1200:
#            uav.stop_motor("M1")
            
class MyUAV:
    motor_enabled = {'M1': False, 'MLeft': False, 'MRight': False}
    M1_EN = "P9_42"
    M1_IN1 = "P9_26"
    M1_IN2 = "P9_27"
    MLeft_EN = "P9_16"
    MLeft_IN1 = "P9_23"
    MLeft_IN2 = "P9_15"
    MRight_EN = "P9_14"
    MRight_IN1 = "P9_13"
    MRight_IN2 = "P9_12"

        
    def __init__(self):
        GPIO.setup(self.M1_IN1, GPIO.OUT)
        GPIO.setup(self.M1_IN2, GPIO.OUT)
        GPIO.setup(self.MLeft_IN1, GPIO.OUT)
        GPIO.setup(self.MLeft_IN2, GPIO.OUT)
        GPIO.setup(self.MRight_IN1, GPIO.OUT)
        GPIO.setup(self.MRight_IN2, GPIO.OUT)
        print("UAV __init__ has been executed!") 
        
    def enable_motor(self, motor = "M1", direction = "CW", duty_cycle = 75):
        if direction == "CW":
            try:
                GPIO.output(getattr(self, motor + "_IN1"), GPIO.HIGH)
                GPIO.output(getattr(self, motor + "_IN2"), GPIO.LOW)
                PWM.start(getattr(self, motor + "_EN"), duty_cycle) 
            except:
                print "Unexpected error:"
                raise
                sys.exit()
                
        else:
            try:         
                GPIO.output(getattr(self, motor + "_IN1"), GPIO.LOW)
                GPIO.output(getattr(self, motor + "_IN2"), GPIO.HIGH)
                PWM.start(getattr(self, motor + "_EN"), duty_cycle)
            except:
                print "Unexpected error:"
                raise
                sys.exit()                         
        print "motor ", motor, " enabled"
        self.motor_enabled[motor] = True
        
    def stop_motor(self, motor = "M1"):
        print "motor", motor, " stopped"
        PWM.stop(getattr(self, motor + "_EN"))        
        self.motor_enabled[motor] = False
        
    def get_motor_status(self, motor = "M1"):
        return self.motor_enabled[motor]
    
class Sensor:
    def __init__(self):
        print("class Sensor __init__ executed")

    def get_sensor_value(self):
        pass
        
class DepthSensor(Sensor):
    depth = 0
    call_count = 0
    def __init__(self):
        self.pressure_Sensor = BMP085.BMP085()
        print("depth sensor __init__ executed")
#        depth = 0
#        call_count = 0
        
    def get_sensor_value(self):
#        if uav.get_motor_status("M1"):
#            self.depth = -1*self.call_count
#            self.call_count += 1
#            #return(self.depth)
#        else: 
#            self.depth = -1*self.call_count
#            self.call_count -= 1
#            #return(self.depth)

        self.depth = self.pressure_Sensor.read_altitude()
        pub.sendMessage('topic1', msg='Depth ', depth=self.depth)
        return self.depth

class AccelerationSensor(Sensor):
    def __init__(self):
        self.lsm = Adafruit_LSM303()
        print("Acceleration sensor __init__ executed")
#        self.call_count = 0
        
    def get_sensor_value(self):
        self.acceleration = self.lsm.read()[0]
        pub.sendMessage('topic2', msg="Acceleration", acceleration = self.acceleration)
        return self.acceleration

    
uav = MyUAV()
depth_sensor = DepthSensor()
acceleration_sensor = AccelerationSensor()
listenerObj = Listener()
pub.subscribe(listenerObj.onTopic1, 'topic1')
pub.subscribe(listenerObj.onTopic2, 'topic2')
atexit.register(exit_handler)

def main():
    uav.enable_motor("M1", direction = "CW", duty_cycle = 100)
    while True:
        print depth_sensor.get_sensor_value()
        acc =  acceleration_sensor.get_sensor_value()[2]
        print acc #z-axis acceleration value
        if acc > 1200:
            uav.stop_motor("M1")
        time.sleep(0.5)
        
        
    
if __name__ == "__main__":
    main()
        
