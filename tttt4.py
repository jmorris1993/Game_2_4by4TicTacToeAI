# -*- coding: utf-8 -*-
#!/usr/bin/env python
# October 5 2014
#
# Julian Morris & Alvaro Antunez
#
# Game Programming, Level 2 Project
#
# TIC-TAC-TOE 4
#
# A simple strategy game, an extension of the standard 4x4 tic-tac-toe
#

import sys
from graphics import *
import copy
import random
import cProfile


GRID_SIZE = 4
hasWinner=0
tie=0
screenSize=600
width, height =150,150
giantMoveList = []
availableMoves=[]



def fail (msg):
    raise StandardError(msg)

def create_board (string):
    # Take a description of the board as input and create the board
    #  in your representation
    #
    # The string description is a sequence of 16 characters,
    #   each either X or O, or . to represent a free space
    # It is allowed to pass in a string describing a board
    #   that would never arise in legal play starting from an empty
    #   board
    grid = []
    for j in range(0,len(string),4):
        thing=[string[j],string[j+1],string[j+2],string[j+3]]
        grid.append(thing)
    return grid
        

def has_mark (board,x,y):
    # Take a board representation and checks if there's a mark at
    # position x, y (each between 1 and 4)
    # Return 'X' or 'O' if there is a mark
    # Return False if there is not
    if x>GRID_SIZE or x<1 or y>GRID_SIZE or y<1:
        return False
        
    if board[y-1][x-1]=='O':
        return 'O'
    elif board[y-1][x-1]=='X':
        return 'X'
    else:
        return False

def has_win (board):
    # Check if a board is a win for X or for O.
    # Return 'X' if it is a win for X, 'O' if it is a win for O,
    # and False otherwise
    for y in board:
        if y[0]!='.' and y[0]==y[1]==y[2]==y[3]:
            return y[0]
    for x in range(4):
        if board[0][x]!='.' and board[0][x]==board[1][x]==board[2][x]==board[3][x]:
            return board[0][x]
    if board[0][0]!='.' and board[0][0]==board[1][1]==board[2][2]==board[3][3]:
        return board[0][0]
    elif board[0][3]!='.' and board[0][3]==board[1][2]==board[2][1]==board[3][0]:
        return board[0][3]
    else:
        return False
        

def done (board):
    # Check if the board is done, either because it is a win or a draw
    if has_win(board)==False:
        for x in range(4):
            for y in range(4):
                if board[y][x]=='.':
                    return False
        return True
    else:
        return True


def print_board (board):
    # Display a board on the console
    # Use this for AI vs. AI testing.
    for row in board:
        print " ".join(row) 




def draw_board (board,win):
    # Draws the board on a screen. Comment this out for AI vs. AI testing.
    
    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):           
            rect=Rectangle(Point(width*row,height*column),Point((width)*(row+1),(height)*(column+1)))
            rect.setFill('white')
            rect.draw(win)
            if board[column][row]=='O':
                Circle(Point(row*150+75,column*150+75),50).draw(win)
            elif board[column][row]=="X":
                ln1 = Line(Point(row*150+25,column*150+25),Point(row*150+125,column*150+125))
                ln2 = Line(Point(row*150+125,column*150+25),Point(row*150+25,column*150+125))
                ln1.draw(win)
                ln2.draw(win)


def wait_player_input (board,player,win):
  # Returns the position of the board from getting a mouse click input from the user.
  # Comment this out for AI vs AI testing.

  pos = win.getMouse()
  x=pos.getX()/150+1
  y=pos.getY()/150+1
  if x>4 or x<1 or x>4 or x<1:
      return wait_player_input(board,player)
  elif [x,y] not in checkAvailableMoves(board,player):
      return wait_player_input(board,player)

  return x,y


def checkAvailableMoves (board,player):
    #Checks the empty spots on the board.

    numAvailableMoves=0
    availableMoves = []
    for y in range(1,GRID_SIZE+1):
        for x in range(1,GRID_SIZE+1):
            if board[y-1][x-1]=='.':
                numAvailableMoves+=1
                availableMoves.append([x,y])
    return availableMoves

