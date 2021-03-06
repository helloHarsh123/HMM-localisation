import random


class Sensor:
    # Settings for robot sensor.
    def __init__(self, grid):
        self.grid = grid

    L = 0.1
    L_s = 0.05
    L_s2 = 0.025

    def sense_location(self):
        """
        Uses sensor to detect current coordinates.
        :return: Tuple of coordinates based on sensing probabilities.
        """
        rand = random.random()
        if rand <= self.L:
            return self.grid.robot_location
        elif rand <= self.L + self.L_s * 8:
            return self.grid.robot_adj_location()
        elif rand <= self.L + self.L_s * 8 + self.L_s2 * 16:
            return self.grid.robot_adj2_location()
        else:
            return None

class Robot:
    def __init__(self, sensor, hmm):
        self.sensor = sensor
        self.x_guess, self.y_guess = 0, 0
        self.hmm = hmm

    def guess_move(self):
        sensed_location = self.sensor.sense_location()
        print "Sensor senses: ", sensed_location
        self.hmm.forward_step(sensed_location)
        guessed_move, probability = self.hmm.most_probable()
        print "Robot thinks it's in: ", guessed_move, " with probability: ", probability
        return guessed_move, probability


class Direction:
    NORTH, EAST, SOUTH, WEST = range(4)
    DIRS = [NORTH, EAST, SOUTH, WEST]

    def __init__(self):
        pass

    @classmethod
    def random(cls, exempt_dir=None):
        dirs = [cls.NORTH, cls.EAST, cls.SOUTH, cls.WEST]
        if exempt_dir:
            dirs.remove(exempt_dir)
            return dirs[random.randint(0, 2)]
        else:
            return dirs[random.randint(0, 3)]