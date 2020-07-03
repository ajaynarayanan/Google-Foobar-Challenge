# Expanding Nebula
# ================

# You've escaped Commander Lambda's exploding space station along with numerous escape pods full of bunnies. But - oh no! - one of the escape pods has flown into a nearby nebula, causing you to lose track of it. You start monitoring the nebula, but unfortunately, just a moment too late to find where the pod went. However, you do find that the gas of the steadily expanding nebula follows a simple pattern, meaning that you should be able to determine the previous state of the gas and narrow down where you might find the pod.

# From the scans of the nebula, you have found that it is very flat and distributed in distinct patches, so you can model it as a 2D grid. You find that the current existence of gas in a cell of the grid is determined exactly by its 4 nearby cells, specifically, (1) that cell, (2) the cell below it, (3) the cell to the right of it, and (4) the cell below and to the right of it. If, in the current state, exactly 1 of those 4 cells in the 2x2 block has gas, then it will also have gas in the next state. Otherwise, the cell will be empty in the next state.

# For example, let's say the previous state of the grid (p) was:
# .O..
# ..O.
# ...O
# O...

# To see how this grid will change to become the current grid (c) over the next time step, consider the 2x2 blocks of cells around each cell.  Of the 2x2 block of [p[0][0], p[0][1], p[1][0], p[1][1]], only p[0][1] has gas in it, which means this 2x2 block would become cell c[0][0] with gas in the next time step:
# .O -> O
# ..

# Likewise, in the next 2x2 block to the right consisting of [p[0][1], p[0][2], p[1][1], p[1][2]], two of the containing cells have gas, so in the next state of the grid, c[0][1] will NOT have gas:
# O. -> .
# .O

# Following this pattern to its conclusion, from the previous state p, the current state of the grid c will be:
# O.O
# .O.
# O.O

# Note that the resulting output will have 1 fewer row and column, since the bottom and rightmost cells do not have a cell below and to the right of them, respectively.

# Write a function solution(g) where g is an array of array of bools saying whether there is gas in each cell (the current scan of the nebula), and return an int with the number of possible previous states that could have resulted in that grid after 1 time step.  For instance, if the function were given the current state c above, it would deduce that the possible previous states were p (given above) as well as its horizontal and vertical reflections, and would return 4. The width of the grid will be between 3 and 50 inclusive, and the height of the grid will be between 3 and 9 inclusive.  The answer will always be less than one billion (10^9).

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
# Solution.solution({{true, true, false, true, false, true, false, true, true, false}, {true, true, false, false, false, false, true, true, true, false}, {true, true, false, false, false, false, false, false, false, true}, {false, true, false, false, false, false, true, true, false, false}})
# Output:
#     11567

# Input:
# Solution.solution({{true, false, true}, {false, true, false}, {true, false, true}})
# Output:
#     4

# Input:
# Solution.solution({{true, false, true, false, false, true, true, true}, {true, false, true, false, false, false, true, false}, {true, true, true, false, false, false, true, false}, {true, false, true, false, false, false, true, false}, {true, false, true, false, false, true, true, true}}
# Output:
#     254

# -- Python cases --
# Input:
# solution.solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]])
# Output:
#     11567

# Input:
# solution.solution([[True, False, True], [False, True, False], [True, False, True]])
# Output:
#     4

# Input:
# solution.solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]])
# Output:
#     254

# Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.


def check(previous_state, i, j, ij_value, current_state):
    # Given the current state, previous_state, indices (i, j) and previous_state[i][j] as ij_value 
    # this function checks whether current_state[i-1][j-1] is possible from the given configuration of previous_state and ij_value by following the CA rule 
    count = (
        previous_state[i][j - 1]
        + previous_state[i - 1][j]
        + previous_state[i - 1][j - 1]
        + ij_value
    )
    val = count == 1
    return val == current_state[i - 1][j - 1]


