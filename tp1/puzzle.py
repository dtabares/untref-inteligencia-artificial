#!/usr/bin/python

import sys
import math

def find_blank_pos(state):
    pos = 0
    for x in state:
        if x == '0':
            return pos
        pos += 1

def allowed_moves(pos):
    allowed_moves_list = ['up','down','right','left']

    #Checks if it's in first row and removes the up move
    if 0 <= pos <= (boundary -1):
        allowed_moves_list.remove('up')
    #Checks if it's in last row and removes the down move
    elif (initial_state_len - 1 - boundary) <= pos <= (initial_state_len -1):
        allowed_moves_list.remove('down')
    #Checks if it's in first col and removes the left move
    if pos in first_column:
        allowed_moves_list.remove('left')
    #Checks if it's in the last col and removes the right move
    elif pos in last_column:
        allowed_moves_list.remove('right')

    return allowed_moves_list

def column_ranges():
    first_column = list(range(0,initial_state_len - 1,boundary))
    last_column = list(range(boundary - 1,initial_state_len,boundary))
    return first_column, last_column
    

print ('input #:', str(len(sys.argv)))
print ('input #:', str(sys.argv))

if len(sys.argv) != 2:
    print ('Wrong number of arguments given ',str(len(sys.argv)),' expected 1')
    print ('Usage example: ', str(sys.argv[0]), ' 1,0,5,6,4,7,2,3,8')
    sys.exit(1)

initial_state = sys.argv[1].split(',')
initial_state_len = int(len(initial_state))
# With this I get if the matrix is 3x3 or 4x4 or even bigger
boundary = int(math.sqrt( initial_state_len ))

desired_state = []
# Sets the desired state
for x in range(0, initial_state_len):
    print ('value: ' + str(x))
    desired_state.append(str(x))

cost = 0
steps = []
evaluated_positions = 0

first_column, last_column = column_ranges()
