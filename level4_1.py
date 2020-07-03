# Escape Pods
# ===========

# You've blown up the LAMBCHOP doomsday device and broken the bunnies out of Lambda's prison - and now you need to escape from the space station as quickly and as orderly as possible! The bunnies have all gathered in various locations throughout the station, and need to make their way towards the seemingly endless amount of escape pods positioned in other parts of the station. You need to get the numerous bunnies through the various rooms to the escape pods. Unfortunately, the corridors between the rooms can only fit so many bunnies at a time. What's more, many of the corridors were resized to accommodate the LAMBCHOP, so they vary in how many bunnies can move through them at a time. 

# Given the starting room numbers of the groups of bunnies, the room numbers of the escape pods, and how many bunnies can fit through at a time in each direction of every corridor in between, figure out how many bunnies can safely make it to the escape pods at a time at peak.

# Write a function solution(entrances, exits, path) that takes an array of integers denoting where the groups of gathered bunnies are, an array of integers denoting where the escape pods are located, and an array of an array of integers of the corridors, returning the total number of bunnies that can get through at each time step as an int. The entrances and exits are disjoint and thus will never overlap. The path element path[A][B] = C describes that the corridor going from A to B can fit C bunnies at each time step.  There are at most 50 rooms connected by the corridors and at most 2000000 bunnies that will fit at a time.

# For example, if you have:
# entrances = [0, 1]
# exits = [4, 5]
# path = [
#   [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
#   [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
#   [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
#   [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
#   [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
#   [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
# ]

# Then in each time step, the following might happen:
# 0 sends 4/4 bunnies to 2 and 6/6 bunnies to 3
# 1 sends 4/5 bunnies to 2 and 2/2 bunnies to 3
# 2 sends 4/4 bunnies to 4 and 4/4 bunnies to 5
# 3 sends 4/6 bunnies to 4 and 4/6 bunnies to 5

# So, in total, 16 bunnies could make it to the escape pods at 4 and 5 at each time step.  (Note that in this example, room 3 could have sent any variation of 8 bunnies to 4 and 5, such as 2/6 and 6/6, but the final solution remains the same.)

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
# Solution.solution({0, 1}, {4, 5}, {{0, 0, 4, 6, 0, 0}, {0, 0, 5, 2, 0, 0}, {0, 0, 0, 0, 4, 4}, {0, 0, 0, 0, 6, 6}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
# Output:
#     16

# Input:
# Solution.solution({0}, {3}, {{0, 7, 0, 0}, {0, 0, 6, 0}, {0, 0, 0, 8}, {9, 0, 0, 0}})
# Output:
#     6

# -- Python cases --
# Input:
# solution.solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])
# Output:
#     6

# Input:
# solution.solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
# Output:
#     16

# Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.

def bfs(R, source, targets, parent):
    # Standard breadth-first search(bfs) implementation with parent array for keeping track of path
    # R represents residual graph
    visited = [source]
    queue = [source]
  
    while (queue):
        # Pop out the first node in the queue 
        u = queue.pop(0) 
        for v in range(len(R)):
            if (not(v in visited) and R[u][v] > 0):
                queue.append(v)
                parent[v] = u
                visited.append(v)

    # If any vertex in visited is part of targets then return that vertex as there is an augmenting path from source to that vertex
    for vertex in visited:
        if vertex in targets:
            return vertex
    return -1

def solution(entrances, exits, path):
    # The given problem is same as finding maximum flow in a graph with multiple sources and multiple sinks
    # Let us first look at Ford-Fulkerson algorithm for solving single source and single sink maximum flow problem and extend it to our problem
    # Given a graph(V,E) with source vertex - 's', sink vertex - 't' and capacity matrix - C[u][v] representing maximum flow value in the edge (u,v) 
    # 1. Start with max_flow = 0, Residual matrix (R) = C
    # 2. Repeat untill no augmenting path from any source(S) to any target/sink(T) can be found. An augmenting path is a simple path from s to t which uses only postivie capacity edges 
    #       2.1 Use DFS/BFS to find an augmented path from s to t, say 'p' 
    #       2.2 Find 'f' - the minimum flow value in the path p 
    #       2.3 max_flow = max_flow + f
    #       2.4 For each edge (u,v) in path p,
    #               2.4.1 R[u][v] = R[u][v] - f
    #               2.4.2 R[v][u] = R[v][u] - f
    # 3. max_flow represents the maximum flow possible from s to t
    # Extending the above solution to multiple sources and multiple sinks by considering augmenting paths from any source node to any sink node. 

    # Step 1, Initalize max_flow to 0 and Residual matrix/graph(R) to Capacity matrix (paths) 
    # In our problem, max_flow will represent the total number of bunnies that can get through at each time step
    max_flow = 0        
    R = path[:]
    # Parent array to keep track of augmenting path 
    parent = [-1]*len(R)


    # Step 2, find any augmenting path, update max_flow and residual graph
    while True:
        # Variable for checking exit condition
        flag = 0

        # Check for an augmenting path starting from any entrances/source vertex - 'source' to any vertex 'target' in sinks/exits 
        for source in entrances:
            target = bfs(R, source, exits, parent)
            # Augmenting path exists from source to target 
            if target != -1:
                # Step 2.2
                # Find minimum flow value in the above path
                f = 2000000
                node = target
                while(node != source):
                    f = min(R[parent[node]][node], f)
                    node = parent[node]

                # Step 2.3
                # Update value of max_flow
                max_flow += f 

                # Step 2.4
                # Update Residual graph's values 
                node = target
                while(node != source):
                    R[parent[node]][node] -= f
                    R[node][parent[node]] += f
                    node = parent[node]

            else:
                flag += 1
        # If no augmenting path exists from any 'source' in sources/entrances to any 'target' in targets/exits, we have found the maximum flow  
        if flag == len(entrances):
            break

    # Step 3, max_flow now has the maximum flow value for the problem 
    return max_flow


print(solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
print(solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]]))