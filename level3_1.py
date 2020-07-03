# Fuel Injection Perfection
# =========================

# Commander Lambda has asked for your help to refine the automatic quantum antimatter fuel injection system for her LAMBCHOP doomsday device. It's a great chance for you to get a closer look at the LAMBCHOP - and maybe sneak in a bit of sabotage while you're at it - so you took the job gladly. 

# Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort and shift the pellets down to a single pellet at a time. 

# The fuel control mechanisms have three operations: 

# 1) Add one fuel pellet
# 2) Remove one fuel pellet
# 3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)

# Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more pellets than you can express in that many digits.

# For example:
# solution(4) returns 2: 4 -> 2 -> 1
# solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1

# Languages
# =========

# To provide a Python solution, edit solution.py
# To provide a Java solution, edit Solution.java

# Test cases
# ==========
# Your code should pass the following test cases.
# Note that it may also be run against hidden test cases not shown here.

# -- Python cases --
# Input:
# solution.solution('15')
# Output:
#     5

# Input:
# solution.solution('4')
# Output:
#     2

# -- Java cases --
# Input:
# Solution.solution('4')
# Output:
#     2

# Input:
# Solution.solution('15')
# Output:
#     5

# Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.


# Trying out few cases to find any patterns
#  2 - div_2     
#  3 - sub 1
#  4 - div_2
#  5 - sub 1 
#  6 - div_2
#  7 - add 1 
#  8 - div_2
#  9 - sub 1
# 10 - div_2
# 11 - add 1 
# 12 - div_2
# 13 - sub 1
# 14 - div_2
# 15 - add 1
# 16 - div_2
# 17 - sub 1 
# 18 - div_2
# 19 - add 1
# starting from n = 4 , we can see the pattern 
# <div_2, sub 1, div_2, add 1> repeat 
# Choosing the operations can be done based on modulo operations
# count = 0
# Given an positive integer n, repeat the following till n = 1
#    if (n % 4 == 1), choose sub 1                 -> n = n - 1
#    elif(n % 4 == 0 or n % 4 == 2), choose div_2  -> n = n / 2
#    else, choose add 1                            -> n = n + 1
#    count += 1

def solution(n):
    n = int(n)
    count = 0
    while(n > 1):
        val = n % 4
        if(n == 3 or val == 1):
            n -= 1
        elif(val == 0 or val == 2):
            n /= 2
        else:
            n +=1 
        count += 1
    return count

                
for i in range(2, 21):
    print(i, solution(i))