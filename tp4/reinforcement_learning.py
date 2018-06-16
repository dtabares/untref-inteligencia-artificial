#!/usr/bin/python

from tkinter import Tk, Canvas, Frame, BOTH
import random
import numpy as np
from move_memory import MoveMememory

#Allowed moves in the board
moves = ['UP','LEFT','RIGHT','DOWN']
oposite_moves = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT','RIGHT': 'LEFT'}
#Number of iterations for training
iterations = 1
#Drawing stuff
rectangles = []
rectangle_h = 50
rectangle_w = 50
x1 = None
x2 = None
#World size
grid_size_x = 10
grid_size_y = 3
# World rewards (will be filled when world is created)
rewards = []
#Training stuff
number_of_moves = 0
score = 0
start_position = 0
end_position = grid_size_x - 1
end_flag = False
q_table = np.zeros((grid_size_x * grid_size_y, len(moves), 1))

#Needed for world moves and actions
fringe_left_values = []
fringe_right_values = []
for i in range(grid_size_y):
  fringe_left_values.append(grid_size_x * i)
  fringe_right_values.append((grid_size_x * i) + grid_size_x - 1)


def draw_x(x,y):
  canvas.delete(x1)
  canvas.delete(x2)
  x1 = canvas.create_line(x, y, x + rectangle_w, y + rectangle_h)
  x2 = canvas.create_line(x + rectangle_w, y, x, y + rectangle_h)

def random_move():
  intended_direction = random.choice(moves)
  move_list, probabilities = probabilities_for_a_move(intended_direction)
  actual_direction = np.random.choice(move_list,1,p=probabilities)
  return actual_direction

def probabilities_for_a_move(intended_direction):
  moves_with_probabilities = {'UP': 0.1, 'DOWN':0.1, 'LEFT': 0.1,'RIGHT': 0.1}
  moves_with_probabilities[intended_direction] = 0.8
  moves_with_probabilities[oposite_moves[intended_direction]] = 0
  k = list(moves_with_probabilities.keys())
  v = list(moves_with_probabilities.values())
  return k,v

def calculate_new_pos_and_reward(actual_pos,direction):
  if (direction == 'UP'):
    if (actual_pos < grid_size_x):
      new_pos = actual_pos
    else:
      new_pos = actual_pos - 10
  elif (direction == 'DOWN'):
    if (actual_pos > ((grid_size_x * 2 ) -1) ):
      new_pos = actual_pos
    else:
      new_pos = actual_pos + 10
  elif (direction == 'LEFT'):
    if actual_pos in fringe_left_values:
      new_pos = actual_pos
    else:
      new_pos = actual_pos - 1
  else:
    if actual_pos in fringe_right_values:
      new_pos = actual_pos
    else:
      new_pos = actual_pos + 1
  return new_pos, rewards[new_pos]

def move(actual_pos):
  direction = random_move()
  print("direction: ", direction)
  new_pos, reward = calculate_new_pos_and_reward(actual_pos,direction)
  global score, end_flag
  score = score + reward
  global number_of_moves
  number_of_moves = number_of_moves + 1
  if (new_pos == end_position):
    end_flag = True
  return new_pos
  

def learn():
  for x in range(iterations):
    global score
    score = 0
    global number_of_moves
    number_of_moves = 0
    pos = start_position
    while (end_flag == False):
      print("pos: ", pos)
      print("score:", score)
      print("number_of_moves",number_of_moves)
      pos = move(pos)

# Define la ventana principal de la aplicación
root = Tk()
# Define las dimensiones de la ventana, que se ubicará en 
# el centro de la pantalla. Si se omite esta línea la
# ventana se adaptará a los widgets que se coloquen en
# ella. 
root.geometry("800x250+300+300")
root.title("UNTREF - IA - TP 4") 
canvas = Canvas(root)
for y in range(1, grid_size_y + 1):
  for x in range(1, grid_size_x + 1):
    init_x = x * rectangle_w
    init_y = y * rectangle_h
    #print("pos inicio x:", init_x)
    #print("pos inicio y:",init_y)
    #print("pos fin x:",init_x + rectangle_w)
    #print("pos fin y:",init_y + rectangle_h)
    rectangle = canvas.create_rectangle(init_x,init_y,init_x + rectangle_w,init_y + rectangle_h)
    rectangles.append(rectangle)
    if y == 1:
      if x == 1:
        rewards.append(0)
      elif x == grid_size_x:
        rewards.append(10)
      else:
        rewards.append(-10)
    else:
      rewards.append(0)
        
for x in rewards:
  print(x)
canvas.pack(fill=BOTH, expand=1)
learn()
root.mainloop()