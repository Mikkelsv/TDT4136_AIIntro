from sys import stdin
import math
from tkinter import *
from PIL import Image, ImageDraw
import copy


class Node():
  def __init__(self,x,y,wall=False,goal=False,start=False,cost=1):
    self.x,self.y,self.wall,=x,y,wall #inits the Node depending on input
    self.wall,self.goal,self.start=wall,goal,start
    self.parent =None #current parent is set to None
    self.children =[] #current children is set to empty
    self.path_cost=float('inf') #g(n)
    self.path_remaining= None  #h(n)
    self.path_clear = None     #f(n)
    self.cost=cost 

  def manhatten_distance(self,goal):
    self.path_remaining = abs(goal.x-self.x)+abs(goal.y-self.y)
    self.path_clear = self.path_cost + self.path_remaining
 
  def pos(self): #returns the position of the Node
    return (self.x,self.y)
  
class A_star():
  def __init__(self,t,nodes,start,goal,alg="A_star"):
    self.table= t #a table to map where the algorithm have been
    self.nodes = nodes #a list of all Node objects
    self.goal = goal #the ending goal
    self.start = start #the start goal
    self.start.manhatten_distance(goal) #Calculate finds the manhatten distance
    self.path = [] #A list to store the path found
    self.alg=alg #The set algorithm: A_Star, Djikstras or DBS
    print("Start: %d %d, Goal: %d, %d" %(start.x,start.y,goal.x,goal.y),end=" ")
    
  def agenda_loop(self): #The A_star algorithm
    closed = []
    agenda = [self.start] #Open
    while(agenda): #Agenda Loop
      #The different sort methods, depending on algorithm chosen
      if(self.alg=="BFS"): 
        pass #dont sort
      elif(self.alg=="Djikstra"):
        agenda.sort(key=lambda n: n.path_cost)
      else: 
        agenda.sort(key=lambda n: n.path_clear)

      node = agenda.pop(0) #X <- pop(OPEN)
      self.table[node.pos()[0]][node.pos()[1]]="V" #updates the table, visitied current node
      closed.append(node) #push(X,closed)

      if node.goal: #if X is a solution retun (X,Succeed)
        self.update_path() #fills the path[] with it parents back to start
        print("Shortest Path Found")
        return True, self.table,self.path

      self.generate_all_children(node) #Succ <- generate_all_successors(X) + push(S,kids(X))
      for child in node.children:
        #Did not need "If node S* has previosly beed created, and if
        #state(S*)==state(S) then S <-S*
        if child not in agenda and child not in closed: 
          self.attach_and_eval(child,node) #attach-and-eval(S,X)
          agenda.append(child) #insert(S,OPEN)
        elif node.path_cost + child.cost < child.path_cost:
          self.attach_and_eval(child,node)
          if child in closed:
            self.propagate_path_improvements(child)
    print("No Path Found") #if it breaks without retring, Loop Failed
    return False,self.table,self.path
  
  def generate_all_children(self,parent):
    #Followed the A_Star pseudocode
    for child in self.nodes:
      if (child.x == parent.x + 1 and child.y == parent.y) or\
          (child.x == parent.x -1 and child.y == parent.y) or\
          (child.x == parent.x and child.y == parent.y+1) or\
          (child.x == parent.x and child.y == parent.y-1):
        if not child.wall:
          parent.children.append(child)

  def attach_and_eval(self,child,parent):
    #Followed the A_Star pseudocode
    child.parent=parent
    child.path_cost = parent.path_cost + child.cost
    child.manhatten_distance(self.goal)
    child.path_clear = child.path_cost + child.path_remaining 
    self.table[child.pos()[0]][child.pos()[1]]="N" #updates the table, noticed the child node

  def propagate_path_improvements(self,parent):
    #Followed the A_Star pseudocode
    for child in parent.children:
      current_path_cost =  parent.path_cost+child.cost
      if current_path_cost < child.path_cost:
        child.parent=parent
        child.path_cost = current_path_cost 
        child.path_clear = child.path_cost + child.path_remaining
  
  def update_path(self):
    #Follows the parent-chain from the goal to the start
    current = self.goal
    self.path.append(current)
    while(current.parent):
      self.table[current.pos()[0]][current.pos()[1]]="P" #updates table with path 
      current = current.parent
      self.path.append(current) 
    self.path.reverse()


def get_input(f): #takes in the input file as list
  t = []
  inp = open(f)
  for line in inp:
    t.append(list(line))
  return t

def build_board(t):#builds the board with the nodes
  nodes = set([])
  for x in range(len(t)):
    for y in range(len(t[x])):
      sign=t[x][y]
      if sign=='.':
        node=Node(x,y,cost=1)
      elif sign=='#':
        node=Node(x,y,wall=True)
      elif sign=='w':
        node=Node(x,y,cost=100)
      elif sign=='m':
        node=Node(x,y,cost=50)
      elif sign=='f':
        node=Node(x,y,cost=10)
      elif sign=='g':
        node=Node(x,y,cost=5)
      elif sign=='r':
        node=Node(x,y,cost=1)
      elif sign=='A':
        node = Node(x,y,start=True)
        node.path_cost = 0
        start = node 
      elif sign=='B':
        node = Node(x,y,goal=True)
        goal = node
      nodes.add(node) 
  return nodes,start,goal

def build_string_from_table(t): #builds a string used for the gui
  s=""
  for x in range(len(t)):
    for y in range(len(t[0])):
      s = s + t[x][y]
  return s

