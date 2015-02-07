import time
from pubsub import pub

    
class Listener():
    def onTopic1(self, msg, depth=None):
        print 'received: ',  msg + '= ',depth
        if depth <= -10 and uav.get_motor_status():
            uav.stop_motor()
        elif depth >= -8 and (uav.get_motor_status() == False):            
            uav.enable_motor()
 
    def onTopic2(self, msg, acceleration = None):
        #print 'received: ', msg + '= ', acceleration
        if acceleration > 100:
            uav.stop_motor()
            
class MyUAV:
    motor_enabled = False
    def __init__(self):
        print("UAV __init__ has been executed!") 
        
    def enable_motor(self):
        print("motor enabled")
        self.motor_enabled = True
        
    def stop_motor(self):
        print("motor stopped")
        self.motor_enabled = False
        
    def get_motor_status(self):
        return self.motor_enabled
    
class Sensor:
    def __init__(self):
        print("class Sensor __init__ executed")

    def get_sensor_value(self):
        pass
        
class DepthSensor(Sensor):
    depth = 0
    call_count = 0
    def __init__(self):
        print("depth sensor __init__ executed")
        depth = 0
        call_count = 0
        
    def get_sensor_value(self):
        if uav.motor_enabled:
            self.depth = -1*self.call_count
            self.call_count += 1
            #return(self.depth)
        else: 
            self.depth = -1*self.call_count
            self.call_count -= 1
            #return(self.depth)
        pub.sendMessage('topic1', msg='Depth ', depth=self.depth)
        

class AccelerationSensor(Sensor):
    def __init__(self):
        print("Acceleration sensor __init__ executed")
        self.call_count = 0
        
    def get_sensor_value(self):
        pub.sendMessage('topic2', msg="Acceleration", acceleration = 5)
        

    
uav = MyUAV()
depth_sensor = DepthSensor()
acceleration_sensor = AccelerationSensor()
listenerObj = Listener()
pub.subscribe(listenerObj.onTopic1, 'topic1')
pub.subscribe(listenerObj.onTopic2, 'topic2')

def main():
    uav.enable_motor()
    while True:
        depth_sensor.get_sensor_value()
        acceleration_sensor.get_sensor_value()
        time.sleep(0.5)
        
    
if __name__ == "__main__":
    main()
        
