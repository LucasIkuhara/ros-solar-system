#!/usr/bin/env python  
import tf2_ros
import math
import rospy
import tf_conversions
import tf2_ros
import geometry_msgs.msg
import numpy as np

rospy.init_node("solar_system")
rate = rospy.Rate(50)

class SolarSystem:

    def __init__(self):
        self.broadcaster = tf2_ros.TransformBroadcaster()
        self.starName = "Sun"
        self.planets =  rospy.get_param("planets")



    def broadcastPlanet(self, time, planet):
        try:
            k = rospy.get_param("radiusConstant")
        except:
            k = 1
            
        trans = geometry_msgs.msg.TransformStamped()
        trans.header.stamp = rospy.Time.now()
        trans.header.frame_id = self.starName
        trans.child_frame_id = planet['name']
        trans.transform.translation.x = math.cos(time*(10 - planet['orbitRadius'])) * planet["orbitRadius"] * k
        trans.transform.translation.y = math.sin(time*(10 - planet['orbitRadius'])) * planet["orbitRadius"] * k
        trans.transform.translation.z = 0

        trans.transform.rotation.x = 0
        trans.transform.rotation.y = 0
        trans.transform.rotation.z = 0
        trans.transform.rotation.w = 1

        self.broadcaster.sendTransform(trans)


    def broadcastAllPlanets(self, time):
        for planet in self.planets:
            #rospy.loginfo(time)
            self.broadcastPlanet(time, planet)



mySolarSystem = SolarSystem()

while not rospy.is_shutdown():
    for time in np.arange(0, 2*math.pi, 0.001):
        mySolarSystem.broadcastAllPlanets(time)
        rate.sleep()

rospy.spin()