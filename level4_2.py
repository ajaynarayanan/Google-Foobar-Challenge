# Bringing a Gun to a Guard Fight
# ===============================

# Uh-oh - you've been cornered by one of Commander Lambdas elite guards! Fortunately, you grabbed a beam weapon from an abandoned guard post while you were running through the station, so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the elite guard: its beams reflect off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

# Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know that if a beam hits a corner, it will bounce back in exactly the same direction. And of course, if the beam hits either you or the guard, it will stop immediately (albeit painfully). 

# Write a function solution(dimensions, your_position, guard_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the guard's x and y coordinates in the room, and returns an integer of the number of distinct directions that you can fire to hit the elite guard, given the maximum distance that the beam can travel.

# The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite guard are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000.

# For example, if you and the elite guard were positioned in a room with dimensions [3, 2], your_position [1, 1], guard_position [2, 1], and a maximum shot distance of 4, you could shoot in seven different directions to hit the elite guard (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite guard with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting the elite guard with a total shot distance of sqrt(5).

# Languages
# =========

# To provide a Java solution, edit Solution.java
# To provide a Python solution, edit solution.py

# Test cases
# ==========
# Your code should pass the following test cases.
# Note that it may also be run against hidden test cases not shown here.

# -- Java cases --
# Input:
# Solution.solution([3,2], [1,1], [2,1], 4)
# Output:
#     7

# Input:
# Solution.solution([300,275], [150,150], [185,100], 500)
# Output:
#     9

# -- Python cases --
# Input:
# solution.solution([3,2], [1,1], [2,1], 4)
# Output:
#     7

# Input:
# solution.solution([300,275], [150,150], [185,100], 500)
# Output:
#     9

# Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.


import math    

def valid_points(dimension, x, distance):
    # Here, x refers to a coordinate
    # We know that the maximum number of valid mirror points in the grid will be (distance//dimension + 1) to either directions of point x
    
    points = []
    max_count = (distance//dimension + 1)
    count = 0
    point = x
    # Generate valid points to the left of x  
    while (count < max_count ):  
        if count % 2 == 1 :
            point -= 2*(dimension - x)
        else:
            point -= 2*(x)
        points.append(point)
        count += 1

    # Add the original point to the list of all possible points in the mirror grid
    points.append(x)
    # Generate points right of x
    point = x
    count = 0
    while (count < max_count ):  
        if count % 2 == 0 :
            point += 2*(dimension - x)
        else:
            point += 2*(x)
        points.append(point)
        count += 1
    return points

def grid_points(dimensions, position, distance):
    # Generate all mirror points in the gridworld for both the axes
    X = valid_points(dimensions[0], position[0], distance)
    Y = valid_points(dimensions[1], position[1], distance)
    points = []
    for x in X:
        for y in Y:
            points.append([x, y])
    return points

def solution(dimensions, your_position, guard_position, distance):
    # At first look, the challenge seems similar to a ray-tracing problem. 
    # It is difficult to find valid ways to shoot in a room if we try to solve this by reflection equations of the laser
    # A key insight is to reflect/mirror the persons instead of the lasers.
    # We construct an extended gridworld based on mirroring of the persons
    # and then calculate the number of ways to shoot lasers from starting position to any guard postion in the gridworld as long as we don't encounter ourselves in the path
    # A rough sketch of the solution is as follows
    # 
    # 1. Construct extended grid world by mirroring the persons inside the room.
    #           Insight 1.1) We know that the laser can mirror at most 'distance' times, this will allow us to limit the size of the gridworld
    #           Insight 1.2) We know that the mirroring a person twice sequentially in a given direction will give us the same result as the original scenario
    # 2. For every 'guard_position' in the extended gridworld, we need to find the direction/slope of that point and 'your_position' in the room
    # 3. While finding the direction we have make sure that no positions of ourselves are there in the path of ray.




    # Step 1, Find all possible points in the extended room/grid for both the positions
    your_positions = grid_points(dimensions, your_position, distance)
    guard_positions = grid_points(dimensions, guard_position, distance)
    

    # Step 2, find all possible directions/slopes 

    # Results keeps track of all possible valid ways to shoot laser from 'your_position' to 'guard_position'
    # slopes_distance is a dictionary to help in tracking the ways of not killing ourselves when we shoot in a given slope direction
    results = {}
    slopes_distance = {}
    for point in your_positions:
        # Find slope of every point the extended grid world of your_positions and your_position
        slope = math.atan2((your_position[1]-point[1]), (your_position[0]-point[0]))
        current_distance = ((point[0] - your_position[0])**2 + (point[1] - your_position[1])**2 )**0.5
        # If the distance between the point and 'your_position' is less than max distance, keep track of it as 
        # shooting along this direction might kill us instead of killing the guard
        if distance >= current_distance :
            # keep track of the smallest distance to a point in a given slope direction
            if((slope in slopes_distance and slopes_distance[slope] > current_distance) or slope not in slopes_distance ):
                slopes_distance[slope] = current_distance


    # Step 3, Make sure, we don't cross ourself in the directions found before
    for point in guard_positions:
        # Find slope of every point in the extended grid world of guard_positions and your_position
        slope = math.atan2((your_position[1]-point[1]), (your_position[0]-point[0]))
        current_distance = ((point[0] - your_position[0])**2 + (point[1] - your_position[1])**2 )**0.5
        # If the distance is less than max distance and, 
        # If it is also less than the distance between any point in 'your_position' of the extended gridworld to the your_position in the room
        # Then, shooting along this direction will kill the guard    
        if distance >= current_distance :
            if((slope in slopes_distance and slopes_distance[slope] > current_distance) or slope not in slopes_distance ):
                slopes_distance[slope] = current_distance
                results[slope] = True

    return len(results)

print(solution([3,2], [1,1], [2,1], 4))
print(solution([2,5], [1,2], [1,4], 11))
print(solution([300,275], [150,150], [185,100], 500))