def read_player_input (board, player):
    # Read player input when playing as 'player' (either 'X' or 'O')
    # Return a move (a tuple (x,y) with each position between 1 and 4)
    # Only used when printing to the console.

     rawmove = raw_input("Please enter your move as two numbers: ")
     if len(rawmove)!=2:
        print "Please enter a valid input"
        print_board(board)
        return read_player_input (board, player)
     lstmove=list(rawmove)
     try:
        lstmove[0]=int(lstmove[0])
        lstmove[1]=int(lstmove[1])                 
     except: ValueError
     pass
     if lstmove[0]>4 or lstmove[0]<1 or lstmove[1]>4 or lstmove[1]<1:
         print "Please enter a valid input"
         print_board(board)
         return read_player_input (board, player)
     elif [lstmove[0],lstmove[1]] not in checkAvailableMoves(board,player):
         print "Please enter a valid input"
         print_board(board)
         return read_player_input (board, player)
         
     return lstmove

def make_move (board,move,player):
    # Returns a board where 'move' has been performed on 'board' by 
    # 'player'
    # Change can be done in place in 'board' or a new copy created
    if move[0]>4 or move[0]<1 or move[1]>4 or move[1]<1:
        return False
    board[move[1]-1][move[0]-1]=player
    return board
    
         
def hasTriple(board, player):
    #Checks rows for a three in a row.
    for y in range(GRID_SIZE):
        if board[y].count(player)==3:
            for x in range(GRID_SIZE):
                if board[y][x]=='.':
                    return [x+1,y+1]
                    print'a'
                    break
    #Checks columns for a three in a row.
    for x in range(GRID_SIZE):
        if board[0][x]=='.' and board[1][x]==board[2][x]==board[3][x]==player:
            return [x+1,1]
        if board[1][x]=='.' and board[0][x]==board[2][x]==board[3][x]==player:
            return [x+1,2]
        if board[2][x]=='.' and board[0][x]==board[1][x]==board[3][x]==player:
            return [x+1,3]
        if board[3][x]=='.' and board[0][x]==board[1][x]==board[2][x]==player:
            return [x+1,4]
       
    #Checks left to right diagonal for a three in a row.
    if board[0][0]=='.' and board[1][1]==board[2][2]==board[3][3]==player:
        return [1,1]
    elif board[1][1]=='.' and board[0][0]==board[2][2]==board[3][3]==player:
        return [2,2] 
    elif board[2][2]=='.' and board[0][0]==board[1][1]==board[3][3]==player:
        return [3,3] 
    elif board[3][3]=='.' and board[0][0]==board[1][1]==board[2][2]==player:
        return [4,4] 
        
    #Checks right to left diagnoal for a three in a row.
    elif board[0][3]=='.' and board[1][2]==board[2][1]==board[3][0]==player:
        return [4,1]
    elif board[1][2]=='.' and board[0][3]==board[2][1]==board[3][0]==player:
        return [3,2]
    elif board[2][1]=='.' and board[0][3]==board[1][2]==board[3][0]==player:
        return [2,3]
    elif board[3][0]=='.' and board[0][3]==board[1][2]==board[2][1]==player:
        return [1,4]
        
    return False

