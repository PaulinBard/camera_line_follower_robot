from pypot.dynamixel.io import DxlIO
import time
import controls as ctrl
import numpy as np
import odom

# Paramètres de communication
port = '/dev/ttyACM0'  # Port série de votre moteur
print("debut")
with DxlIO(port) as dxl_io:
    print("Debut du demarrage du go to\n")
    dxl_io.set_wheel_mode([1])
    dxl_io.set_wheel_mode([2])

    ctrl.stop(dxl_io)
    print("debut de la sequence de test du go to")
    v=200
    # dxl_io.set_moving_speed({1:-v})
    # dxl_io.set_moving_speed({2:v})
    dxl_io.disable_torque([1,2])
    dt = 200

    t0 = time.time()
    x = 0
    y = 0
    theta = 0
    while True:
        s1, s2 = dxl_io.get_present_speed([1,2])
        linear, angular = odom.direct_kinematics(np.pi * s2/180, np.pi * (-s1) /180)
        t1 = time.time()
        dt = t1-t0
        t0 = t1

        x, y, theta = odom.tick_odom(x,y,theta,linear, angular,dt)
        print(f"x = {x} y = {y} theta = {theta}")

#    ctrl.go_to(dxl_io, 40,80,180,90,20)
    # ctrl.stop(dxl_io)
    print("fin")
