from curses.ascii import isupper
from random import randint
import pyautogui as pg
import cv2 as cv
from time import sleep
import numpy as np

white_turn = True
match_result = None
all_steps = []

white_coordinates = {}
black_coordinates = {}

cell_size = 50

chess_matrix = np.array(
    [   # 0   1   2   3   4   5   6   7
        ['r','n','b','q','k','b','n','r'],  # 8
        ['p','p','p','p','p','p','p','p'],  # 7
        ['.','.','.','.','.','.','.','.'],  # 6
        ['.','.','.','.','.','.','.','.'],  # 5
        ['.','.','.','.','.','.','.','.'],  # 4
        ['.','.','.','.','.','.','.','.'],  # 3
        ['P','P','P','P','P','P','P','P'],  # 2
        ['R','N','B','Q','K','B','N','R']   # 1
        # a   b   c   d   e   f   g   h
    ],
    dtype='<U1'
)

def initialize():
    global cell_size
    screenshot = pg.screenshot()
    screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

    # Initiating white_coordinates
    white_board = pg.locateOnScreen("res/white_board.png")
    init_x = white_board.left + (cell_size/2)
    init_y = white_board.top + (cell_size/2)
    for alp in range (97, 105):
        init_y = white_board.top + (cell_size/2)
        for num in range(8,0,-1):
            key = chr(alp) + str(num)
            val = (init_x, init_y)
            white_coordinates[key] = val
            init_y += cell_size
        init_x += cell_size
    
    # Initiating black_coordinates
    black_board = pg.locateOnScreen("res/black_board.png")
    init_x = black_board.left + (cell_size/2)
    init_y = black_board.top + (cell_size/2)
    for alp in range (104,96,-1):
        init_y = black_board.top + (cell_size/2)
        for num in range(1,9):
            key = chr(alp) + str(num)
            val = (init_x, init_y)
            black_coordinates[key] = val
            init_y += cell_size
        init_x += cell_size

def cvt_chess_to_index(notation):
    matrix_row = 8-int(notation[1])
    matrix_col = ord(notation[0]) - ord('a')
    return (matrix_row, matrix_col)

def cvt_index_to_chess(index):
    row = 8 - index[0]
    file = chr(index[1] + ord('a'))
    return str(file) + str(row)

def update_matrix(init, dest, castle):
    init = cvt_chess_to_index(init)
    destt = cvt_chess_to_index(dest)

    chess_matrix[destt[0]][destt[1]] = chess_matrix[init[0]][init[1]]
    chess_matrix[init[0]][init[1]] = '.'

    if (castle):
        if dest == "g1" or dest == "g8":
            # short castle
            chess_matrix[destt[0]][5] = chess_matrix[init[0]][7]
            chess_matrix[init[0]][7] = '.'


        if dest == "c1" or dest == "c8":
            # long castle
            chess_matrix[destt[0]][3] = chess_matrix[init[0]][0]
            chess_matrix[init[0]][0] = '.'

def mov(init, dest, castle = False):
    first_click = white_coordinates[init] if (white_turn) else black_coordinates[init]
    second_click = white_coordinates[dest] if (white_turn) else black_coordinates[dest]
    pg.click(x=first_click[0], y=first_click[1])
    sleep(0.25)
    pg.click(x=second_click[0], y=second_click[1])
    update_matrix(init, dest, castle)

def inBetween(init, dest, diffrow, difffile):
    init = cvt_chess_to_index(init)
    dest = cvt_chess_to_index(dest)

    if (diffrow == 0):
        col = min(init[1], dest[1])+1
        while(col < max(init[1], dest[1])):
            if (chess_matrix[init[0]][col] != '.'): return False
            col+=1
        return True
    if (difffile == 0):
        row = min(init[0], dest[0])+1
        while(row < max(init[0], dest[0])):
            if (chess_matrix[row][init[1]] != '.'): return False
            row+=1
        return True

def isPossibleMove(piece, init, dest):
    diffrow = abs(ord(dest[1]) - ord(init[1]))
    difffile = abs(ord(dest[0]) - ord(init[0]))

    if piece == 'b' or piece == 'B':
        return diffrow == difffile
    elif piece == "n" or piece == "N":
        return ((diffrow == 2 and difffile == 1) or (diffrow == 1 and difffile == 2))
    elif piece == "r" or piece == "R":
        return ((diffrow == 0) or (difffile == 0)) and inBetween(init, dest, diffrow, difffile)
    else:
        return True