def build_string_from_table_2(t,path=[]): #builds a string used for the gui
  T = list(t)
  s=""
  for n in path[1:-1]:
    x,y = n.pos()
    T[x][y]='P'
  for x in range(len(t)):
    for y in range(len(t[0])):
      s = s + T[x][y]
  return s

def build_gui(s,p,w,h,filename="NoName.jpg",save=True,show=False,rec_size=50):
    #builds the GUI and saves it. se show=True to show it
    width = w*rec_size 
    height=h*rec_size
    root = Tk()
    cv = Canvas(root, width=w*rec_size, height=h*rec_size,bg='white') 
    cv.pack()
    img = Image.new("RGB",(width,height),(255,255,255))
    draw = ImageDraw.Draw(img)
    x = 0
    y = 0
    for symbol in s:
        if symbol == '\n':
            y += 1
            x = 0
        else:
            #Different Colors mapped to different symbols
            if symbol == 'A': color = '#ff0000' 
            elif symbol == 'B': color = '#00ff00'
            elif symbol == '#': color = '#000000'
            elif symbol == 'f': color = '#008080'
            elif symbol == 'g': color = '#76eec6'
            elif symbol == 'm': color = '#cdaa7d'
            elif symbol == 'w': color = '#99ccff'
            elif symbol == 'r': color = '#cdc0b0'
            else: color = 'white'
            cv.create_rectangle(x*rec_size, y*rec_size, \
                    x*rec_size + rec_size, y*rec_size + rec_size, fill=color)
            if save:
              draw.rectangle([(x*rec_size, y*rec_size), \
                      (x*rec_size + rec_size, y*rec_size + rec_size)], fill=color)
            x += 1
    x = 0
    y = 0
    for symbol in p:
        if symbol == '\n':
            y += 1
            x = 0
        else:
            #Different Colors mapped to different symbols
            if symbol == 'P': #plots path nodes
              cv.create_oval((x+1/3)*rec_size, (y+1/3)*rec_size, \
                    (x+2/3)*rec_size,(y+2/3)*rec_size, fill='#0000ff')
              draw.ellipse(((x+1/3)*rec_size, (y+1/3)*rec_size, \
                    (x+2/3)*rec_size,(y+2/3)*rec_size), fill='#0000ff')

            elif symbol == 'V': #plots visited nodes
              cv.create_oval((x+1/3)*rec_size, (y+1/3)*rec_size, \
                    (x+2/3)*rec_size,(y+2/3)*rec_size, fill='#000000')
              draw.ellipse(((x+1/3)*rec_size, (y+1/3)*rec_size, \
                    (x+2/3)*rec_size,(y+2/3)*rec_size), fill='#000000')

            elif symbol == 'N': #plots discovered nodes
              cv.create_oval((x+1/3)*rec_size, (y+1/3)*rec_size, \
                    (x+2/3)*rec_size,(y+2/3)*rec_size, fill='#ff9933')
              draw.ellipse(((x+1/3)*rec_size, (y+1/3)*rec_size, \
                    (x+2/3)*rec_size,(y+2/3)*rec_size), fill='#ff9933') 
            x += 1
    if save:
      img.save(filename) #saves the image
    if show: 
      root.mainloop() #shows the image

def copy_list(t):#makes a copy of a list
  T=[]
  for x in range(len(t)):
    T.append([])
    for y in range(len(t[x])):
      T[x].append(t[x][y])
  return T

def get_file(f): #returns a file name
  return "boards/boards/board-"+f+".txt"

def _name(p,n,m): #Gives a filename used for saving
  return "outputs/"+p+"/"+n+"_"+m+".jpg"

def files(): #Returns a list of all the boards names
  return [["1-1","1-2","1-3","1-4"],["2-1","2-2","2-3","2-4"]]

def execute_board(name,alg="A_star",shortcut=True): #executes a single file, returns values
  if shortcut:
    f = get_file(name) 
  else:
    f = name
  t = get_input(f)

  nodes,start,goal = build_board(t)
  a_star = A_star(copy_list(t),nodes,start,goal,alg=alg)
  path_found,e_t,path =  a_star.agenda_loop()
  return t,e_t,path_found,path
 
def create_gui(alg,t,e_t,path,name,save=True,show=False): 
  map_string = build_string_from_table(t) #map string from map table
  exp_string = build_string_from_table(e_t) #explored string from explored table
  build_gui(map_string,exp_string,len(t[0]),len(t),_name(alg,name,"map"),save,show)

def execute_all_files(names,algorithm="A_star"):
  for i in range(len(names)):
    for j in range(len(names[i])):
      name = names[i][j]
      t,e_t,path_found,path = execute_board(name,alg=algorithm)
      create_gui(algorithm,t,e_t,path,name,True,False)

def main(): 
  #make sure to have a the following folders:
  #outputs/BFS , outputs/A_star, outputs/Djikstra
  names = files()
  name = names[1][3] 
  shortcut = True
  #for specific file: name = "bords/boards/1-1.txt" while setting shortcut to False

  algorithm = "A_star" #"A_star", "BFS", "Djikstra"
  t,e_t,path_found,path = execute_board(name,alg=algorithm,shortcut=shortcut)
  create_gui(algorithm,t,e_t,path,name,save=True,show=True)

  #To execute all files, show disabled for these
  execute_all_files(names,"A_star")
  execute_all_files(names,"Djikstra")
  execute_all_files(names,"BFS")
 
if __name__=="__main__":
  main()
