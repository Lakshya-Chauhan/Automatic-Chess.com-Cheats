from os import system
import random
import pyautogui as gui
import time
from stockfish import Stockfish

stockfish = Stockfish(path = "<---Path of the Stockfish Exe--->", depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 3})

initPos = [None, None] #stores the position from where the pieces is picked (when move is made)
finalPos = [None, None] #stores the position of where the pieces is played (when move is made)
firstCheck = True #Checks if current iteration is first iteration of the loop
justMoved = False #Checks if in the last iteration of the main loop a move was made by the program
fullyMoved = False #In chess.com (even on fast animation) Pieces take about ~0.3 second time to move, if a change is detected on the board then it allows the piece to move completely (complete it's animation) and then check what the move was; to avoid error
selfColor = None #Stores the color assigned to the user in the chess game
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
                selfColor = 'white' #sets the color of the player to white
                stockfish.set_fen_position(initFen) #for white (as it makes the first move) the fen is initFen
                move = random.choice(["c2c4", "e2e4", "d2d4", "f2f4", "c2c3", "e2e3", "d2d3", "f2f3"]) #Choose randomly out of the following moves (Although f3 and f4 are not good moves and you can neglect them, Or you can keep them to disrespect your opponent)
                stockfish.make_moves_from_current_position([move]) #makes one of the random moves out of the above

                #getting the coordinates of the point of start and of end from the stockfish notation
                initPos[0] = ord(move[0])-97
                initPos[1] = 8-int(move[1])
                finalPos[0] = ord(move[2])-97
                finalPos[1] = 8-int(move[3])

                #simulating virtual clicks on the start point and at the end point thus making a move
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
            if fullyMoved == False: #Has the animation of movement of piece completed?
                time.sleep(0.3) #gives it enough time to complete
                fullyMoved = True #returns to the loop again to check the actual move that was made
                continue
            fullyMoved = False
            system("cls")
            print(selfColor)
            pieceMoves = list()  #stores the coordinates of opponent pieces that have changed their positions (both the position where they initially were and where they came after moving)
            for i in range(8):
                for j in range(8):
                    if prevBoard[i][j] != currentBoard[i][j]: #if the pieces on coordinates of current board and the board before the move was made are different
                        if selfColor == 'black' and ((prevBoard[i][j].isupper() == True) or (currentBoard[i][j].isupper() == True)): #checks if the piece that moved was an opponent piece
                            if initPos == [None, None] : initPos = [i, j] #stores the position first in initPos
                            else : finalPos = [i, j] #and later in finalPos
                            pieceMoves.append([i, j]) #appends the list with coordinate of opponent pieces that moved (be it initial or final)
                        elif (prevBoard[i][j].islower() == True) or (currentBoard[i][j].islower() == True): #checks if the piece that was moved was an opponent piece
                            if initPos == [None, None] : initPos = [i, j] #stores the position first in initPos
                            else : finalPos = [i, j] #and later in finalPos
                            pieceMoves.append([i, j]) #appends the list with coordinates of opponent pieces that moved (be it initial or final)
                        
                    print(currentBoard[j][i], end=" ")
                print()
            
            if len(pieceMoves) == 4: #if number of such positions are 4 means there are two inital and two final positions which can only happen in the case of castling
                print("\<----        nCastles!!         ---->\n")
                for i in range(4):
                    for j in range(4):
                        #since stockfish represents castling as a move of the king we identify the initial position and final position of the king out of the two neglecting the rook's position
                        if (i!=j) and (currentBoard[pieceMoves[i][0]][pieceMoves[i][1]] == prevBoard[pieceMoves[j][0]][pieceMoves[j][1]]) and (currentBoard[pieceMoves[i][0]][pieceMoves[i][1]].lower() == 'k'):
                            initPos = pieceMoves[i]
                            finalPos = pieceMoves[j]
                            print("<----   ", pieceMoves[i], pieceMoves[j], "   ---->")

            print(initPos, finalPos, len(pieceMoves))
            if initPos != [None, None]:
                if selfColor == 'black':
                    #Arranges the moves correctly (if not); Makes initPos store the initial position (as it is not necessary for the first position to encountered in the above loop logic to be initial position) and finalPos store final position
                    if prevBoard[initPos[0]][initPos[1]].isupper() != True: 
                        initPos, finalPos = finalPos, initPos

                    #Converts the position from tuples to stockfish notation of the move (for black)
                    initPos[0] = chr(104-initPos[0])
                    initPos[1] = str(initPos[1]+1)
                    finalPos[0] = chr(104-finalPos[0])
                    finalPos[1] = str(finalPos[1]+1)
                else:
                    #Arranges the moves correctly (if not); Makes initPos store the initial position (as it is not necessary for the first position to encountered in the above loop logic to be initial position) and finalPos store final position
                    if prevBoard[initPos[0]][initPos[1]].islower() != True:
                        initPos, finalPos = finalPos, initPos

                    #Converts the position from tuples to stockfish notation for move (for white)
                    initPos[0] = chr(97+initPos[0])
                    initPos[1] = str(8-initPos[1])
                    finalPos[0] = chr(97+finalPos[0])
                    finalPos[1] = str(8-finalPos[1])

                move = initPos[0] + initPos[1] + finalPos[0] + finalPos[1] #stores in form of string so that it can be given as input easily to stockfish
                print(move)

                stockfish.make_moves_from_current_position([move])
                bestMove = stockfish.get_best_move()

                #getting the coordinates of the point of start and of end from the stockfish notation
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

                #simulating virtual clicks on the start point and at the end point thus making a move
                gui.moveTo(boardInitPos[0] + initPos[0]*blockSize[0] + 78, boardInitPos[1] + initPos[1]*blockSize[1] + 78, 0.1)
                gui.click()
                gui.moveTo(boardInitPos[0] + finalPos[0]*blockSize[0] + 78, boardInitPos[1] + finalPos[1]*blockSize[1] + 78, 0.1)
                gui.click()
                
                justMoved = True

            prevBoard = currentBoard
