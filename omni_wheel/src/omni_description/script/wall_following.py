#! /usr/bin/env python3

# import ROS packages
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# Define global variables
regions_ = {
    'right': 0,
    'front': 0,
    'left': 0,
}
robo_sta = 0
state_ = 0
state_dict_ = {
    0: 'find the wall',
    1: 'turn left',
    2: 'turn right',
    3: 'back',
    4: 'follow the wall',
}

pub_ = None

def callback_laser(msg):
    global regions_
    front_min_list = []
    left_min_list = []
    right_min_list = []
    ranges = msg.ranges
    radar_len = len(ranges)
    front_list = ranges[int(345 * radar_len / 360):radar_len] + ranges[0:int(15 * radar_len / 360)]
    left_list = ranges[int(70 * radar_len / 360):int(90 * radar_len / 360)]
    right_list = ranges[int(270 * radar_len / 360):int(290 * radar_len / 360)]
    
    for i in range(len(front_list)):
        if front_list[i] != 0:
            front_min_list.append(front_list[i])
    front_min = min(front_min_list)

    for i in range(len(left_list)):
        if left_list[i] != 0:
            left_min_list.append(left_list[i])
    left_min = min(left_min_list)

    for i in range(len(right_list)):
        if right_list[i] != 0:
            right_min_list.append(right_list[i])
    right_min = min(right_min_list)

    regions_ = {
        'left': left_min,
        'front': front_min,
        'right': right_min,
    }

    take_action()

def change_state(state):
    global robo_sta, regions_
    if state == 0:
        regions_['right'], regions_['left'] = d + 0.2, d + 0.2
    if state == 1:
        regions_['right'] = d + 0.2
        robo_sta = 1  # following right wall
    elif state == 3:
        regions_['front'] = d + 0.2
    elif state == 2:
        regions_['left'] = d + 0.2
        robo_state = 2  # following left wall
    elif state == 4 and robo_sta == 1:
        regions_['right'] = d + 0.2
        robo_sta = 1
    elif state == 4 and robo_sta == 2:
        regions_['left'] = d + 0.2
        robo_sta = 2

    global state_, state_dict_
    if state != state_:
        print('Wall follower - [%s] - %s' % (state, state_dict_[state]))
        state_ = state

def take_action():
    global regions_
    regions = regions_

    msg = Twist()

    state_description = ''
    global d
    d = 1.5

    if regions['front'] > d:
        state_description = 'case 1 - nothing'
        change_state(0)
    elif regions['front'] < d and regions['left'] > d and regions['right'] > d:
        state_description = 'case 2 - front'
        change_state(1)
    elif regions['front'] > d and regions['left'] > d and regions['right'] < d:
        state_description = 'case 3 - fright'
        change_state(4)
    elif regions['front'] > d and regions['left'] < d and regions['right'] > d:
        state_description = 'case 4 - fleft'
        change_state(4)
    elif regions['front'] < d and regions['left'] > d and regions['right'] < d:
        state_description = 'case 5 - front and fright'
        change_state(1)
    elif regions['front'] < d and regions['left'] < d and regions['right'] > d:
        state_description = 'case 6 - front and fleft'
        change_state(2)
    elif regions['front'] < d and regions['left'] < d and regions['right'] < d:
        state_description = 'case 7 - front and fleft and fright'
        change_state(3)
    elif regions['front'] > d and regions['left'] < d and regions['right'] < d:
        state_description = 'case 8 - fleft and fright'
        change_state(4)
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

    # Additional condition to handle the transition between rooms
    if state_ == 4 and robo_sta == 1 and regions_['right'] > 2 * d:
        change_state(2)
    elif state_ == 4 and robo_sta == 2 and regions_['left'] > 2 * d:
        change_state(1)

def find_wall():
    msg = Twist()
    msg.linear.x = 0.0
    msg.angular.z = -0.8
    return msg

def turn_left():
    msg = Twist()
    msg.linear.x = -1.5
    msg.angular.z = 0.0
    return msg

def turn_right():
    msg = Twist()
    msg.linear.x = 1.5
    msg.angular.z = 0.0
    return msg

def back():
    msg = Twist()
    msg.linear.x = 0.0
    msg.angular.z = 1.5
    return msg

def follow_the_wall():
    msg = Twist()
    msg.linear.x = -1.5
    return msg

def main():
    global pub_

    rospy.init_node('reading_laser')
    pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    sub = rospy.Subscriber('/scan', LaserScan, callback_laser, queue_size=1)

    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        msg = Twist()

        if state_ == 0:
            msg = find_wall()
        elif state_ == 1:
            msg = turn_left()
        elif state_ == 2:
            msg = turn_right()
        elif state_ == 3:
            msg = back()
        elif state_ == 4:
            msg = follow_the_wall()

        pub_.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    main()