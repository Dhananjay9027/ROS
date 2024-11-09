#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import time

def move_straight(velocity_publisher, speed, distance):
    vel_msg = Twist()
    vel_msg.linear.x = speed
    vel_msg.angular.z = 0.0
    start_time = rospy.Time.now().to_sec()
    current_distance = 0
    rate = rospy.Rate(10)

    while current_distance < distance:
        velocity_publisher.publish(vel_msg)
        current_time = rospy.Time.now().to_sec()
        current_distance = speed * (current_time - start_time)
        rate.sleep()
    
    # Stop after moving straight
    vel_msg.linear.x = 0
    velocity_publisher.publish(vel_msg)

def turn(velocity_publisher, angular_speed, angle):
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.angular.z = angular_speed
    start_time = rospy.Time.now().to_sec()
    current_angle = 0
    rate = rospy.Rate(10)

    while current_angle < angle:
        velocity_publisher.publish(vel_msg)
        current_time = rospy.Time.now().to_sec()
        current_angle = angular_speed * (current_time - start_time)
        rate.sleep()
    
    # Stop turning
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)

def move_rectangle():
    rospy.init_node('move_turtle_rectangle_node', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    
    length = 2.0  # Define length of the rectangle
    breadth = 2.0  # Define breadth of the rectangle
    speed = 1.0  # Define speed for straight movement
    angular_speed = 1.57  # Approximate angular speed for 90-degree turn (radians per second)
    angle = 1.57  # 90 degrees in radians

    for _ in range(2):  # Repeat twice for four sides
        move_straight(velocity_publisher, speed, length)
        turn(velocity_publisher, angular_speed, angle)
        move_straight(velocity_publisher, speed, breadth)
        turn(velocity_publisher, angular_speed, angle)

if __name__ == '__main__':
    try:
        move_rectangle()
    except rospy.ROSInterruptException:
        pass
