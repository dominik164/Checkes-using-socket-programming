import pygame
from colors import *
from pion import *


class Board():
    def __init__(self):
        self.board = [[0 for x in range(8)] for _ in range(8)]
        self.white_pions_number = 12
        self.grey_pions_number = 12
    # drawing board

    def draw_white_squares(self, win):
        win.fill(WHITE)
        for i in range(8):
            for j in range(i % 2, 8, 2):
                pygame.draw.rect(win, BLACK, (i*80, (j*80)+60, 80, 80))

    def create_board(self):
        for i in range(0, 8, 2):
            for j in range(3):
                if j % 2 != 0:
                    self.board[i+1][j] = Pion(i+1, j, GREY)
                else:
                    self.board[i][j] = Pion(i, j, GREY)
            for j in range(5, 8):
                if j % 2 != 0:
                    self.board[i+1][j] = Pion(i+1, j, WHITE)
                else:
                    self.board[i][j] = Pion(i, j, WHITE)
    # drawing pions

    def draw(self, win):
        self.draw_white_squares(win)
        for i in range(8):
            for j in range(8):
                pion = self.board[i][j]
                if pion != 0:
                    pion.draw_pion(win)
        pygame.display.update()

    def move_pion(self, pion, x, y):
        self.board[x][y] = self.board[pion.x][pion.y]
        self.board[pion.x][pion.y] = 0
        pion.move(x, y)

    def possible_capture(self, pion, x, y):
        moves = {}
        key, value = x, y
        if pion.color == WHITE and pion.y > 1:
            if pion.x > 5:
                if self.board[pion.x-1][pion.y-1] != 0 and self.board[pion.x-1][pion.y-1].color == GREY and self.board[pion.x-2][pion.y-2] == 0:
                    return True
            else:
                if self.board[pion.x-1][pion.y-1] != 0 and self.board[pion.x-1][pion.y-1].color == GREY and self.board[pion.x-2][pion.y-2] == 0:
                    m = {pion.x-2: pion.y-2}
                    moves.update(m)
                if self.board[pion.x+1][pion.y-1] != 0 and self.board[pion.x+1][pion.y-1].color == GREY and self.board[pion.x+2][pion.y-2] == 0:
                    m = {pion.x+2: pion.y-2}
                    moves.update(m)
        elif pion.color == GREY and pion.y < 6:
            if pion.x > 5:
                if self.board[pion.x-1][pion.y+1] != 0 and self.board[pion.x-1][pion.y+1].color == WHITE and self.board[pion.x-2][pion.y+2] == 0:
                    return True
            else:
                if self.board[pion.x-1][pion.y+1] != 0 and self.board[pion.x-1][pion.y+1].color == WHITE and self.board[pion.x-2][pion.y+2] == 0:
                    m = {pion.x-2: pion.y+2}
                    moves.update(m)
                if pion.x < 6 and self.board[pion.x+1][pion.y+1] != 0 and self.board[pion.x+1][pion.y+1].color == WHITE and self.board[pion.x+2][pion.y+2] == 0:
                    m = {pion.x+2: pion.y+2}
                    moves.update(m)
        if key in moves and value == moves[key]:
            return True
    # moves without capture

    def possible_moves_wo(self, pion, x, y):
        moves = {}
        key, value = x, y
        if pion.queen == True:
            i = pion.x
            j = pion.y
            while i < 8 and j < 8:
                if self.board[i][j] == 0:
                    m = {i: j}
                    moves.update(m)
                i += 1
                j += 1
            i = pion.x
            j = pion.y
            while i >= 0 and j >= 0:
                if self.board[i][j] == 0:
                    m = {i: j}
                    moves.update(m)
                i -= 1
                j -= 1
            i = pion.x
            j = pion.y
            while i < 8 and j >= 0:
                if self.board[i][j] == 0:
                    m = {i: j}
                    moves.update(m)
                i += 1
                j -= 1
            i = pion.x
            j = pion.y
            while i >= 0 and j < 8:
                if self.board[i][j] == 0:
                    m = {i: j}
                    moves.update(m)
                i -= 1
                j += 1
        elif pion.color == WHITE:
            if self.board[pion.x-1][pion.y-1] == 0:
                if pion.x == 7:
                    return True
                m = {pion.x-1: pion.y-1}
                moves.update(m)
            if self.board[pion.x+1][pion.y-1] == 0:
                m = {pion.x+1: pion.y-1}
                moves.update(m)
        elif pion.color == GREY:
            if self.board[pion.x-1][pion.y+1] == 0:
                if pion.x == 7:
                    return True
                m = {pion.x-1: pion.y+1}
                moves.update(m)
            if pion.y < 7 and self.board[pion.x+1][pion.y+1] == 0:
                m = {pion.x+1: pion.y+1}
                moves.update(m)
        if key in moves and value == moves[key]:
            return True
    # removing captured pions

    def remove(self, pion, x, y):
        if pion.color == WHITE:
            if x > pion.x:
                self.board[x-1][y+1] = 0
            else:
                self.board[x+1][y+1] = 0
            self.grey_pions_number -= 1
        else:
            if x > pion.x:
                self.board[x-1][y-1] = 0
            else:
                self.board[x+1][y-1] = 0
            self.white_pions_number -= 1
    # determing victory

    def victory(self, win):
        if self.white_pions_number == 0:
            pygame.draw.rect(win, WHITE, (0, 0, 640, 60))
            pygame.display.update()
            font_1.render_to(win, (250, 10),
                             "GREY WIN", (3, 169, 242))
            pygame.display.flip()
        elif self.grey_pions_number == 0:
            pygame.draw.rect(win, WHITE, (0, 0, 640, 60))
            pygame.display.update()
            font_1.render_to(win, (250, 10),
                             "WHITE WIN", (3, 169, 242))
            pygame.display.flip()
