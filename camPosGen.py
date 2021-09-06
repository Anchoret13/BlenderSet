# CAMERA POSITION FOR CAMERA LOADER

'''
Input center radius look_at_point
output location rotation
'''
import os
import argparse

import numpy as np


parser = argparse.ArgumentParser(description='camera pose')
parser.add_argument('number', type=int, help='number')
parser.add_argument('height', type=float, help='height')
parser.add_argument('radius', type=float, help='radius')
args = parser.parse_args()

center = [0, 0, args.height]
object_position = [0, 0, 0]
theta = np.arange(0, 2*np.pi, 2*np.pi/args.number)
r = args.radius

a, b = (0., 0.)

x = a + r * np.cos(theta)
y = b + r * np.sin(theta)

posList = []

for i in range(args.number):
    posList.append([x[i], y[i], args.height, object_position[0], object_position[1],object_position[2]])

postList = np.array(posList)
np.savetxt("camPose", postList)