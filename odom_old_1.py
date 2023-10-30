import math
import time
import controls as ctrl

# Constants
R = 2.6     # Wheel radius (cm)
L = 15.1    # Wheelbase (cm)

# Initial pose of the robot (x, y, theta)
x = 0.0
y = 0.0
theta = 90.0

def direct_kinematics(left_speed, right_speed):
    linear_speed = (R / 2) * (left_speed + right_speed)
    angular_speed = (R / L) * (right_speed - left_speed)
    return linear_speed, angular_speed

def odom(linear_speed, angular_speed, dt):
    global x, y, theta

    delta_x = linear_speed * math.cos(theta) * dt
    delta_y = linear_speed * math.sin(theta) * dt
    delta_theta = angular_speed * dt

    x += delta_x
    y += delta_y
    theta += delta_theta

    return delta_x, delta_y, delta_theta
 
def tick_odom(x_world, y_world, theta_world, linear_speed, angular_speed, dt):
    global x, y, theta

    # Update the robot's pose in the world frame
    x = x_world
    y = y_world
    theta = theta_world

    # Compute odometry values in the robot's frame
    delta_x_robot, delta_y_robot, delta_theta = odom(linear_speed, angular_speed, dt)

    # Rotate odometry values from the robot's frame to the world frame
    delta_x_world = delta_x_robot * math.cos(theta) - delta_y_robot * math.sin(theta)
    delta_y_world = delta_x_robot * math.sin(theta) + delta_y_robot * math.cos(theta)

    return x + delta_x_world, y + delta_y_world, theta + delta_theta


def get_linear_equation(x, y, x_target, y_target):
    a = -1
    b = -1
    if (x_target - x) != 0:
    	a = (y_target - y) / (x_target - x)
    	b = y - a*x
    return a, b

def get_ortogonal_projection(x, y, a, b):
    k = -1
    if (a*a + b) != 0:
       k = (y - a * x - b) / (a*a + b)
    return a*k + x, - b*k +y
    
    
    
def go_to_xya_odom(robot, x_target, y_target, theta_target, dt=0.5, xy_tolerance=3, theta_tolerance=10):
    global x, y, theta

    dir_angle = ctrl.get_direction_angle(x, y, theta, x_target, y_target)
    ctrl.rotation(robot, dir_angle)
    time.sleep(2)
    ctrl.go_forward(robot, 10)
    time.sleep(2)

    # Set the initial values (before calculating the real left_speed and right_speed)
    left_speed = robot.get_present_speed([ctrl.LEFT])
    left_speed = left_speed[0]
    right_speed = robot.get_present_speed([ctrl.RIGHT])
    right_speed = right_speed[0]
    linear_speed, angular_speed = direct_kinematics(left_speed, right_speed)
    print("angu ", angular_speed)
    angular_speed = 0.0
    print("first left_speed :", left_speed)
    print("first right_speed : ", right_speed)
    print("first linear : ", linear_speed)
    print("first angular : ", angular_speed)
    
    ctrl.go_forward(robot, linear_speed) # Go forward (with the linear speed)
    time.sleep(2)
    while True:
        # Calculate errors
        x_error = x_target - x
        y_error = y_target - y
        theta_error = theta_target - theta
        print("theta_error = ", theta_error, "\n")

        # Check if the robot reached the target pose within tolerances
        if abs(x_error) < xy_tolerance and abs(y_error) < xy_tolerance and abs(theta_error) < theta_tolerance:
            break  # Robot reached the target pose
        
        # Recalculate the left and right speeds
        left_speed = robot.get_present_speed([ctrl.LEFT])
        left_speed = left_speed[0]
        right_speed = robot.get_present_speed([ctrl.RIGHT])
        right_speed = right_speed[0]

        # Recalculate the linear and angular speeds
        linear_speed, angular_speed = direct_kinematics(left_speed, right_speed)
        print("linear : ", linear_speed)

        # Calculate the new position and orientation of the robot in the world frame
        new_x, new_y, new_theta = tick_odom(x, y, theta, linear_speed, angular_speed, dt)
        
        # Update the global robot variables
        x = new_x
        y = new_y
        theta = new_theta
        
        # Calculate the new angle for rotate
        if (theta_error > theta):
           dir_angle -= 5
        else:
           dir_angle += 5
        print("dir_angle end : ", dir_angle)

        #ctrl.rotation(robot, dir_angle) # Rotate
        ctrl.go_forward(robot, linear_speed) # Go forward
        
        time.sleep(dt)
        
    ctrl.stop(robot) # Stop the robot
    
    return x, y, theta  
    
    
    
