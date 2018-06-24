#!/usr/bin/python

from tkinter import Tk, Canvas, Frame, BOTH
import random
import numpy as np
from move_memory import MoveMememory
from time import sleep
import matplotlib.pyplot as plt
import pickle
import sys, getopt


#Allowed moves in the board
moves = ['UP','LEFT','RIGHT','DOWN']
oposite_moves = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT','RIGHT': 'LEFT'}
#Number of iterations for training
iterations = 50000
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
q_learning_scores = []
sarsa_scores = []
end_positions = []
log = []
start_position = 0
end_flag = False
move_type = []
#HyperParams
#A factor of 0 will make the agent not learn anything, while a factor of 1 would make 
#the agent consider only the most recent information.
alpha = 0.1
decay = 0.000001
eps = .9
#The discount factor determines the importance of future rewards. A factor of 0 makes the agent
#"opportunistic" by only considering current rewards, while a factor approaching 1 will make it 
# strive for a long-term high reward.
gamma = 0.7

#Needed for world moves and actions
fringe_left_values = []
fringe_right_values = []
for i in range(grid_size_y):
  fringe_left_values.append(grid_size_x * i)
  fringe_right_values.append((grid_size_x * i) + grid_size_x - 1)

def initialize_q_table():
  global q_table
  q_table = np.zeros((grid_size_x * grid_size_y, len(moves), 1))

def save_object(obj, filename):
  with open(filename, 'wb') as output:  # Overwrites any existing file.
    pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_q_table(filename):
  with open(filename, 'rb') as input:
    q_table = pickle.load(input)
    return q_table


def win_condition(x):
    return x == 10

def set_eps():
  global eps
  eps = 0.9

def calculate_end_positions():
  global end_positions
  for i in range(1,grid_size_x):
    end_positions.append(i)

def draw_x(pos):
  global x1,x2
  if x1 is not None:
    canvas.delete(x1)
  if x2 is not None:
    canvas.delete(x2)
  if (pos < grid_size_x):
    x = (pos + 1) * rectangle_w
    y = rectangle_h
  elif (grid_size_x <= pos < grid_size_x * 2 ):
    x = (pos + 1 - grid_size_x) * rectangle_w
    y = rectangle_h * 2
  else:
    x = (pos + 1 - (grid_size_x * 2)) * rectangle_w
    y = rectangle_h * 3
  x1 = canvas.create_line(x, y, x + rectangle_w, y + rectangle_h, fill='deep sky blue', width=3)
  x2 = canvas.create_line(x + rectangle_w, y, x, y + rectangle_h, fill='deep sky blue', width=3)

def reset_canvas():
  canvas.delete(x1)
  canvas.delete(x2)

def random_move():
  intended_direction = random.choice(moves)
  return actual_move(intended_direction)

def actual_move(intended_direction):
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

def play_mode_move(actual_pos):
  global end_flag, number_of_moves
  best_move_idx = np.argmax(q_table[actual_pos])
  best_move = moves[best_move_idx]
  direction = actual_move(best_move)
  new_pos, reward = calculate_new_pos_and_reward(actual_pos,direction)
  number_of_moves = number_of_moves + 1
  if new_pos in end_positions:
    end_flag = True
  return new_pos, reward, direction

def move(actual_pos):
  global end_flag, number_of_moves
  if np.random.uniform(0, 1) < eps:
    direction = random_move()
    #print ("move: random")
    #move_type.append(0)
  else:
    best_move_idx = np.argmax(q_table[actual_pos])
    best_move = moves[best_move_idx]
    direction = actual_move(best_move)
    #print ("move: best")
    #move_type.append(1)

  #print("direction: ", direction)
  new_pos, reward = calculate_new_pos_and_reward(actual_pos,direction)
  number_of_moves = number_of_moves + 1
  #if (new_pos == end_position):
  if new_pos in end_positions:
    end_flag = True
  return new_pos, reward, direction
  
def e_greedy(pos):
  if np.random.uniform(0, 1) < eps:
    return random.choice(q_table[pos])
  else:
    return np.max(q_table[pos])


def q_learning():
  print ('using Q-Learning')
  initialize_q_table()
  for iter in range(iterations):
    global score, end_flag, number_of_moves,decay,eps, gamma, q_table
    print("iteration #:", iter)
    #print("eps: ", eps)
    score = 0
    end_flag = False
    number_of_moves = 0
    actual_position = start_position
    while (end_flag == False):
      draw_x(actual_position)
      root.update()
      #print("number_of_moves",number_of_moves)
      new_position, reward, action = move(actual_position)
      #update q_table
      q_table[actual_position,moves.index(action)] = (1 - alpha) * q_table[actual_position,moves.index(action)] + (alpha * (reward + (gamma * np.max(q_table[new_position]))))
      score = score + reward
      actual_position = new_position
      eps -= decay
      #sleep(0.01)
    q_learning_scores.append(score)
    draw_x(actual_position)
    root.update()
    #sleep(3)

