# MyUAV

MyUAV is Autonomous Underwater Vehicle robot project. Based on Beaglebone black, 3 DC motors (one for diving, and 2 for
left/right forward movement), electronic compass + accelerator sensor, and pressure sensor.

Basic mission:
- dive until hitting bottom or depth is too deep
   - bump to bottom detected by the acceleration sensor of LSM303DLH 3-Axis Compass Accelerometer Module GY-51
   - depth detected by pressure sensor BMP805
- hover above bottom for defined time
- return to surface