def generate_states(current_state, i, j, previous_state, dp, history):
    n = len(current_state)
    m = len(current_state[0])
    # Base case
    if j == m + 1:
        return 1

    valid_entries = 0
    
    # If we have already encountered this configuration, look it up from DP table/dictionary 
    index = ((i, j), tuple(history[-(n + 2):]))
    if index in dp:
        return dp[index]

    # Assign True to previous_state[i][j] if it satsifies the Cellular Automata rule and then recurse 
    if (i == 0 or j == 0) or check(previous_state, i, j, True, current_state):
        previous_state[i][j] = True
        history.append(True)
        valid_entries += generate_states(
            current_state,
            i=(i + 1) % (n + 1),
            j=j + (i + 1) // (n + 1),
            previous_state=previous_state,
            dp=dp,
            history=history,
        )
        history.pop()

    # Assign False to previous_state[i][j] if it satsifies the Cellular Automata rule and recurse
    if (i == 0 or j == 0) or check(previous_state, i, j, False, current_state):
        previous_state[i][j] = False
        history.append(False)
        valid_entries += generate_states(
            current_state,
            i=(i + 1) % (n + 1),
            j=j + (i + 1) // (n + 1),
            previous_state=previous_state,
            dp=dp,
            history=history,
        )
        history.pop()

    # Store the number of valid_entries possible from this point in the DP table/dictionary
    dp[index] = valid_entries

    return valid_entries

def solution(g):
    # With the recent demise of the famous mathematician - Dr. John Conway, I came across few articles discussing his renowned work - 'Game of Life' under Cellular Automata. 
    # The given problem comes under Cellular Automata(CA) and it asks about the number of preimages given a current image/state.
    # Let (n, m) be the dimensions of current_state. We know that previous_state has the dimensions - (n+1, m+1)
    # Finding a valid previous state can be done column by column, starting at column zero of current state
    # Each column (say c(i) of size (mx1)) of the current state maps into different possible previous_states of size (mx2). Let p(c(i)) denote one such valid previous_state instance. 
    # Considering two adjacent column in current state (c(i) and c(i+1)), we can see that for a valid configuration of previous state from both the columns, we need p(c(i))'s second column and p(c(i+1))'s first column to match
    # Thus, there are overlapping sub-problems and we can solve this by recursion + memoization.       
    # 
    # A quick overview of the solution is as follows,
    # Given i = 0, j = 0 and previous_state initalized with random values, consider the following recursive function
    #       1) Base case : If we have reached last column in previous_state, then return 1 as the count of all further possible configurations from this configuration 
    #       2) If we have encountered this state before, look up the DP table for count of all possible states from this state
    #       3) Assign True to previous_state[i][j] if it satsifies the Cellular Automata rule and then recurse to find other configurations from the current configuration by incrementing i and j appropriately
    #       4) Assign False to previous_state[i][j] if it satsifies the Cellular Automata rule and recurse to find other configurations from the current configuration by incrementing i and j appropriately
    #       5) Store the value of the current configuration in the DP table for look up

    # Get the current state's dimensions
    # g, the current state has dimensions of (n*m)
    n = len(g)
    m = len(g[0])
    # Previous state dimensions are (n+1)*(m+1)
    previous_state = [[True] * (m + 1) for i in range(n + 1)]
    # Memoization/Look up variables
    history = []
    dp = {}
    return generate_states(g, 0, 0, previous_state, dp, history)
    
# print(answer([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]]))
g = [[True, False, True], [False, True, False], [True, False, True]]
print(solution(g))
# p = [[False, True, False, False], [False, False, True, False], [False, False, False, True], [True, False, False, False]]
# p = [j for x in p  for j in x ]
# print(check(p, g))

# def check(p, c):
#     """
#         p is a 1D array of size ((n+1)*(m+1)) representing previous state
#         c is a 2D matrix of size (n)*(m) representing current state
#     """
#     n = len(c)
#     m = len(c[0])
#     # print(p)
#     for i in range(n):
#         for j in range(m):
#             count = (
#                 int(p[i * (m + 1) + j])
#                 + int(p[i * (m + 1) + j + 1])
#                 + int(p[(i + 1) * (m + 1) + j])
#                 + int(p[(i + 1) * (m + 1) + j + 1])
#             )
#             if count == 1:
#                 value = True
#             else:
#                 value = False
#             if value != c[i][j]:
#                 return False

#     return True


# def bruteforce(g):
#     # Brute force
#     # Current state's dimensions
#     n = len(g)
#     m = len(g[0])
#     count = 0
#     # Previous state's dimensions
#     p_dims = (n + 1) * (m + 1)
#     i = 0
#     while i <= 2 ** p_dims:
#         p = "{:0{}b}".format(i, p_dims)
#         if check(p, g):
#             # print("yes")
#             count += 1
#         i += 1
#     return count