def sarsa():
  global score, end_flag, number_of_moves, decay, eps, gamma, q_table
  initialize_q_table()
  set_eps()
  print ('using SARSA')
  for iter in range(iterations):
    print("iteration #:", iter)
    score = 0
    end_flag = False
    number_of_moves = 0
    actual_position = start_position
    while (end_flag == False):
      draw_x(actual_position)
      root.update()
      #print("iteration #:", iter)
      #print("actual_position: ", actual_position)
      #print("score:", score)
      #print("number_of_moves",number_of_moves)
      #print("eps: ", eps)
      new_position, reward, action = move(actual_position)
      #update q_table
      q_next = e_greedy(new_position)
      q_table[actual_position,moves.index(action)] = (1 - alpha) * q_table[actual_position,moves.index(action)] + (alpha * (reward + (gamma * q_next)))
      score = score + reward
      actual_position = new_position
      eps -= decay
      #sleep(0.01)
    draw_x(actual_position)
    root.update()
    sarsa_scores.append(score)

def play():
  global q_table, number_of_moves, end_flag, log
  score = 0
  end_flag = False
  number_of_moves = 0
  actual_position = start_position
  log.append(actual_position)
  while (end_flag == False):
    draw_x(actual_position)
    root.update()
    new_position, reward, direction = play_mode_move(actual_position)
    actual_position = new_position
    log.append(actual_position)
    score = score + reward
    sleep(0.5)
  draw_x(actual_position)
  root.update()
  print("# of Moves: ", number_of_moves)
  print("score: ", score)
  if score == 10:
    ask_for_replay()
  else:
    ask_for_new_play()

def ask_for_replay():
  global log
  respose = input("Do you want to see a replay? [Y/n]")
  if (respose == '' or respose == 'y' or respose == 'Y'):
    for actual_position in log:
      draw_x(actual_position)
      root.update()
      sleep(0.5)
    ask_for_replay()
  else:
    print ("Exiting...")

def ask_for_new_play():
  respose = input("Do you want to play again? [Y/n]")
  if (respose == '' or respose == 'y' or respose == 'Y'):
    play()
  else:
    print ("Exiting...")


def build_env():
  global root, canvas
  calculate_end_positions()
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
      color = 'gray95'
      if y == 1:
        if x == 1:
          rewards.append(0)
        elif x == grid_size_x:
          rewards.append(10)
          color = 'pale green'
        else:
          rewards.append(-10)
          color = 'firebrick1'
      else:
        rewards.append(0)
      rectangle = canvas.create_rectangle(init_x,init_y,init_x + rectangle_w,init_y + rectangle_h, fill=color)
      rectangles.append(rectangle)
          
  #for x in rewards:
    #print(x)
  canvas.pack(fill=BOTH, expand=1)

def main(options):
  global q_table
  if len(options) == 2:
    selected_option = options[1]
  else:
    selected_option = ''
  print("Selected Option: ", selected_option)
  #np settings
  np.set_printoptions(precision=3)
  np.set_printoptions(suppress=True)
  build_env()
  if (selected_option == 'q'):
    q_learning()
    print(q_table)
    save_object(q_table, 'q_table_q_learning.pkl')
    plt.plot(q_learning_scores,'ro')
    plt.ylabel('q_learning scores')
    plt.xlabel('round')
    plt.show()
  elif (selected_option == 'sarsa'):
    sarsa()
    print(q_table)
    save_object(q_table, 'q_table_sarsa.pkl')
    plt.plot(sarsa_scores,'ro')
    plt.ylabel('sarsa scores')
    plt.xlabel('round')
    plt.show()
  elif (selected_option == 'both'):
    #Runs the 2 learning algorithms
    q_learning()
    print(q_table)
    save_object(q_table, 'q_table_q_learning.pkl')
    sarsa()
    print(q_table)
    save_object(q_table, 'q_table_sarsa.pkl')
    plt.subplot(2, 1, 1)
    plt.plot(q_learning_scores,'ro')
    plt.ylabel('q_learning scores')
    plt.xlabel('round')
    plt.subplot(2, 1, 2)
    plt.plot(sarsa_scores,'ro')
    plt.ylabel('sarsa scores')
    plt.xlabel('round')
    plt.show()

    q_learning_win_sum = sum(1 for i in q_learning_scores if win_condition(i))
    sarsa_win_sum = sum(1 for i in sarsa_scores if win_condition(i))
    print("q-learning win rate : ", (q_learning_win_sum * 100)/iterations)
    print("sarsa win rate : ", (sarsa_win_sum * 100)/iterations)
  elif ( selected_option == 'play_q'):
    q_table = load_q_table('q_table_q_learning.pkl')
    play()
    sleep(5)
  elif ( selected_option == 'play_s'):
    q_table = load_q_table('q_table_sarsa.pkl')
    play()
    sleep(5)
  else:
    print("ussage: reinforcement_learning.py <option>")
    print("options are:")
    print("q : Learns using Q-Learning")
    print("sarsa: Learns using SARSA")
    print("both: Runs both Learning algorithms")
    print("play_q: Plays using Q-Learning q_table")
    print("play_s: Plays using SARSA q_table")

if __name__ == "__main__":
   main(sys.argv)