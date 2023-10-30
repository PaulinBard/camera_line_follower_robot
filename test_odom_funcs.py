from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import controls as ctrl
import odom as odom


#### Tests on the direct_kinematics function:

class DirectKinematics:
    def __init__(self) -> None:
        pass

    def test(self):
        direct_kinematics_array = []

        # # Same speed on both sides positive
        # left_speed = 150
        # right_speed = 150
        # linear_speed, angular_speed = odom.direct_kinematics(left_speed, right_speed)
        # direct_kinematics_array.append((left_speed, right_speed, linear_speed, angular_speed))

        # # Same speed on both sides negative
        # left_speed = -150
        # right_speed = -150
        # linear_speed, angular_speed = odom.direct_kinematics(left_speed, right_speed)
        # direct_kinematics_array.append((left_speed, right_speed, linear_speed, angular_speed))

        # # Opposite speeds negative right
        # left_speed = 150
        # right_speed = -150
        # linear_speed, angular_speed = odom.direct_kinematics(left_speed, right_speed)
        # direct_kinematics_array.append((left_speed, right_speed, linear_speed, angular_speed))

        # # Opposite speeds negative left
        # left_speed = -150
        # right_speed = 150
        # linear_speed, angular_speed = odom.direct_kinematics(left_speed, right_speed)
        # direct_kinematics_array.append((left_speed, right_speed, linear_speed, angular_speed))

        # # Same direction with a small difference
        # left_speed = 150
        # right_speed = 130
        # linear_speed, angular_speed = odom.direct_kinematics(left_speed, right_speed)
        # direct_kinematics_array.append((left_speed, right_speed, linear_speed, angular_speed))

        # Same direction with a big difference
        left_speed = 30
        right_speed = 150
        linear_speed, angular_speed = odom.direct_kinematics(left_speed, right_speed)
        direct_kinematics_array.append((left_speed, right_speed, linear_speed, angular_speed))

        # # Opposite direction with a small difference
        # left_speed = -130
        # right_speed = 150
        # linear_speed, angular_speed = odom.direct_kinematics(left_speed, right_speed)
        # direct_kinematics_array.append((left_speed, right_speed, linear_speed, angular_speed))

        # # Opposite direction with a big difference
        # left_speed = 150
        # right_speed = -30
        # linear_speed, angular_speed = odom.direct_kinematics(left_speed, right_speed)
        # direct_kinematics_array.append((left_speed, right_speed, linear_speed, angular_speed))

        print("\nStart test_direct_kinematics_func:")
        for tuple in direct_kinematics_array:
            print("For left_speed =", round(tuple[0], 1), 
                  " and right_speed =", round(tuple[1], 1), 
                  "\n\twe have: linear_speed =", round(tuple[2], 1), 
                  " and angular_speed =", round(tuple[3], 1))
        print("End test_direct_kinematics_func.\n")

        return direct_kinematics_array


#### Tests on the odom function:

class Odom:
    def __init__(self) -> None:
        pass

    def test(slef, direct_kinematics_array):
        odom_array = []

        for tuple in direct_kinematics_array:
            linear_speed = tuple[2]
            angular_speed = tuple[3]
            dt = 0.5
            delta_x, delta_y, delta_theta = odom.odom(linear_speed, angular_speed, dt)
            odom_array.append((linear_speed, angular_speed, dt, delta_x, delta_y, delta_theta))

        print("\nStart test_odom_func:")
        for tuple in odom_array:
            print("For linear_speed =", round(tuple[0], 1), 
                  ", angular_speed =", round(tuple[1], 1), 
                  " and dt =", round(tuple[2], 1), 
                  "\n\twe have: delta_x =", round(tuple[3], 1), 
                  ", delta_y =", round(tuple[4], 1), 
                  " and delta_theta =", round(tuple[5], 1))
        print("End test_odom_func.\n")

        return odom_array
    

#### Tests on the tick_odom function:

class TickOdom:
    def __init__(self) -> None:
        pass

    def test(slef, direct_kinematics_array):
        tick_odom_array = []

        x = 0.0
        y = 0.0
        theta = 90.0

        for tuple in direct_kinematics_array:
            linear_speed = tuple[2]
            angular_speed = tuple[3]
            dt = 0.5
            new_x, new_y, new_theta = odom.tick_odom(x, y, theta, linear_speed, angular_speed, dt)
            tick_odom_array.append((x, y, theta, linear_speed, angular_speed, dt, new_x, new_y, new_theta))
            x = new_x
            y = new_y
            theta = new_theta

        print("\nStart test_tick_odom_func:")
        for tuple in tick_odom_array:
            print("For x =", round(tuple[0], 1), 
                  ", y =", round(tuple[1], 1), 
                  ", theta =", round(tuple[2], 1), 
                  ", linear_speed =", round(tuple[3], 1), 
                  ", angular_speed =", round(tuple[4], 1), 
                  " and dt =", round(tuple[5], 1), 
                  "\n\twe have: new_x =", round(tuple[6], 1), 
                  ", new_y =", round(tuple[7], 1), 
                  " and new_theta =", round(tuple[8], 1))
        print("End test_tick_odom_func.\n")

        return tick_odom_array
    


def plot_robot_position(x_start, y_start, theta_start, x_end, y_end, theta_end):
    # Create a figure and axis for the plot
    fig, ax = plt.subplots()

    # Plot the starting position and orientation of the robot
    ax.plot(x_start, y_start, 'ro', label='Start Position')
    ax.quiver(x_start, y_start, np.cos(np.radians(theta_start)), np.sin(np.radians(theta_start)), angles='xy', scale_units='xy', scale=0.01, color='r', label='Start Orientation')

    # Plot the ending position and orientation of the robot
    ax.plot(x_end, y_end, 'bo', label='End Position')
    ax.quiver(x_end, y_end, np.cos(np.radians(theta_end)), np.sin(np.radians(theta_end)), angles='xy', scale_units='xy', scale=0.01, color='b', label='End Orientation')

    # Set axis limits
    ax.set_xlim([-250, 250])
    ax.set_ylim([-250, 250])

    # Add labels and legend
    ax.set_xlabel('X Position (cm)')
    ax.set_ylabel('Y Position (cm)')
    ax.legend()

    # Show the plot
    plt.show()


print("Start test_odom_funcs:\n")

direct_kinematics_object = DirectKinematics()
direct_kinematics_array = direct_kinematics_object.test()

odom_object = Odom()
odom_array = odom_object.test(direct_kinematics_array)

tick_odom_object = TickOdom()
tick_odom_array = tick_odom_object.test(direct_kinematics_array)

test_number = 0
plot_robot_position(tick_odom_array[test_number][0], tick_odom_array[test_number][1], 
                    tick_odom_array[test_number][2], tick_odom_array[test_number][6], 
                    tick_odom_array[test_number][7], tick_odom_array[test_number][8])

print("End test_odom_funcs.\n")