def calc_mov(piece, dest, init_row = None, init_file = None):
    piece = piece.upper() if (white_turn) else piece.lower()
    if (piece == 'p' or piece == 'P'):
        init = init_file if (init_file != None) else dest[0]
        init = init + str(int(dest[1])-1) if (white_turn) else init + str(int(dest[1])+1)
        check_index = cvt_chess_to_index(init)
        if (chess_matrix[check_index[0]][check_index[1]] == '.'):
            init = init[0] + str(int(init[1])-1) if (white_turn) else init[0] + str(int(init[1])+1)
        return init

    init = np.where(chess_matrix == piece)
    initlist = [None]*len(init[0])
    for i in range(len(init[0])):
        initlist[i] = (init[0][i], init[1][i])
        initlist[i] = cvt_index_to_chess(initlist[i])
        if (init_file != None and init_file in initlist[i]): return initlist[i]
        if (init_row != None and init_row in initlist[i]): return initlist[i]
        if (init_file == None and init_row == None and isPossibleMove(piece, initlist[i], dest)): return initlist[i]

def read_step(step):
    piece = 'p'
    dest_file = ""
    dest_row = ""

    if (step == "0-0" or step == "O-O"):
        # short castle
        initial = "e1" if (white_turn) else "e8"
        dest = "g1" if (white_turn) else "g8"
        mov(initial, dest, True)
        return

    if (step == "0-0-0" or step == "O-O-O"):
        # long castle
        initial = "e1" if (white_turn) else "e8"
        dest = "c1" if (white_turn) else "c8"
        mov(initial, dest, True)
        return

    init_file = None
    init_row = None

    for chr in step:
        if isupper(chr):
            piece = chr
        if chr >= 'a' and chr <= 'h':
            if dest_file == "":
                dest_file = chr
            else:
                init_file = dest_file
                dest_file = chr
        if chr >= '1' and chr <= '8':
            if dest_row == "":
                dest_row = chr
            else:
                init_row = dest_row
                dest_row = chr

    dest = dest_file + dest_row
    init = None

    init = calc_mov(piece, dest, init_row, init_file)

    mov(init,dest)

def read_input():
    f = open("input.txt", "r")
    str = f.read()
    global all_steps, match_result
    word = ""
    steps = []
    for c in str:
        if (c == ' '):
            if '.' in word:
                word = ""
                continue
            if (word == "1/2-1/2"): match_result = 0
            elif (word == "1-0"): match_result = 1
            elif (word == "0-1"): match_result = -1
            else:
                steps.append(word)
                word = ""
                if (len(steps) == 2):
                    all_steps.append(steps)
                    steps = []
        else:
            word = word + c
    if (len(steps) != 0): all_steps.append(steps)
    f.close()

def endgame():
    if (match_result == 0):
        # sending draw request
        screenshot = pg.screenshot()
        screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
        draw = pg.locateCenterOnScreen('res/draw.png')
        pg.doubleClick(x=draw.x, y=draw.y, interval=1)

        # accepting draw request
        screenshot = pg.screenshot()
        screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
        accept = pg.locateCenterOnScreen('res/accept_draw.png')
        pg.click(x = accept.x, y = accept.y)
        
    elif (match_result == 1 or match_result == -1):
        screenshot = pg.screenshot()
        screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
        for resign in pg.locateAllOnScreen('res/resign.png'):
            if (match_result == 1):
                # white wins, black resigns
                if (abs(resign.left - black_coordinates["a6"][0]) < abs(resign.left - white_coordinates["h3"][0])):
                    pg.click(x = resign.left + (resign.width/2), y = resign.top + (resign.height/2), clicks=2, interval=2)
            else:
                # black wins, white resigns
                if (abs(resign.left - black_coordinates["a6"][0]) > abs(resign.left - white_coordinates["h3"][0])):
                    pg.click(x = resign.left + (resign.width/2), y = resign.top + (resign.height/2), clicks=2, interval=2)

def main():
    global white_turn
    read_input()
    for i in range(5,0,-1):
        print("Starting in", i)
        sleep(1)

    initialize()
    global all_steps
    for row in all_steps:
        for step in row:
            read_step(step)
            white_turn = not white_turn
            print(chess_matrix)
            print("\n\n\n")
            sleep(0.5)
            # sleep(60 + randint(-5,15))

    endgame()

main()