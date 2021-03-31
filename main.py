import pygame
from board import Board
from colors import *

WIDTH = 640
HEIGHT = 700


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Warcaby')


def get_pion_position(pos):
    x, y = pos
    x = x // 80
    y = y // 80
    return x, y


def change_turn(player):
    if player == WHITE:
        player = GREY
    else:
        player = WHITE
    return player


def main():
    player = WHITE
    clicked = None
    board = Board()
    board.create_board()
    board.draw(win)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                x, y = get_pion_position(position)
                if clicked != None:
                    if board.possible_capture(clicked, x, y):
                        board.remove(clicked, x, y)
                        board.move_pion(clicked, x, y)
                        player = change_turn(player)
                    elif board.possible_moves_wo(clicked, x, y):
                        board.possible_moves_wo(clicked, x, y)
                        board.move_pion(clicked, x, y)
                        player = change_turn(player)
                    board.draw(win)
                    clicked = None
                elif board.board[x][y] != 0 and board.board[x][y].color == player:
                    clicked = board.board[x][y]
        board.victory()


main()
