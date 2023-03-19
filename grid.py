import pygame
import os

letterX = pygame.image.load(os.path.join('im', 'equis.png'))
letterO = pygame.image.load(os.path.join('im', 'circulo.png'))
win = pygame.image.load(os.path.join('im', 'win.png'))
lose = pygame.image.load(os.path.join('im', 'lose.png'))
tie = pygame.image.load(os.path.join('im', 'tie.png'))

class Grid:

    def __init__(self):
        self.grid_lines = [((0,200),(600,200)), #primera horizontal
                           ((0,400),(600,400)), #segunda horizontal
                           ((200,0),(200,600)), #primera vertical
                           ((400,0),(400,600))] #segunda vertical
        
        self.grid = [[0 for x in range(3)] for y in range(3)] # creamos grid 3x3 en 2D
        self.switch_player = True
        # buscamos direcs     N        NO         O       SO       S       SE      E        NE     
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.game_over = False
        self.ganador = False
        self.empate = False
        
    def get_cell_value(self, x, y):
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value
    
    def get_mouse(self, x, y, player):
        if self.get_cell_value(x, y) == 0: # si la casilla esta vacia           
            self.set_cell_value(x, y, player)
            self.check_grid(x, y, player)
        else:
            self.switch_player = False

    def draw(self,surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (0,0,0), line[0], line[1], 2)

        for y in range(len(self.grid)): 
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    surface.blit(letterX, (x*200, y*200))
                elif self.get_cell_value(x, y) == "O":
                    surface.blit(letterO, (x*200, y*200))

    def win(self, surface):
        surface.blit(win, (0,0))

    def lose(self, surface):
        surface.blit(lose, (0,0))

    def tie(self, surface):
        surface.blit(tie, (0,0))

    def dentro_margenes(self, x, y):
        return 0 <= x < 3 and 0 <= y < 3

    def check_grid(self, x, y, player):

        count = 1 # ya tenemos una letra
       
        for index, (dirx, diry) in enumerate(self.search_dirs):
            if self.dentro_margenes(x+dirx, y+diry) and self.get_cell_value(x+dirx, y+diry) == player:
                count += 1
                
                xx = x + dirx
                yy = y + diry
                if self.dentro_margenes(xx+dirx, yy+diry) and self.get_cell_value(xx+dirx, yy+diry) == player:
                    count += 1
                    
                    if count == 3:
                        break
                if count < 3:
                    new_dir=0
                    if index == 0:
                        new_dir = self.search_dirs[4]  # N a S
                    elif index == 1:
                        new_dir = self.search_dirs[5]  # NO a SE
                    elif index == 2:
                        new_dir = self.search_dirs[6]  # O a E
                    elif index == 3:
                        new_dir = self.search_dirs[7]  # SO a NE
                    elif index == 4:
                        new_dir = self.search_dirs[0]  # S a N
                    elif index == 5:
                        new_dir = self.search_dirs[1]  # SE a NO
                    elif index == 6:
                        new_dir = self.search_dirs[2]  # E a O
                    elif index == 7:
                        new_dir = self.search_dirs[3]  # NE a SO
                    
                    if self.dentro_margenes(x + new_dir[0], y + new_dir[1]) and self.get_cell_value(x + new_dir[0], y + new_dir[1])== player:
                        count += 1
                        
                        if count == 3:
                            break
                    else:
                        count = 1
                        
        if count == 3:
            print(player, 'gana!')
            self.game_over = True
            self.ganador = True
            self.empate = False
        else:
            self.game_over = self.esta_llena()
            if self.esta_llena() == True:
                self.empate = True
   
    def esta_llena(self):
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        return True

    def clear(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
               self.set_cell_value(x, y, 0) 

    def print_grid(self):
        for row in self.grid:
            print(row)