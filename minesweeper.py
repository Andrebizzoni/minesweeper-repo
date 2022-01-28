import random as rd
import pygame
from pygame import display
from pygame.constants import *
from pygame.locals import *
import math


HEIGHT = 16
WIDTH = 30
NUM_BOMBS = 50


class Board:
    def __init__(self):
        self.dug = set()
        self.board = [[None for i in range(WIDTH)] for i in range(HEIGHT)]
        self.plant_bombs()
        self.assign_values_to_board()
        
    def plant_bombs(self):
        bomb_count = 0
        while bomb_count < NUM_BOMBS:
            row = rd.randint(0, HEIGHT-1)
            col = rd.randint(0, WIDTH-1)
            if self.board[row][col] != '*':
                self.board[row][col] = '*'
                bomb_count += 1

    def assign_values_to_board(self):
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.board[row][col] == "*":
                    continue
                self.board[row][col] = self.count_num_neighboring_bombs(row, col)
                
    def count_num_neighboring_bombs(self, row, col):
        neighbouring_bomb_count = 0
        for r in range(max(0, row-1), min(HEIGHT, row+2)):
            for c in range(max(0, col-1), min(WIDTH, col+2)):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    neighbouring_bomb_count += 1
        return neighbouring_bomb_count


class Visible_board:
    def __init__(self, surface, board):
        self.board = board
        self.surface = surface
        self.dug = set()
        self.flagged_mines = set()
        self.face_down = pygame.image.load("facingDown.png").convert()
        self.zero = pygame.image.load("0.png").convert()
        self.one = pygame.image.load("1.png").convert()
        self.two = pygame.image.load("2.png").convert()
        self.three = pygame.image.load("3.png").convert()
        self.four = pygame.image.load("4.png").convert()
        self.five = pygame.image.load("5.png").convert()
        self.six = pygame.image.load("6.png").convert()
        self.seven = pygame.image.load("7.png").convert()
        self.eight = pygame.image.load("8.png").convert()
        self.bomb = pygame.image.load("bomb_2.png").convert()
        self.flagged = pygame.image.load("flagged.png").convert()
        self.wrong_bomb = pygame.image.load("wrong_bomb.png").convert()
        self.correct_bomb = pygame.image.load("correct_bomb.png").convert()

    def generate_visible_board(self):
        self.x, self.y = [], []
        for i in range(0, 480, 30):
            for j in range(0, 900, 30):
                self.x.append(j)
                self.y.append(i)
        for i in range(len(self.x)):
            self.surface.blit(self.face_down, (self.x[i], self.y[i]))
        pygame.display.update()
    
    def dig(self, row, col):
        self.dug.add((row, col))
        if self.board[row][col] == '*' or self.board[row][col] in range(1, 9):
            return self.draw(row, col)
        for r in range(max(0, row-1), min(HEIGHT, row+2)):
            for c in range(max(0, col-1), min(WIDTH, col+2)):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return self.draw(row, col)
        
    def draw(self, row, col):
        if self.board[row][col] == '*':
            self.surface.blit(self.bomb, (col*30, row*30))
            pygame.display.update()
            return False
        elif self.board[row][col] == 0:
            self.surface.blit(self.zero, (col*30, row*30))
        elif self.board[row][col] == 1:
            self.surface.blit(self.one, (col*30, row*30))
        elif self.board[row][col] == 2:
            self.surface.blit(self.two, (col*30, row*30))
        elif self.board[row][col] == 3:
            self.surface.blit(self.three, (col*30, row*30))
        elif self.board[row][col] == 4:
            self.surface.blit(self.four, (col*30, row*30))
        elif self.board[row][col] == 5:
            self.surface.blit(self.five, (col*30, row*30))
        elif self.board[row][col] == 6:
            self.surface.blit(self.six, (col*30, row*30))
        elif self.board[row][col] == 7:
            self.surface.blit(self.seven, (col*30, row*30))
        elif self.board[row][col] == 8:
            self.surface.blit(self.eight, (col*30, row*30))
        pygame.display.update()
        return True
    
    def get_pos(self):
        y, x = pygame.mouse.get_pos()
        x //= 30
        y //= 30
        return x, y
    
    def flag(self, row, col):
        if (row, col) not in self.dug:
            self.flagged_mines.add((row, col))
            self.surface.blit(self.flagged, (col*30, row*30))
            pygame.display.update()

    def is_complete_tile(self, row, col):
        count = 0
        for r in range(max(0, row-1), min(HEIGHT, row+2)):
            for c in range(max(0, col-1), min(WIDTH, col+2)):
                if self.board[r][c] == "*" and (r, c) in self.flagged_mines:
                    count += 1
        if count == self.board[row][col]:
            return True
    
    def complete_tile(self, row, col):
        for r in range(max(0, row-1), min(HEIGHT, row+2)):
            for c in range(max(0, col-1), min(WIDTH, col+2)):  
                if (r, c) not in self.dug and (r, c) not in self.flagged_mines:
                    self.dig(r, c)

    def is_correct_tile(self, row, col):
        for r in range(max(0, row-1), min(HEIGHT, row+2)):
            for c in range(max(0, col-1), min(WIDTH, col+2)):
                if (r, c) in self.flagged_mines and self.board[r][c] != '*':
                    return False
        return True
                    
    def remove_flag(self, row, col):
        self.flagged_mines.remove((row, col))
        self.surface.blit(self.face_down, (col*30, row*30))
        pygame.display.update()

    def is_flagged(self, row, col):
        if (row, col) in self.flagged_mines:
            return True
        return False
    
    def is_win(self):
        if len(self.dug) == (HEIGHT * WIDTH) - NUM_BOMBS:
            return True
        return False

    def show_win(self):
        font = pygame.font.SysFont('chicago', 40)
        line1 = font.render("You win!", True, (0,0,0))
        self.surface.blit(line1, (WIDTH*30/2 - 50, HEIGHT*30/2 - 15))
        pygame.display.update()

    def show_game_over(self, row, col):
        for r in range(0, HEIGHT):
            for c in range(0, WIDTH):
                if self.board[r][c] == '*':
                    self.surface.blit(self.bomb, (c*30, r*30))
        self.surface.blit(self.correct_bomb, (col*30, row*30))            
        pygame.display.update()
    
    def show_game_over_2(self, row, col):
        for r in range(0, HEIGHT):
            for c in range(0, WIDTH):
                if self.board[r][c] == '*':
                    self.surface.blit(self.bomb, (c*30, r*30))

        for r in range(max(0, row-1), min(HEIGHT, row+2)):
            for c in range(max(0, col-1), min(WIDTH, col+2)):
                if (r, c) in self.flagged_mines and self.board[r][c] != '*':
                    self.surface.blit(self.wrong_bomb, (c*30, r*30))
                elif (r, c) not in self.flagged_mines and self.board[r][c] == '*':
                    self.surface.blit(self.correct_bomb, (c*30, r*30))
        pygame.display.update()

class Game:
    def __init__(self):
        #initialize pygame
        pygame.init()
        #create surface
        self.surface = pygame.display.set_mode((900, 480))
        #create board object
        self.board = Board()
        #create visible board object
        self.visible_board = Visible_board(self.surface, self.board.board)

    def run(self):
        self.visible_board.generate_visible_board()
        game_over = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE and not game_over:
                            x, y = self.visible_board.get_pos()
                            if self.visible_board.is_flagged(x, y):
                                self.visible_board.remove_flag(x, y)
                                continue
                            elif self.visible_board.is_complete_tile(x, y):
                                self.visible_board.complete_tile(x, y)
                            elif not self.visible_board.is_correct_tile(x, y):
                                game_over = True
                                self.visible_board.show_game_over_2(x, y)
                            else:
                                self.visible_board.flag(x, y)
                elif event.type == MOUSEBUTTONUP and not game_over:
                    x, y = self.visible_board.get_pos()
                    if not self.visible_board.dig(x, y):
                            game_over = True
                            self.visible_board.show_game_over(x, y)
                elif event.type == QUIT:
                    running = False
                elif self.visible_board.is_win():
                    self.visible_board.show_win()
                    game_over = True


if __name__ == "__main__":
    game = Game()
    game.run()