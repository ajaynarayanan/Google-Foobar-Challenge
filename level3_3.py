# Doomsday Fuel
# =============

# Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

# Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

# Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

# For example, consider the matrix m:
# [
#   [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
#   [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
#   [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
#   [0,0,0,0,0,0],  # s3 is terminal
#   [0,0,0,0,0,0],  # s4 is terminal
#   [0,0,0,0,0,0],  # s5 is terminal
# ]
# So, we can consider different paths to terminal states, such as:
# s0 -> s1 -> s3
# s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
# s0 -> s1 -> s0 -> s5
# Tracing the probabilities of each, we find that
# s2 has probability 0
# s3 has probability 3/14
# s4 has probability 1/7
# s5 has probability 9/14
# So, putting that together, and making a common denominator, gives an answer in the form of
# [s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
# [0, 3, 2, 9, 14].

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
# Solution.solution({{0, 2, 1, 0, 0}, {0, 0, 0, 3, 4}, {0, 0, 0, 0, 0}, {0, 0, 0, 0,0}, {0, 0, 0, 0, 0}})
# Output:
#     [7, 6, 8, 21]

# Input:
# Solution.solution({{0, 1, 0, 0, 0, 1}, {4, 0, 0, 3, 2, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
# Output:
#     [0, 3, 2, 9, 14]

# -- Python cases --
# Input:
# solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
# Output:
#     [7, 6, 8, 21]

# Input:
# solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
# Output:
#     [0, 3, 2, 9, 14]

# Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
from fractions import Fraction

def gcd(a,b): 
    # Computes greatest common divisor of two numbers a, b 
    if a == 0: 
        return b 
    return gcd(b % a, a) 
  
def transpose(a):
    # Assumes the matrix is square and transposes the matrix a
    a_t = [[0 for x in range(len(a))] for y in range(len(a[0]))]
    for i in range(len(a)):
        for j in range(len(a[i])):
             a_t[j][i] = a[i][j]

    return a_t

def minor(m,i,j):
    # Given a matrix m, returns the minor by excluding (i)th row and (j)th column
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def determinant(m):
    # Assumes the matrix is square and computes the determinant of a matrix m
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    det = 0
    for j in range(len(m)):
        det += ((-1)**j)*m[0][j]*determinant(minor(m,0,j))
    return det

def inverse(m):
    # Find the determinant of the square matrix
    det = determinant(m)
    if len(m) == 2:
        return [[m[1][1]/det, -1*m[0][1]/det],
                [-1*m[1][0]/det, m[0][0]/det]]

    # Find the cofactors matrix
    cofactors = []
    for i in range(len(m)):
        row = []
        for j in range(len(m)):
            minor_ij = minor(m,i,j)
            row.append(((-1)**(i+j)) * determinant(minor_ij))
        cofactors.append(row)

    # Find the adjoint matrix by transposing the cofactor matrix
    adjoint = transpose(cofactors)
    # m^(-1) = adjoint/determinant
    for i in range(len(adjoint)):
        for j in range(len(adjoint)):
            adjoint[i][j] = adjoint[i][j]/det
    return adjoint

def solution(m):
    # This question deals with absorbing markov chains 
    # The following steps are need to find out the terminal states probabilities 
    # 1. Find out the terminal states(T) and non-terminal(NT) states
    # 2. Arrange the matrix m in standard form 
    #       P = | I O | 
    #           | R Q | 
    #       where, I - Identity matrix of 'TxT' 
    #              O - Zero matrix of 'TxNT'
    #              R - Matrix of size 'NTxT'
    #              Q - Matrix of size 'NTxNT'
    # 3. Compute the matrix F = (I - Q)^(-1) of size (NTxNT)
    # 4. First row of (F*R) gives the required probabilities
    # The above computations will be easy with the help of external libraries for computing inverse, etc
    # Since, no external libraries are allowed, we need to code all matrix operations required 
    

    # When len(m) < 2 and given there is one terminal state, 
    # With probability 1, the terminal state is reached
    if len(m) < 2:
        return ([1,1])
    # Step 1, find out terminal and non-terminal states
    terminal_indices = []
    nonterminal_indices = []
    for index, row in enumerate(m) :
        if(sum(row) == 0):
            terminal_indices.append(index)
        else:
            nonterminal_indices.append(index)
    # Step 2. rearrange the matrix m in the form of P which has probabilities
    # Extract the matrices, R and Q in fraction format
    R, Q = [], []
    for index_nt in nonterminal_indices:
        row_R, row_Q = [], []
        for index, value in enumerate(m[index_nt]):
            if index in terminal_indices:
                row_R.append(Fraction(value, sum(m[index_nt])))
            else:
                row_Q.append(Fraction(value, sum(m[index_nt])))
        R.append(row_R)
        Q.append(row_Q)
    # Step 3, compute F = (I-Q)^(-1)
    I_minus_Q = []
    for index, row in enumerate(Q):
        row_iq = []
        for i in range(len(row)):
            if(i == index):
                row_iq.append(Fraction(1, 1) - row[i])
            else: 
                row_iq.append(-row[i])
        I_minus_Q.append(row_iq)
    # Compute inverse of I_minus_Q
    F = inverse(I_minus_Q)

    # Step 4, compute F*R 
    FR = [[0]*len(R[0]) for i in range(len(F))]
    for i in range(len(F)):
        for j in range(len(R[0])):
            total = 0
            for k in range(len(F[0])):
                total += F[i][k] * R[k][j]
            FR[i][j] = total
    # First row of FR gives us the result 
    result = FR[0]

    # Find LCM of all denominators and multiply FR[0] with it
    denom_lcm = result[0].denominator
    for value in result[1:]:
        denom_lcm = (denom_lcm * value.denominator)/gcd(denom_lcm, value.denominator)

    for i in range(len(result)):
        result[i] = result[i] * denom_lcm

    result = [value.numerator for value in result]
    result.append(denom_lcm)

    return result


resut = solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
print(resut)
