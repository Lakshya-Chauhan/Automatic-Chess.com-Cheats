from os import system
import random
import pyautogui as gui
import time
from stockfish import Stockfish

stockfish = Stockfish(path = "<---Path of the Stockfish Exe--->", depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 3})

initPos = [None, None]
finalPos = [None, None]
firstCheck = True
justMoved = False
fullyMoved = False
selfColor = None
initFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" #initial position of chess board (assuming the user to be playing with white)
currentFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" #We set current Fen to initFen assuming that the player will get white color

#The following parameters were discovered by me after taking a screenshot
boardInitPos = [109, 227] #Coordinates where the chess board starts (on chess.com)
boardEndPos = [844, 962]  #Coordinates where the chess board ends (on chess.com)
blockSize = [(boardEndPos[0]-boardInitPos[0])/8, (boardEndPos[1]-boardInitPos[1])/8] #Size of each square on chess board (on chess.com)
boardColors = [(243, 243, 244), (106, 155, 65)] #The color of Board in 8-bit theme

def fenBlack(board : list): #get fen of the board for black for starting positions
    global initFen
    spaces = 0
    fenStr = str()
    for y in range(7, -1, -1):
        for x in range(7, -1, -1):
            if board[x][y] != " ":
                if spaces != 0: fenStr, spaces = fenStr + str(spaces), 0
                fenStr += board[x][y]
            else : spaces += 1
            if x == 0 and y != 0 : 
                if spaces != 0 : fenStr, spaces = fenStr + str(spaces), 0
                fenStr += '/'
    fenStr += " w KQkq - 0 1"
    if fenStr != initFen:
        fenStr = fenStr[:-len("w KQkq - 0 1")] + "b KQkq - 0 1"
    return fenStr

                    

