import pygame
from grid import Grid
import threading
import socket


surface = pygame.display.set_mode((600,600))
pygame.display.set_caption('TRES EN RAYA                                                   JUGADOR 2')
HOST = '127.0.0.1'
PORT = 65432
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))
grid = Grid()
running  = True
player = "O"
turn = False
playing = 'True'
win = False
lose = False
tie = False


def crear_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

def recive():
    global turn
    while True:
        data = sock.recv(1024).decode() #metodo que bloquea
        data = data.split('-')
        x, y = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if data[4] == 'True':
            grid.empate = True
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, 'X')

crear_thread(recive)




while running:

    if grid.game_over:
        if grid.empate == True:
            grid.tie(surface)
            tie = True
        else: 
            if turn:
                grid.lose(surface)
                lose = True
            else:
                grid.win(surface)
                win = True
                
           
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed()[0]: #boton izquierdo del raton solo
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse( cellX, cellY, player)
                    if grid.game_over:
                        playing = 'False'
                    send_data = '{}-{}-{}-{}-{}'.format(cellX, cellY, 'yourturn', playing, grid.empate).encode()
                    sock.send(send_data)  
                    turn = False  

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear()
                grid.game_over = False
                playing = 'True'
                win = False
                lose = False
                tie = False
                grid.ganador = False
                grid.empate = False 
            elif event.key == pygame.K_ESCAPE:
                running = False

    if win == False and lose == False and tie == False:
        surface.fill((255,255,255)) # pintamos la ventana de color blanco
        grid.draw(surface)

    pygame.display.flip()
