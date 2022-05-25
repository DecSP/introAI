# ------------- INITIALIZATIONS-------------------
from cmath import isfinite
from operator import truediv
from platform import python_branch
import pygame
import chess
import chess.svg
import random
import sys
from svglib.svglib import svg2rlg
import io

import AI
from threading import Thread

pygame.init()  # essential for pygame
pygame.font.init()  # for text

# define display surface
screen = pygame.display.set_mode((800, 60 * 8))
pygame.display.set_caption('Python Chess Game')

# load images
bg = pygame.image.load("assets/chessboard.png").convert()
sidebg = pygame.image.load("assets/woodsidemenu.jpg").convert()
myfont = pygame.font.Font("assets/Roboto-Black.ttf", 30)
clippy = pygame.image.load("assets/Clippy.png").convert_alpha()
clippy = pygame.transform.scale(clippy, (320, 240))
playeravatar = None

# necessary for capping the game at 60FPS
clock = pygame.time.Clock()

board = chess.Board()

mode = 0
difficult = 0
player = 1  # 'AI' for the computer player
goFirst = True

def get_board_image(first, piece = None):
    if piece == None and first:
        boardsvg = chess.svg.board(board,size=1800)
    elif piece == None and not first:
        boardsvg = chess.svg.board(board,size=1800, orientation=chess.BLACK)
    elif piece != None and first:
        boardsvg = chess.svg.board(board=board, fill={chess.parse_square(piece): "#00cc00cc"}, size=1800)
    else:
        boardsvg = chess.svg.board(board=board, orientation=chess.BLACK, fill={chess.parse_square(piece): "#00cc00cc"}, size=1800)
    f = open("image.svg", "w")
    f.write(boardsvg)
    f.close()

    drawing = svg2rlg('image.svg')
    str = drawing.asString("png")
    byte_io = io.BytesIO(str)

    boardImage = pygame.image.load(byte_io).convert_alpha()
    boardImage = pygame.transform.scale(boardImage, (480, 480))
    return boardImage