# def go_to_xya_odom(robot, x_target, y_target, theta_target, dt=0.5, xy_tolerance=3, theta_tolerance=10):
#     global x, y, theta
    
#     # Set the initial values (before calculating the real left_speed and right_speed)
#     left_speed = get_present_speed(ctrl.LEFT)
#     right_speed = get_present_speed(ctrl.RIGHT)
#     linear_speed, angular_speed = direct_kinematics(left_speed, right_speed)
    
#     dir_angle = ctrl.get_direction_angle(0, 0, theta, x, y) # Calculate the initial angle to rotate to
#     ctrl.rotation(robot, dir_angle) # Rotate
#     ctrl.go_forward(robot, linear_speed) # Go forward (with the linear speed)

#     while True:
#         # Calculate errors
#         error_x = x_target - x
#         error_y = y_target - y
#         error_theta = theta_target - theta

#         # Check if the robot reached the target pose within tolerances
#         if abs(error_x) < xy_tolerance and abs(error_y) < xy_tolerance and abs(error_theta) < math.radians(theta_tolerance):
#             break  # Robot reached the target pose
        
#         # Recalculate the left and right speeds
#         left_speed = get_present_speed(ctrl.LEFT)
#         right_speed = get_present_speed(ctrl.RIGHT)
        
#         # Recalculate the linear and angular speeds
#         linear_speed, angular_speed = direct_kinematics(left_speed, right_speed)

#         # Calculate the new position and orientation of the robot in the world frame
#         new_x, new_y, new_theta = tick_odom(x, y, theta, linear_speed, angular_speed, dt)
        
#         # Calculate the new angle for rotate
#         dir_angle = - theta / dt
#         ctrl.rotation(robot, dir_angle) # Rotate
#         ctrl.go_forward(robot, linear_speed) # Go forward

#         # Update the global robot variables
#         x = new_x
#         y = new_y
#         theta = new_theta
        
#         time.sleep(dt)

        
#     ctrl.stop(robot) # Stop the robot
    
#     return x, y, theta    
    
    


# def go_to_xya_odom(x_target, y_target, theta_target, dt, xy_tolerance=3, theta_tolerance=10):
#     global x, y, theta
    
#     a, b = get_linear_equation(x, y, x_target, y_target)
    
#     dir_angle = get_direction_angle(x,y, theta, x_target, y_target) # Angle that the robot must rotate to go to target (straight line)
#     rotate(robot, dir_angle) # TO DO rotate ...
#     linear_speed = 3.0
#     angular_speed = 0.0
    
    
    
#     while True:
#         # Calculate the position and angle errors
#         x_error = x_target - x
#         y_error = y_target - y
#         theta_error = theta_target - theta
        
#         # Check if the robot is close enough to the target, if so, we stop
#         if abs(x_error) < xy_tolerance and abs(y_error) < xy_tolerance and abs(theta_error) < theta_tolerance:
#             break

#         delta_x, delta_y, delta_theta = tick_odom(x, y, theta, linear_speed, angular_speed, dt) # Future position if the robot continues with the same parameters

        
#         x_theoretical, y_theoretical = get_ortogonal_projection(x + delta_x, y + delta_y, a, b)
        
#         dx = abs(x_theoretical - (x + delta_x))
#         dy = abs(y_theoretical - (y + delta_y))
        
        
        
        
        
        
    
    
    
    
    
    
    
    
   





def inverse_kinematics(linear_speed, angular_speed):
    left_speed = (linear_speed - (L * angular_speed) / 2) / R
    right_speed = (linear_speed + (L * angular_speed) / 2) / R
    return left_speed, right_speed