def hasDouble(board, player):
    #Checks rows for a double
    for y in range(GRID_SIZE):
        if board[y].count(player)==2:
            for x in range(GRID_SIZE):
                if board[y][x]=='.':
                    return [x+1,y+1]
                    print'a'
                    break
    
    #Checks columns for a double            
    for x in range(GRID_SIZE):
        verticalCoordinates = [[x+1,1],[x+1,2],[x+1,3],[x+1,4]]
        verticalValues = [board[0][x],board[1][x],board[2][x],board[3][x]]
        
        if verticalValues.count(player)==2:
            for i in range(len(verticalValues)):
                if verticalValues[i] == '.':
                    return verticalCoordinates[i]
                    
    #Checks left to right diagonal for a double
    if board[0][0]=='.' and board[1][1]==board[2][2]==player:
        return [1,1]   
    elif board[0][0]=='.' and board[2][2]==board[3][3]==player:
        return [1,1]  
    elif board[0][0]=='.' and board[1][1]==board[3][3]==player:
        return [1,1]            
    elif board[1][1]=='.' and board[0][0]==board[2][2]==player:
        return [2,2] 
    elif board[1][1]=='.' and board[0][0]==board[3][3]==player:
        return [2,2]         
    elif board[2][2]=='.' and board[0][0]==board[1][1]==player:
        return [3,3] 
       
    #Checks right to left diagnoal for a triple   
    elif board[0][3]=='.' and board[1][2]==board[2][1]==player:
        return [4,1]
    elif board[0][3]=='.' and board[1][2]==board[3][0]==player:
        return [4,1]
    elif board[0][3]=='.' and board[2][1]==board[3][0]==player:
        return [4,1]              
    elif board[1][2]=='.' and board[0][3]==board[3][0]==player:
        return [3,2]
    elif board[2][1]=='.' and board[0][3]==board[1][2]==player:
        return [2,3]
    elif board[3][0]=='.' and board[0][3]==board[2][1]==player:
        return [1,4]
        
    return False   
    
def minimax(board, player):
    # Returns the value of a move that the computer has evaluated.
    global availableMoves
    
    if availableMoves == []:
        win = has_win(board)
        if win =="X":
            return 1
        elif win=="O":
            return -1
        elif done(board):
            return 0
        
    else:
      global giantMoveList
      valueList = []
      for y in range(1,GRID_SIZE+1):
          for x in range(1,GRID_SIZE+1):
              if board[y-1][x-1]=='.':
                availableMoves.append([x,y])
                
      for i in range(len(availableMoves)):
          
          move= availableMoves[i]
          hypo = make_move(copy.deepcopy(board),move,player)
          
#          if hypo not in giantMoveList:        #Tried saving the entire game tree in a list,
#              giantMoveList.append(hypo)       # and did stuff with it, but it only made it slower.
              
          valueList.append(minimax(hypo,other(player)))
          
          #My attempt at alpha beta pruning. It cut the runtime in half.
          if valueList[i]==1 and player == "X":
              return 1
          elif valueList[i]==-1 and player=="O":
              return -1
          
      if player == "X":
          return max(valueList)
      else:
          return min(valueList)
            

def computer_moveHard (board,player):
    # The computer move that the computer makes.
    # It checks to see if it has a triple, then a double.
    # This AI is good enough that it can draw against itself a million times.
    # See the AIvsAITesting function for detail.

    availableMoves = checkAvailableMoves(board,player)
    centerMoves = [[2,2],[2,3],[3,2],[3,3]]
    
    if hasTriple(board,player)!=False:
        return hasTriple(board,player)
    
    elif hasTriple(board,other(player))!=False:
        return hasTriple(board,other(player))
        
    elif hasDouble(board,other(player))!=False:
        return hasDouble(board,other(player))
    
    elif hasDouble(board,player)!=False:
        return hasDouble(board,player)
    
    elif len(availableMoves)>=11:
        for i in centerMoves:
            if board[i[1]-1][i[0]-1]=='.':
                return i
        return availableMoves[random.randrange(len(availableMoves))]
            
    else:
        return availableMoves[random.randrange(len(availableMoves))]



def computer_move (board,player):
    # Select a move for the computer, when playing as 'player' (either 
    #   'X' or 'O')
    # Return the selected move (a tuple (x,y) with each position between 
    #   1 and 4)
    # computer move using the game tree. It is now so efficient that it doesn't even take a second.

    availableMoves = checkAvailableMoves(board,player)
    bestMove = (-1,None)
    
    if hasTriple(board,player)!=False:
        return hasTriple(board,player)
    
    elif hasTriple(board,other(player))!=False:
        return hasTriple(board,other(player))
    
    elif hasDouble(board,other(player))!=False:
        return hasDouble(board,other(player))
        
    for i in range(len(availableMoves)):
        
        move= availableMoves[i]
        hypo = make_move(copy.deepcopy(board),move,player)
        value = minimax(hypo, other(player))
        
        #Slightly faster when it's all on one line.
        if bestMove[1]==None or (player == "X" and value>bestMove[1]) or (player == "O" and value <bestMove[1]) :
            bestMove = (i, value)

    return availableMoves[bestMove[0]]


