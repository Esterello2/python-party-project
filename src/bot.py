from mocks import ReversiBotMock
from reversi import Reversi
import random
import math
import click
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import sys

game: ReversiBotMock
player: int


class RandomBot():
    
    def __init__(self, game: ReversiBotMock, player: int):
        
        self.game = game
        self.player = player
        self.moves = []

    def random_move(self) -> Tuple[int, int]:
        
        random_move = random.choice(self.game.available_moves)
        self.game.apply_move(random_move)
        self.moves.append(random_move)

        return random_move

class SmartBot():
    def __init__(self, game: ReversiBotMock, player: int):
        self.game = game
        self.player = player
        self.moves = []

    def get_num_pieces(self) -> int:
        num_pieces = 0
        for r in range(self.game.side):
            for c in range(self.game.side):
                if self.game.othello[r][c] == self.player:
                    num_pieces += 1
        return num_pieces

    def choose_move(self) -> Tuple[int, int]:
        best_move = None
        best_num_pieces = -1

        for move in self.game.available_moves:
            sim_game = self.game.simulate_moves([move])
            num_pieces = sim_game.bot1.get_num_pieces() if self.player == 1 else sim_game.bot2.get_num_pieces()
            if num_pieces > best_num_pieces:
                best_num_pieces = num_pieces
                best_move = move

        self.game.apply_move(best_move)
        self.moves.append(best_move)

        return best_move

def SnmarterBot(basegame: Reversi, turn: int) -> None:
    '''
    outcomes = basegame.available_moves
    high = -math.inf
    optimal = []
    for move in outcomes:
        total = 0
        first = basegame.simulate_moves([move])
        if first.done:
            optimal = [move]
            break
        second = first.available_moves
        if second:
            for move_two in second:
                final = first.simulate_moves([move_two                            total += 1
            if total / len(second) > high:
                high = total / len(second)
                optimal = []
                optimal.append(move)
            elif total / len(second) == high:
                optimal.append(move)
    if optimal:
        pick = random.randint(0,len(optimal) - 1)
        basegame.apply_move(optimal[pick])

@click.command("bot")


def play_games(num_games):

    bot1_wins = 0
    bot2_wins = 0


    for i in range(num_games):
        match = ReversiBotMock(8, 2, False)
        bot1 = RandomBot(match, 1)
        bot2 = SmarterBot(match, 2)
        while not match.outcome():

            bot1.random_move()

            if match.outcome() != 0:
                break
            
            bot2.choose_move()


        
        outcome = match.outcome

        if outcome == [1]:
            bot1_wins += 1
        elif outcome  == [2]:
            bot2_wins += 1

    bot1_percent = (bot1_wins / num_games) * 100
    bot2_percent = (bot2_wins / num_games) * 100
    ties_percent = 100 - bot1_percent - bot2_percent

    print("Player 1 wins: {:.2f}%".format(bot1_percent))
    print("Player 2 wins: {:.2f}%".format(bot2_percent))
    print("Ties: {:.2f}%".format(ties_percent))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 src/bot.py NUM_GAMES")
        sys.exit(1)
    num_games = int(sys.argv[1])
    play_games(num_games)
