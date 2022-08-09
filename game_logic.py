#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Connect Four game - CLI
Author: Monica Tuttle (with mentorship from Nick Groesch, Lead Instructor
	at TechWise at TalentSprint)
	Code originated on 7/17/22, last update on 8/6/22
"""


class Grid:
    def __init__(self):
        self.chutes = [[], [], [], [], [], [], []]

    def play_token(self, chute, token):
        self.chutes[chute].append(token)

    def draw_grid(self):
        print(self.chutes)

    def check_for_vertical_win(self, chute, token):
        count_in_a_row = 0
        for i in self.chutes[chute]:
            if i == token:
                count_in_a_row += 1
                if count_in_a_row == 4:
                    return True
            else:
                count_in_a_row = 0
        return False

    def check_for_horizontal_win(self):
        for row in range(5):
            # print("row: ", row)
            for n in range(4):
                # print("n: ", n)
                try:
                    if (self.chutes[n][row] == self.chutes[n + 1][row] and self.chutes[n + 1][row] ==
                            self.chutes[n + 2][row] and \
                            self.chutes[n + 2][row] == self.chutes[n + 3][row]):
                        return True
                except IndexError:
                    pass
                continue
        return False

    def check_for_diagonal_win(self, token_color):
        token_color = "red"
        for row in range(4):
            for n in range(3):
                try:
                    if chutes[row][n] == token_color and chutes[row][n + 1] == token_color and chutes[row][
                        n + 2] == token_color and chutes[row][n + 3] == token_color:
                        return True
                except IndexError:
                    next
        return False

    def check_if_chutes_full(self):
        LIMIT = 6
        chutes_list = []
        for chute in self.chutes:
            if len(chute) == LIMIT:
                chutes_list.append(self.chutes.index(chute))
        for i in chutes_list:
            print("Chute " + str(i) + " is full.")
        return input(
            "Pick another chute: ")  # what is returned needs to change so that the AI can use the information to make a choice


class Player:
    def __init__(self, token_color):
        self.token_color = token_color

    def __str__(self):
        return str(self.token_color)

    def __repr__(self):
        return f'{self.token_color}'

    def take_turn(self):
        return input("Select a chute: ")


class Connect4:
    # could add colors to this list maybe eliciting user input and
    # using append() function
    colors = ["red", "yellow", "blue", "green", "purple", "black"]
    
    def __init__(self, number_of_players = 2):
        self.grid = Grid()
        self.players = [Player(token_color) for token_color in Connect4.colors[0:number_of_players]] 
                        # below here we have created ["red", "yellow"]
    def game_loop(self):
            for player in self.players: # ["red", "yellow"]
                player_selection = int(player.take_turn())
                self.grid.play_token(player_selection, player.token_color)
                self.grid.draw_grid()
                if self.grid.check_for_vertical_win(player_selection, player.token_color) or \
                self.grid.check_for_horizontal_win():
                #self.grid.check_for_diagonal_win(self.player_one.token_color):
                    print(f'{player} wins')
                    stop = 0
                    return stop == 0
            else:
                self.game_loop()

my_game = Connect4()
my_game.game_loop()
