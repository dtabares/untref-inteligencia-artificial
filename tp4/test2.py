#!/usr/bin/python

from tkinter import Tk, Canvas, Frame, BOTH
import random
import numpy as np

moves = ['UP','LEFT','RIGHT','DOWN']
oposite_moves = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT','RIGHT': 'LEFT'}


rectangles = []
rectangle_h = 50
rectangle_w = 50
awards = []
x1 = None
x2 = None

def draw_x(x,y):
  canvas.delete(x1)
  canvas.delete(x2)
  x1 = canvas.create_line(x, y, x + rectangle_w, y + rectangle_h)
  x2 = canvas.create_line(x + rectangle_w, y, x, y + rectangle_h)

def random_move():
  intended_move = random.choice(moves)
  actual_move = probabilities_for_a_move(intended_move)
  return actual_move

def probabilities_for_a_move(intended_move):
  moves_with_probabilities = {'UP': 0.2, 'DOWN':0.2, 'LEFT': 0.2,'RIGHT': 0.2}
  moves_with_probabilities[intended_move] = 0.8
  moves_with_probabilities[oposite_moves[intended_move]] = 0
  return moves_with_probabilities



# Define la ventana principal de la aplicación
root = Tk()
# Define las dimensiones de la ventana, que se ubicará en 
# el centro de la pantalla. Si se omite esta línea la
# ventana se adaptará a los widgets que se coloquen en
# ella. 
root.geometry("800x250+300+300")
root.title("UNTREF - IA - TP 4") 
canvas = Canvas(root)
for x in range(1, 11):
          for y in range(1, 4):
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
                awards.append(0)
              elif x == 10:
                awards.append(10)
              else:
                awards.append(-10)
            else:
              awards.append(0)
        
for x in awards:
  print(x)
canvas.pack(fill=BOTH, expand=1)
root.mainloop()