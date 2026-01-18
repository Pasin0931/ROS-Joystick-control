#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32MultiArray

# publisher
pub = rospy.Publisher('robot_cmd_vel', Float32MultiArray, queue_size=10)

# Speed
speed_factor = 0.5  # Start at 50%

def joy_callback(data):
    global speed_factor

    # Button indices
    L1 = data.buttons[4]  # Increase speed
    R1 = data.buttons[5]  # Decrease speed

    # Adjust speed
    if L1:
        speed_factor += 0.05
    if R1:
        speed_factor -= 0.05

    # Clamp speed factor
    speed_factor = max(0.1, min(speed_factor, 1.0))

    # Get joystick axes
    linear = data.axes[1] * speed_factor
    angular = data.axes[0] * speed_factor

    # Tank drive math
    left_motor_command = linear - angular
    right_motor_command = linear + angular

    # Clamp to valid range
    left_motor_command = max(min(left_motor_command, 1.0), -1.0)
    right_motor_command = max(min(right_motor_command, 1.0), -1.0)

    # Send command
    cmd_msg = Float32MultiArray()
    cmd_msg.data = [left_motor_command, right_motor_command]
    pub.publish(cmd_msg)

    rospy.loginfo("Speed: {:.2f} | Left: {:.2f} Right: {:.2f}".format(speed_factor, left_motor_command, right_motor_command))

def main():
    rospy.init_node('joy_teleop', anonymous=True)
    rospy.Subscriber("joy", Joy, joy_callback)
    rospy.spin()

if __name__ == '__main__':
    main()
