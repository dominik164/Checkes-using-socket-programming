import socket
import threading
import pygame
import pygame.freetype
from board import Board
from colors import *

WIDTH = 640
HEIGHT = 700

pygame.init()
font_1 = pygame.freetype.SysFont('Sans', 34)
font_2 = pygame.freetype.SysFont('Sans', 20)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Warcaby')


board = Board()
board.create_board()
board.draw(win)
player = None
current_player = WHITE


def get_pion_position(pos):
    x, y = pos
    x = x // 80
    y = (y-60) // 80
    return x, y


def change_turn(current_player):
    if current_player == WHITE:
        current_player = GREY
    else:
        current_player = WHITE
    return current_player


def send_move(flag, clicked, x, y):
    string = "".join([str(flag), str(clicked.x),
                      str(clicked.y), str(x), str(y)])
    client.send(string.encode('ascii'))


def print_player(player):
    if current_player == WHITE:
        text_str = 'RUCH BIALYCH'
    else:
        text_str = 'RUCH SZARYCH'
    font_1.render_to(win, (200, 10), text_str, (3, 169, 242))
    pygame.display.flip()


def main():
    global player, current_player
    clicked = None
    print_player(current_player)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and player == current_player:
                position = pygame.mouse.get_pos()
                x, y = get_pion_position(position)
                if clicked != None:
                    if board.possible_capture(clicked, x, y):
                        send_move(0, clicked, x, y)
                    elif board.possible_moves_wo(clicked, x, y):
                        send_move(1, clicked, x, y)
                    clicked = None
                elif board.board[x][y] != 0 and board.board[x][y].color == current_player:
                    clicked = board.board[x][y]


def receive():
    global player, current_player
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'WHITE':
                client.send(nickname.encode('ascii'))
                player = WHITE
                txt = 'Playing as White'
                font_2.render_to(win, (0, 10), txt, (3, 169, 242))
                pygame.display.flip()
            elif message == 'GREY':
                client.send(nickname.encode('ascii'))
                player = GREY
                txt = 'Playing as Grey'
                font_2.render_to(win, (0, 10), txt, (3, 169, 242))
                pygame.display.flip()
            elif len(message) == 5:
                if message[0] == '1':
                    board.move_pion(
                        board.board[int(message[1])][int(message[2])], int(message[3]), int(message[4]))
                    board.board[int(message[3])][int(message[4])].make_queen()
                else:
                    board.remove(
                        board.board[int(message[1])][int(message[2])], int(message[3]), int(message[4]))
                    board.move_pion(
                        board.board[int(message[1])][int(message[2])], int(message[3]), int(message[4]))
                board.draw(win)
                current_player = change_turn(current_player)
                print_player(current_player)
                board.victory(win)
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.56.1', 55555))

# Listening to Server and Sending Nickname


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()


main()
