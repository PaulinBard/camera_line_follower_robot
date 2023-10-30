from pypot.dynamixel.io import DxlIO
from time import sleep
import controls as ctrl
import odom as odom

# Paramètres de communication
port = '/dev/ttyACM0'  # Port série de votre moteur
print("debut")
with DxlIO(port) as dxl_io:
    print("Debut du demarrage du go to\n")
    dxl_io.set_wheel_mode([1])
    dxl_io.set_wheel_mode([2])

    ctrl.stop(dxl_io)
    print("debut de la sequence de test du go to")
    odom.go_to_xya_odom(dxl_io,0,80,90)
    
    
    # ctrl.go_forward(dxl_io, 10)
    # sleep(2)
    
    # left_angular_speed = dxl_io.get_present_speed([ctrl.LEFT]) # °/s
    # left_angular_speed = left_angular_speed[0]
    # right_angular_speed = dxl_io.get_present_speed([ctrl.RIGHT]) # °/s
    # right_angular_speed = -right_angular_speed[0]
    
    # left_speed_end = ctrl.get_speed_from_rod(left_angular_speed)
    # right_speed_end = ctrl.get_speed_from_rod(right_angular_speed)
    # print("left_angular_speed =", left_angular_speed, " left_speed_end =", left_speed_end)
    # print("right_angular_speed =", right_angular_speed, " right_speed_end =", right_speed_end)
    
    # ctrl.stop(dxl_io)
    
    print("fin")