def select_piece(board, first):
    x, y = pygame.mouse.get_pos()
    if x > 460 or y > 460 or x < 20 or y < 20:
        return None
    x = (x - 20) // 55
    y = 7 - ((y - 20) // 55)
    if not first:
        x = 7 - x
        y = 7 - y
    piece = board.piece_at(y*8 + x)
    if piece == None:
        return None
    if piece.color != first:
        return None
    row = ['a','b','c','d','e','f','g','h']
    return row[x] + str(y + 1)
    
def select_square(board, first):
    x, y = pygame.mouse.get_pos()
    if x > 460 or y > 460 or x < 20 or y < 20:
        return None
    x = (x - 20) // 55
    y = 7 - ((y - 20) // 55)
    if not first:
        x = 7 - x
        y = 7 - y
    row = ['a','b','c','d','e','f','g','h']
    return row[x] + str(y + 1)

def run_game():

    global player, playeravatar, clippy
    playeravatar = pygame.image.load("assets/avatar.png").convert_alpha()
    playeravatar = pygame.transform.scale(playeravatar, (320, 240))
    update_sidemenu('Your Turn!', (255, 255, 255))
    screen.blit(get_board_image(goFirst), (0, 0))
    update = True

    selected = False
    pieceSelected = ''
    isfinish = False

    while not board.is_checkmate() and not isfinish:
        if player == 1:
            if len(list(board.legal_moves)) == 0:
                update_sidemenu('You have no legal move!\nCPU Win!\nPress any key to quit.', (255, 255, 0))
                player = 'AI'
                update = True
                isfinish = True
                continue

            if mode == 1:
                thread=Thread(target=AI.minimaxroot2,args=(3, board, True, not goFirst,))
                AI.bestMove=None
                thread.start()
                while True:
                    if AI.bestMove is not None: break
                    pygame.event.get()
                    clock.tick(60)
                # move = random.choice(list(board.legal_moves))
                move = AI.bestMove
                board.push(move)
                if board.is_checkmate():
                    update_sidemenu('Checkmate!\nYou Win!\nPress any key to quit.', (255, 255, 0))
                else:
                    player = 'AI'
                screen.blit(get_board_image(goFirst), (0, 0))
                update = True

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and not selected:
                        piece = select_piece(board, goFirst)
                        if piece != None: 
                            selected = True
                            pieceSelected = piece

                            screen.blit(get_board_image(goFirst, piece), (0, 0))
                            update = True

                    elif event.type == pygame.MOUSEBUTTONDOWN and selected:
                        piece = select_square(board, goFirst)
                        if piece == None:
                            continue
                        if piece == pieceSelected:
                            selected = False
                            screen.blit(get_board_image(goFirst), (0, 0))
                            update = True
                        else:
                            move = chess.Move.from_uci(pieceSelected+piece)
                            smove = chess.Move.from_uci(pieceSelected+piece+'q')
                            if move in board.legal_moves or smove in board.legal_moves:
                                selected = False
                                if move in board.legal_moves:
                                    board.push(move)
                                else:
                                    board.push(smove)
                                if board.is_checkmate():
                                    update_sidemenu('Checkmate!\nYou Win!\nPress any key to quit.', (255, 255, 0))
                                else:
                                    player = 'AI'
                                    update_sidemenu('CPU Thinking...', (255, 255, 255))
                                screen.blit(get_board_image(goFirst), (0, 0))
                                update = True
                            else:
                                update_sidemenu('Invalid move!', (255, 0, 0))
                                update = True


        elif player == 'AI':
            if len(list(board.legal_moves)) == 0:
                update_sidemenu('CPU have no legal move!\nYou Win!\nPress any key to quit.', (255, 255, 0))
                player = 1
                update = True
                isfinish = True
                continue
            
            thread=Thread(target=AI.minimaxroot,args=(difficult, board, True, goFirst,))
            AI.bestMove=None
            thread.start()
            while True:
                if AI.bestMove is not None: break
                pygame.event.get()
                clock.tick(60)
            
            board.push(AI.bestMove)
            if board.is_checkmate():
                update_sidemenu('Checkmate!\nCPU Wins!\nPress any key to quit.', (255, 255, 0))
            else:
                player = 1
                update_sidemenu('Your Turn!', (255, 255, 255))
            screen.blit(get_board_image(goFirst), (0, 0))
            update = True

        if update:
            pygame.display.update()
            update = False
        clock.tick(60)



def game_over():
    '''
    This runs before the game quits. A nice game over screen.
    '''
    import os
    crown = pygame.image.load("assets/crown.png").convert_alpha()
    crown = pygame.transform.scale(crown, (80, 60))
    screen.blit(crown, (520, 20))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.event.clear()
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                return
            elif event.type == pygame.QUIT:
                import sys
                sys.exit()

    os.remove('assets/avatar.png')


def update_sidemenu(message, colour):
    '''
    Allows the side menu to be updated with a custom message and colour in the rgb(x,x,x) format
    \n characters can be passed in manually to print a new line below.
    '''

    screen.blit(sidebg, (480, 0))  # update side menu background
    global playeravatar, clippy

    # blit current player's avatar
    if player == 1:
        screen.blit(playeravatar, (480, 0))

    elif player == 'AI':
        screen.blit(clippy, (480, 0))

    # separate text by \n and print as additional lines if needed
    message = message.splitlines()
    c = 0
    for m in message:
        textsurface = myfont.render(m, False, colour)
        screen.blit(textsurface, (500, 250 + c))
        c += 40


def camstream():
    '''
    The bulk of the camera code was not written by us, since it's just here for fun
    and does not contribute to the actual game in any meaningful way.
    We use this to make a avatar for the user on the fly
    modified from https://gist.github.com/snim2/255151
    works only in linux, or by installing some dependency in windows [not tested]
    '''
    try:
        DEVICE = '/dev/video0'
        SIZE = (640, 480)
        FILENAME = 'assets/avatar.png'
        import pygame.camera
        pygame.camera.init()
        display = pygame.display.set_mode((800, 60 * 8), 0)
        camera = pygame.camera.Camera(DEVICE, SIZE)
        camera.start()
        screen = pygame.surface.Surface(SIZE, 0, display)
        screen = camera.get_image(screen)
        pygame.image.save(screen, FILENAME)
        camera.stop()
        return
    except:
        # if camera fails to take a picture, use backup generic avatar
        from shutil import copyfile
        copyfile('assets/backupavatar.png', 'assets/avatar.png')


def welcome():
    '''
    Display a welcome screen.
    This mostly is just blitting a bunch of surfaces in the right spot.
    '''
    global mode, goFirst, player

    # wood background
    menubg = pygame.image.load("assets/menubg.jpg").convert()
    screen.blit(menubg, (0, 0))
    bigfont = pygame.font.Font("assets/Roboto-Black.ttf", 80)
    textsurface = bigfont.render('Python Chess Game', False, (255, 255, 255))
    screen.blit(textsurface, (30, 10))

    pve_button = pygame.draw.rect(screen,(204,149,68),(250,180,300,50))
    textsurface = myfont.render("PvE - GO FIRST", False, (255, 255, 255))
    screen.blit(textsurface, (300, 190))

    pve_button = pygame.draw.rect(screen,(204,149,68),(250,250,300,50))
    textsurface = myfont.render("PvE - GO SECOND", False, (255, 255, 255))
    screen.blit(textsurface, (280, 260))

    eve_button = pygame.draw.rect(screen,(204,149,68),(250,320,300,50))
    textsurface = myfont.render("EvE - GO FIRST", False, (255, 255, 255))
    screen.blit(textsurface, (300, 330))

    eve_button = pygame.draw.rect(screen,(204,149,68),(250,390,300,50))
    textsurface = myfont.render("EvE - GO SECOND", False, (255, 255, 255))
    screen.blit(textsurface, (280, 400))


    # infinite loop until player wants to begin
    pygame.display.update()
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 250 <= mouse[0] <= 550:
                    if 180 <= mouse[1] <= 230:
                        mode = 0
                        goFirst = True
                        player = 1
                        return
                    elif 250 <= mouse[1] <= 300:
                        mode = 0
                        goFirst = False
                        player = 'AI'
                        return
                    elif 320 <= mouse[1] <= 370:
                        mode = 1
                        goFirst = True
                        player = 1
                        return
                    elif 390 <= mouse[1] <= 440:
                        mode = 1
                        goFirst = False
                        player = 'AI'
                        return

        mouse = pygame.mouse.get_pos()


def select_difficult():
    '''
    Display a welcome screen.
    This mostly is just blitting a bunch of surfaces in the right spot.
    '''
    global difficult
    
    # wood background
    menubg = pygame.image.load("assets/menubg.jpg").convert()
    screen.blit(menubg, (0, 0))
    bigfont = pygame.font.Font("assets/Roboto-Black.ttf", 80)
    textsurface = bigfont.render('Python Chess Game', False, (255, 255, 255))
    screen.blit(textsurface, (30, 10))

    easy_button = pygame.draw.rect(screen,(204,149,68),(250,130,300,50))
    textsurface = myfont.render("EASY", False, (255, 255, 255))
    screen.blit(textsurface, (365, 140))

    easy_button = pygame.draw.rect(screen,(204,149,68),(250,200,300,50))
    textsurface = myfont.render("NORMAL", False, (255, 255, 255))
    screen.blit(textsurface, (345, 210))

    normal_button = pygame.draw.rect(screen,(204,149,68),(250,270,300,50))
    textsurface = myfont.render("HARD", False, (255, 255, 255))
    screen.blit(textsurface, (365, 280))

    hard_button = pygame.draw.rect(screen,(204,149,68),(250,340,300,50))
    textsurface = myfont.render("INSANE", False, (255, 255, 255))
    screen.blit(textsurface, (350, 350))

    insane_button = pygame.draw.rect(screen,(204,149,68),(250,410,300,50))
    textsurface = myfont.render("MASTER", False, (255, 255, 255))
    screen.blit(textsurface, (345, 420))


    # infinite loop until player wants to begin
    pygame.display.update()
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 250 <= mouse[0] <= 550:
                    if 130 <= mouse[1] <= 180:
                        difficult = 1
                        return
                    elif 200 <= mouse[1] <= 250:
                        difficult = 2
                        return
                    elif 270 <= mouse[1] <= 320:
                        difficult = 3
                        return
                    elif 340 <= mouse[1] <= 390:
                        difficult = 4
                        return
                    elif 410 <= mouse[1] <= 460:
                        difficult = 5
                        return

        mouse = pygame.mouse.get_pos()


if __name__ == "__main__":
    welcome()
    select_difficult()
    camstream()
    run_game()
    game_over()
