# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name:
# Collaborators (discussion):
# Time:

import math
import random
import statistics # to coompute the mean

import ps3_visualize
import pylab

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y      
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y  
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)
    def __str__(self):  
        return "(x,y)=(" + str(round(self.x,2 )) + "," + str(round(self.y,2))+")"

# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        width, height, dirt_amount = int(width), int(height), int(dirt_amount)

        if width <= 0 or height <= 0 or dirt_amount < 0:
            raise ValueError
        
        tiles={}
        for x in range(width):
            for y in range(height):
                tiles[(x,y)]=dirt_amount
        self.width = width
        self.height = height
        self.tiles = tiles
        self.dirt_amount=dirt_amount
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        
        x=math.floor(pos.get_x())
        y=math.floor(pos.get_y())
        tile=(x,y)
        old_dirt_amount=self.tiles[tile]
        if old_dirt_amount>=0:
            # new dirt amount cannot be negative
            new_dirt_amount=max(0,old_dirt_amount-capacity)
            self.tiles[tile]=new_dirt_amount  
    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        dirt_amount=self.tiles[(m,n)]
        return dirt_amount==0
    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        num_cleaned_tiles=0
        for tile_dirt in self.tiles.values():
            if tile_dirt==0:
                num_cleaned_tiles+=1
        return num_cleaned_tiles   
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        x=math.floor(pos.get_x())
        y=math.floor(pos.get_y())
        tile=(x,y)
        return tile in self.tiles        
    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        return self.tiles[(m, n)]        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # do not change -- implement in subclasses.
        raise NotImplementedError         
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and (in the case of FurnishedRoom) 
                 if position is unfurnished, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError         
    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        # do not change -- implement in subclasses
        raise NotImplementedError
    def __str__(self):  
        return "Tiles:dirt= " + str(self.tiles)

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot 
                  in a single time-step
        """
        capacity=int(capacity)
        
        if speed<=0 or capacity<0:
            raise ValueError

        initial_pos=room.get_random_position()
        initial_direction=random.uniform(0.0, 360.0)
        self.position=initial_pos
        self.direction=initial_direction
        self.room=room
        self.speed=speed
        self.capacity=capacity
    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position
    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction
    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position=position
    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        if isinstance(direction, float)==False:
            raise ValueError
        self.direction=direction
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark 
        the tile it is on as having been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class EmptyRoom(RectangularRoom):
    """
    An EmptyRoom represents a RectangularRoom with no furniture.
    """
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return len(self.tiles)
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        Returns: True if pos is in the room, False otherwise.
        """
        return self.is_position_in_room(pos)
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room).
        """
        x=random.uniform(0, self.width-1)
        y=random.uniform(0, self.height-1)
        return Position(x,y)
    def __str__(self):  
        return "Emptyroom= " + str(self.tiles)

class FurnishedRoom(RectangularRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.
    """
    def __init__(self, width, height, dirt_amount):
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        RectangularRoom.__init__(self, width, height, dirt_amount)
        # Call the __init__ method for the parent class
        # Adds the data structure to contain the list of furnished tiles
        self.furniture_tiles = []
    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored 
        as (x, y) tuples in the list furniture_tiles 
        
        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of furniture so that the entire piece of 
        furniture lies in the room.
        """
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.    
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles. Daniel's note: It does not recognize overlapped furniture
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))
        print(self.furniture_tiles)        
    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.
        """
        return (m,n) in self.furniture_tiles
    def is_position_furnished(self, pos):
        """
        pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        x=math.floor(pos.get_x())
        y=math.floor(pos.get_y())
        tile=(x,y)
        return tile in self.furniture_tiles
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
        x=math.floor(pos.get_x())
        y=math.floor(pos.get_y())
        tile=(x,y)
        return tile not in self.furniture_tiles and tile in self.tiles
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        valid_tiles=0
        for tile in self.tiles:
            if tile not in self.furniture_tiles:
                valid_tiles+=1
        return valid_tiles
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room and not in a furnished area).
        """
        #No valid tiles to generate random position
        if self.get_num_tiles()==0:
            print('There are not valid tiles')
            raise ValueError
        x=random.randint(0, self.width-1)
        y=random.randint(0, self.height-1)
        # print('random pos',x,y)
        if self.is_position_valid(Position(x,y)):
            return Position(x,y)
        else:
            # print('nao é valido',x,y)
            return self.get_random_position()
    def __str__(self):  
        return "FurnishedRoom. Tiles= " + str(self.tiles) + "Furnished tiles= "+str(self.furniture_tiles)

# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """
        # print(self.position, self.direction, self.speed)
        new_position=self.position.get_new_position(self.direction, self.speed)
        room=self.room
        if room.is_position_valid(new_position):
            self.position=new_position
            room.clean_tile_at_position(new_position, self.capacity)
        else:
            random_direction=random.uniform(0.0, 360.0)
            self.set_robot_direction(random_direction)


# Uncomment this line to see your implementation of StandardRobot in action!
# test_robot_movement(StandardRobot, EmptyRoom)
# test_robot_movement(StandardRobot, FurnishedRoom)

# === Problem 4
class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.
    """
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        """
        Sets the probability of getting faulty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob
    
    def gets_faulty(self):
        """
        Answers the question: Does this FaultyRobot get faulty at this timestep?
        A FaultyRobot gets faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the current tile and change its direction randomly.

        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        # print(self.position, self.direction, self.speed)
        new_position=self.position.get_new_position(self.direction, self.speed)
        room=self.room
        if room.is_position_valid(new_position) and self.gets_faulty()==False:
            # if self.gets_faulty()==False:
                # print('Robot Error')
            self.position=new_position
            room.clean_tile_at_position(new_position, self.capacity)
        else:
            random_direction=random.uniform(0.0, 360.0)
            self.set_robot_direction(random_direction)
        
    
# test_robot_movement(FaultyRobot, FurnishedRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                FaultyRobot)
    """
    tsteps_list=[]
    while num_trials>=0:
        room = EmptyRoom(width, height, dirt_amount)
        robots=[robot_type(room, speed, capacity)]*num_robots
        coverage = 0
        time_steps = 0
        # anim = ps3_visualize.RobotVisualization(1, 5, 5, [])  
        while coverage < min_coverage:
            time_steps += 1 
            for robot in robots:
                robot.update_position_and_clean()
                # anim.update(room, robots)
                coverage = float(room.get_num_cleaned_tiles())/room.get_num_tiles()        # anim.done()
        tsteps_list.append(time_steps)
        num_trials-=1
    return statistics.mean(tsteps_list)
 

# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
#  Asnwer: We can conclude by the first plot* that the time to clean 80% of the room is 
#  inversely proportional to the number of robots. The plot can be aproximated to
#  the function y=1/x. 
#  The second conclusion we can make is the FaultyRobot does not perform that
#  so bad comparing to the standardRobot, considering a squared room (on the next question
#  we will see a bigger gap). And difference between the performance of
#  the robot types decreases as the number of robots increases.
# 
#  *The plots were saved in path=PS3/Plots
# 
# 2) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
#   Asnwer: Here we can see that that the FaultyRobot performes relatively worst comparared
#   to the StandardRobot when the aspect ratio of the room increases.
# 
#   Overall conclusions: If you have a squared room, don't repair your Faulty iRobot. 
#   Consider buying another FaultyRobot, if you get a good price.
#



def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 17.5, 17.5, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 17.5, 17.5, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
# show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')