def other (player):
    #Gets other player.
    if player == 'X':
        return 'O'
    return 'X'


def run (string,player,playX,playO): 
    #The run method that gets the game going.
    
    board = create_board(string)
    print_board(board)

    while not done(board):
        if player == 'X':        
            move = playX(board,player)
            print "Player X moved to" + str(tuple(move))

        elif player == 'O':
            move = computer_move(board,player)
            print "Computer O moved to"+ str(tuple(move))

        else:
            fail('Unrecognized player '+player)
            
        board = make_move(board,move,player)
        print_board(board)
        player = other(player)

    winner = has_win(board)
    
    if winner:
        print winner,'wins!'

    else:
        print 'Draw'


def runScreen (string,player,playX,playO): 
    #The run method that gets the game going.
    
    board = create_board(string)
    win=GraphWin('4*4TicTacToe',screenSize,screenSize)
    draw_board(board,win)

    while not done(board):
        if player == 'X':        
            move = playX(board,player,win)

        elif player == 'O':
            move = computer_move(board,player)

        else:
            fail('Unrecognized player '+player)
            
        board = make_move(board,move,player)
        draw_board(board, win)
        player = other(player)

    winner = has_win(board)
    
    if winner:
        print winner,'wins!'
        win.close()
    else:
        print 'Draw'
        win.close()
        
       

#run("OXXOXOO.........","X",read_player_input, computer_move)


oneCircle = ""
a = random.randrange(15)
#generates a random string with one O.
for i in range(16):
    if i == a:
        oneCircle+="O"
    else:
        oneCircle+='.'


#run(oneCircle,"X",read_player_input, computer_move)

#Testing the version of the game where the board is drawn on the screen.
#AI uses the game tree.
#runScreen(oneCircle,"X",wait_player_input, computer_move)

#Testing the version of the game where the board is drawn on the console.
#AI uses the game tree.
#run("."*16,"X",read_player_input, computer_move)


#Testing the version of the game where the board is drawn on the screen.
#AI is hard coded.

#runScreen(oneCircle,"X",wait_player_input, computer_moveHard)


#Testing the version of the game where the board is drawn on the console.
#AI is hard coded.

#run("."*16,"X",read_player_input, computer_moveHard)




#Testing the runtime
#cProfile.run('computer_move(create_board("O.O..XO.XX..O.X."),"X")')

#run("................","X",read_player_input, computer_move)

def AIvsAI (string,player,playX,playO): 
    #Tests AIvsAI to see which side wins for one game.
    
    board = create_board(string)
    #print_board(board)

    while not done(board):
        if player == 'X':        
            move = computer_move(board,player)

        elif player == 'O':
            #move = computer_moveHard(board,player)
            move = computer_move(board,player)

        else:
            fail('Unrecognized player '+player)
        board = make_move(board,move,player)
        #print_board(board)
        player = other(player)

    winner = has_win(board)
    if winner:
        print_board(board)
        global hasWinner
        hasWinner+=1

    else:
        global tie
        tie+=1


def AIvsAITesting(iterations):
    #Tests AIvsAI to see how often they draw and how often one side wins for 
    #multiple iterations. When using this, comment out everything to do with
    #graphics. Which are wait_player_input, global variable win, and 

    for i in range(iterations):
        #AIvsAI("."*16,"X",computer_move, computer_moveHard) #Game tree computer vs. hard coded computer.
        AIvsAI("."*16,"X",computer_move, computer_move) #Game tree vs. Game tree.
        print hasWinner, tie
        if tie==10000:            #Just to see if the computer is still awake
            print tie
        if tie==20000:
            print tie
    return hasWinner, tie
    
#print AIvsAITesting(30000)



