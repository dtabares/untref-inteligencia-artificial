#!/usr/bin/python

import sys
import math
from state import State

def solvable():
    initial_state_wo_zero = list(initial_state)
    initial_state_wo_zero.remove(0)
    number_of_inversions = 0
    for i in range(0,initial_state_len - 1):
        for j in range(i+1,initial_state_len - 1):
            if initial_state_wo_zero[i] > initial_state_wo_zero[j]:
                number_of_inversions += 1 

    blank_on_odd_row_from_bottom = False

    if math.floor((find_blank_pos(initial_state))/boundary)+1 %2 != 0:
        blank_on_odd_row_from_bottom = True
    
    #print('boundary even: ', boundary % 2  == 0)
    #print('blank_on_odd_row_from_bottom: ', blank_on_odd_row_from_bottom)
    #print('# of inversions: ', number_of_inversions)
    #print('row: ', math.floor((find_blank_pos(initial_state))/boundary)+1)

    #boundary is odd and there is an even number of inversions
    if boundary % 2  != 0 and number_of_inversions % 2 == 0:
        return True
    #boundary is even, 0 is on an odd row, counting from below, and the number of inversions is even
    elif boundary % 2  == 0 and blank_on_odd_row_from_bottom and  number_of_inversions % 2 == 0:
        return True
    else:
        return False

def solved_board_states_list(node):
    solved_board_states = []
    while node.parent is not None:
        solved_board_states.insert(0,node.state)
        node = node.parent
    solved_board_states.insert(0,initial_state)
    return solved_board_states

def print_results(node):
    print('BFS Cost: ',node.cost)
    move_list = node.move_list
    move_list_len = len(move_list)
    solved_board_states = solved_board_states_list(node)
    i = 0
    for board in solved_board_states:
        print('Board State: ', board)
        if(i < move_list_len):
            print('Move: ', move_list[i])
        i += 1


def find_blank_pos(state):
    return state.index(0)

def up(state, pos):
    new_state = list(state)
    new_state[pos] = new_state[pos - boundary]
    new_state[pos - boundary] = 0
    return new_state

def down(state, pos):
    new_state = list(state)
    new_state[pos] = new_state[pos + boundary]
    new_state[pos + boundary] = 0
    return new_state

def left(state, pos):
    new_state = list(state)
    new_state[pos] = new_state[pos - 1]
    new_state[pos - 1] = 0
    return new_state

def right(state, pos):
    new_state = list(state)
    new_state[pos] = new_state[pos + 1]
    new_state[pos + 1] = 0
    return new_state

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

def bfs(initial_state):

    print ('Starting BFS......')

    explored_states = []
    cost = 0
    frontier = [State(initial_state,None,cost,None)]

    if frontier[0].state == desired_state:
        return frontier[0]
    
    while frontier:
        current_node = frontier.pop(0)
        explored_states.append(current_node)
        cost += 1
        #print('cost so far: ', str(cost))
        #print('current node moves: ', str(current_node.move_list))
        blank_pos = find_blank_pos(current_node.state)
        for move in allowed_moves(blank_pos):
            #print('trying move: ', move)
            new_state = globals()[move](current_node.state,blank_pos)
            #print('child node state: ', str(new_state))
            new_moves_list = list(current_node.move_list)
            new_moves_list.append(move)
            #print('new move list: ', str(new_moves_list))
            child = State(new_state,current_node,cost,new_moves_list)
            
            if child not in (frontier or explored_states):
                if child.state == desired_state:
                    return child
                frontier.append(child)

if len(sys.argv) != 2:
    print ('Wrong number of arguments given ',str(len(sys.argv)),' expected 1')
    print ('Usage example: ', str(sys.argv[0]), ' 1,0,5,6,4,7,2,3,8')
    sys.exit(1)

initial_state = [ int(x) for x in sys.argv[1].split(',') ]
initial_state_len = int(len(initial_state))

# With this I get if the matrix is 3x3 or 4x4 or even bigger
boundary = int(math.sqrt( initial_state_len ))

# Sets the desired state
desired_state = list(range(0,initial_state_len))

#Calculates the positions of the most left/right columns which restric some moves
first_column, last_column = column_ranges()

if solvable():
    print_results(bfs(initial_state))
else:
    print ('Puzzle is not solvable')
    sys.exit(1)