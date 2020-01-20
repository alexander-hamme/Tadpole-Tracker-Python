from collections import deque
import math


class Animal:
    """
    Class to keep track of position and motion vectors.
    One Animal instance should be created for each animal to be tracked.
    """

    DEFAULT_BUFFER = 24  # corresponds to length of line trailing behind each tracked animal in graphic window

    def __init__(self, point, r, t):

        self.x, self.y = point

        self.position_bounds = (0, 0, 0, 0)


        self.radius = int(r)
        self.velocity_vector = (0, 0)
        self.accel_vector = (0, 0)
        self.jerk_vector = 0
        self.current_direction = 0
        self.line_points = deque(maxlen=self.DEFAULT_BUFFER)
        self.data_points = [(t, point, (0, 0), (0, 0), 0), ]  # time, position, velocity, accel, direction
        self.selection_index = 5  # buffer of previous data points to run calculations on

    def update_location(self, point, r, t):
        # update kinematics values and append new data points
        self.x, self.y = point

        self.calc_kinematics(point, t)

        self.data_points.append((t, (self.x, self.y), self.velocity_vector, self.accel_vector, self.current_direction))

        self.line_points.appendleft((int(point[0]), int(point[1])))


    def apply_pos_bounds(self):
        self.x = max(self.x, self.position_bounds[0])
        self.x = min(self.x, self.position_bounds[1])
        self.y = max(self.y, self.position_bounds[2])
        self.y = min(self.y, self.position_bounds[3])