if __name__ == "__main__":
    while True:
        img = gui.screenshot()

        currentBoard = list()
        for x in range(8):
            currentBoard.append(list())
            for y in range(8):
                bPos = [int(boardInitPos[0] + blockSize[0]*x), int(boardInitPos[1] + blockSize[1]*y)]

                if img.getpixel((bPos[0]+46, bPos[1]+71)) in boardColors: #if these coordinates are transparent for the png of piece than it must not be there
                    currentBoard[x].append(" ")

                elif img.getpixel((bPos[0]+55, bPos[1]+9)) not in boardColors: #Only for Knight are these coordinates filled
                    currentBoard[x].append("N")

                elif (img.getpixel((bPos[0]+42, bPos[1]+9)) not in boardColors) and (img.getpixel((bPos[0]+49, bPos[1]+9)) not in boardColors): #Both of these coordinates are filled at same time only if the piece is king
                    currentBoard[x].append("K")

                elif img.getpixel((bPos[0]+42, bPos[1]+42)) in boardColors: #As in 8 bit theme there is cut in the bishop, the middlish coordinates are transparent thus the color of board appears
                    currentBoard[x].append("B")

                elif img.getpixel((bPos[0]+21, bPos[1]+22)) not in boardColors: #Only for the queen are these coordinates Occupied (The coordinates of highest point of the crown of the queen)
                    currentBoard[x].append("Q")

                elif img.getpixel((bPos[0]+29, bPos[1]+16)) not in boardColors: #Only for the rook are these filled
                    currentBoard[x].append("R")

                else: #If the piece falls in none of the above catagories it has to be a pawn
                    currentBoard[x].append("P")

                if img.getpixel((bPos[0]+46, bPos[1]+71)) == (56, 56, 56): #checks if the piece is black
                    currentBoard[x][y] = currentBoard[x][y].lower()
                    
        if firstCheck == True: #if this is the first iteration of the loop
            if currentBoard[0][0].isupper() == True : 
                selfColor = 'black' #sets the color of player to black
                currentFen = fenBlack(currentBoard) #gets the current fen
                stockfish.set_fen_position(currentFen)
                if currentFen != initFen: #if this holds then it means that white player has already made it's move and it's black's turn
                    move = stockfish.get_best_move()
                    stockfish.make_moves_from_current_position([move])
                    
                    #getting the coordinates of the point of start and of end from the stockfish notation
                    initPos[0] = 104-ord(move[0])
                    initPos[1] = int(move[1])-1
                    finalPos[0] = 104-ord(move[2])
                    finalPos[1] = int(move[3])-1

                    #simulating virtual clicks on the start point and at the end point thus making a move
                    gui.moveTo(boardInitPos[0] + initPos[0]*blockSize[0] + 78, boardInitPos[1] + initPos[1]*blockSize[1] + 78, 0.2)
                    gui.click()
                    gui.moveTo(boardInitPos[0] + finalPos[0]*blockSize[0] + 78, boardInitPos[1] + finalPos[1]*blockSize[1] + 78, 0.3)
                    gui.click()
                    justMoved = True
                    firstCheck = False
                    continue
                    


            else : 
                selfColor = 'white'
                stockfish.set_fen_position(initFen)
                move = random.choice(["c2c4", "e2e4", "d2d4", "f2f4", "c2c3", "e2e3", "d2d3", "f2f3"])
                stockfish.make_moves_from_current_position([move])

                # vitrual move Making logic here
                initPos[0] = ord(move[0])-97
                initPos[1] = 8-int(move[1])
                finalPos[0] = ord(move[2])-97
                finalPos[1] = 8-int(move[3])

                gui.moveTo(boardInitPos[0] + initPos[0]*blockSize[0] + 78, boardInitPos[1] + initPos[1]*blockSize[1] + 78, 0.2)
                gui.click()
                gui.moveTo(boardInitPos[0] + finalPos[0]*blockSize[0] + 78, boardInitPos[1] + finalPos[1]*blockSize[1] + 78, 0.3)
                gui.click()
                justMoved = True
                firstCheck = False
                continue

            prevBoard = currentBoard
            firstCheck = False
        
        if justMoved == True:            
            initPos = [None, None]
            finalPos = [None, None]

            prevBoard = currentBoard
            justMoved = False
        
        if prevBoard != currentBoard:
            if fullyMoved == False:
                time.sleep(0.3)
                fullyMoved = True
                continue
            fullyMoved = False
            system("cls")
            print(selfColor)
            pieceMoves = list()
            for i in range(8):
                for j in range(8):
                    if prevBoard[i][j] != currentBoard[i][j]:
                        if selfColor == 'black' and ((prevBoard[i][j].isupper() == True) or (currentBoard[i][j].isupper() == True)):
                            if initPos == [None, None] : initPos = [i, j]
                            else : finalPos = [i, j]
                            pieceMoves.append([i, j])
                        elif (prevBoard[i][j].islower() == True) or (currentBoard[i][j].islower() == True):
                            if initPos == [None, None] : initPos = [i, j]
                            else : finalPos = [i, j]
                            pieceMoves.append([i, j])
                        
                    print(currentBoard[j][i], end=" ")
                print()
            
            if len(pieceMoves) == 4:
                print("\<----        nCastles!!         ---->\n")
                for i in range(4):
                    for j in range(4):
                        if (i!=j) and (currentBoard[pieceMoves[i][0]][pieceMoves[i][1]] == prevBoard[pieceMoves[j][0]][pieceMoves[j][1]]) and (currentBoard[pieceMoves[i][0]][pieceMoves[i][1]].lower() == 'k'):
                            initPos = pieceMoves[i]
                            finalPos = pieceMoves[j]
                            print("<----   ", pieceMoves[i], pieceMoves[j], "   ---->")

            print(initPos, finalPos, len(pieceMoves))
            if initPos != [None, None]:
                if selfColor == 'black':
                    if prevBoard[initPos[0]][initPos[1]].isupper() != True:
                        initPos, finalPos = finalPos, initPos
                    initPos[0] = chr(104-initPos[0])
                    initPos[1] = str(initPos[1]+1)
                    finalPos[0] = chr(104-finalPos[0])
                    finalPos[1] = str(finalPos[1]+1)
                else:
                    if prevBoard[initPos[0]][initPos[1]].islower() != True:
                        initPos, finalPos = finalPos, initPos
                    initPos[0] = chr(97+initPos[0])
                    initPos[1] = str(8-initPos[1])
                    finalPos[0] = chr(97+finalPos[0])
                    finalPos[1] = str(8-finalPos[1])

                move = initPos[0] + initPos[1] + finalPos[0] + finalPos[1]
                print(move)

                stockfish.make_moves_from_current_position([move])
                bestMove = stockfish.get_best_move()
                
                if selfColor == 'black':
                    initPos[0] = 104-ord(bestMove[0])
                    initPos[1] = int(bestMove[1])-1
                    finalPos[0] = 104-ord(bestMove[2])
                    finalPos[1] = int(bestMove[3])-1

                else:
                    initPos[0] = ord(bestMove[0])-97
                    initPos[1] = 8-int(bestMove[1])
                    finalPos[0] = ord(bestMove[2])-97
                    finalPos[1] = 8-int(bestMove[3])

                print(bestMove)
                stockfish.make_moves_from_current_position([bestMove])

                gui.moveTo(boardInitPos[0] + initPos[0]*blockSize[0] + 78, boardInitPos[1] + initPos[1]*blockSize[1] + 78, 0.1)
                gui.click()
                gui.moveTo(boardInitPos[0] + finalPos[0]*blockSize[0] + 78, boardInitPos[1] + finalPos[1]*blockSize[1] + 78, 0.1)
                gui.click()
                
                justMoved = True

            prevBoard = currentBoard
