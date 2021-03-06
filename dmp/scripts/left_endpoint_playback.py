#!/usr/bin/env python
import rospy,sys
import argparse
import moveit_commander
import numpy as np
from geometry_msgs.msg import PoseStamped,Pose
from moveit_commander import MoveGroupCommander
import time
from copy import deepcopy
from os import path
class MoveItDemo:
	def __init__ (self):
		moveit_commander.roscpp_initialize(sys.argv)
		self.left_arm  = moveit_commander.MoveGroupCommander( 'left_arm')
		self.left_eef = self.left_arm.get_end_effector_link()
		self.left_arm.allow_replanning(True)
		self.left_arm.set_goal_position_tolerance(0.5)
		self.left_arm.set_goal_orientation_tolerance(0.5)
		self.left_arm.set_planning_time(5)
	def execute(self,filename):
		with open(filename, 'r') as f:
			lines = f.readlines()
		waypoints = []
		waypoints_l_start = []
		for idx, values in enumerate(lines[1:]):
			if idx==len(lines)-2:
				break
			values = values.rstrip().split(',')
			values = [float(x) for x in values]
			if idx == 0:
				start_pose = self.left_arm.get_current_pose(self.left_eef).pose
				wpose = deepcopy(start_pose)
				wpose.position.x = values[1]
				wpose.position.y= values[2]
				wpose.position.z = values[3]
				wpose.orientation.x = values[4]
				wpose.orientation.y = values[5]
				wpose.orientation.z = values[6]
				wpose.orientation.w = values[7]
				waypoints_l_start.append(deepcopy(start_pose))
				waypoints_l_start.append(deepcopy(wpose))
			wpose.position.x = values[1]
			wpose.position.y = values[2]
			wpose.position.z = values[3]
			wpose.orientation.x = values[4]
			wpose.orientation.y = values[5]
			wpose.orientation.z = values[6]
			wpose.orientation.w = values[7]
			waypoints.append(deepcopy(wpose))
		(cartesian_plan_l,fraction) = self.left_arm.compute_cartesian_path(waypoints_l_start,0.01, 0.0, True)
		self.left_arm.execute(cartesian_plan_l)
		rospy.sleep(1)
		print "***playback***\n"
		(cartesian_plan_l,fraction) = self.left_arm.compute_cartesian_path(waypoints,0.01, 0.0, True)
		self.left_arm.execute(cartesian_plan_l)
		rospy.sleep(1)
		print("Done.")
		moveit_commander.roscpp_shutdown()
		moveit_commander.os._exit(0)	
def main():
	print("Initializing node... ")
	rospy.init_node('moveit_demo')
	rospy.sleep(1)
	epilog = """
Related examples:
	joint_recorder.py; joint_position_file_playback.py.
	"""
	arg_fmt = argparse.RawDescriptionHelpFormatter
	parser = argparse.ArgumentParser(formatter_class=arg_fmt,
									description=main.__doc__,
									epilog=epilog)
	parser.add_argument(
	'-f', '--file', metavar='PATH', required=True,
	help='path to input file'
	)
	args = parser.parse_args(rospy.myargv()[1:])
	moveit = MoveItDemo()
	moveit.execute(path.expanduser(args.file))

if __name__ == "__main__":
	main()
