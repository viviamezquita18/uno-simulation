import os
from itertools import chain, product, repeat
from pathlib import Path
from random import shuffle, choice
from typing import Any

from src.model.card import Card
from src.model.player import Player
from src.util.constants import COLORS, BLACK_CARD_TYPES, COLOR_CARD_TYPES

file_name = Path(__file__).parent / '../analysis/statistics.csv'


def create_deck(random: bool) -> list:
    color_cards = product(COLORS, COLOR_CARD_TYPES)
    black_cards = product(repeat('black', 4), BLACK_CARD_TYPES)
    all_cards = chain(color_cards, black_cards)
    deck = [Card(color, card_type) for color, card_type in all_cards]
    if random:
        shuffle(deck)
        return deck
    else:
        return list(reversed(deck))


def check_dir():
    directory = os.path.dirname(file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)


def store_winner_hand(line: list) -> None:
    check_dir()
    f = open(file_name, 'a')
    f.write(' '.join(str(x) for x in line) + '\n')
    f.close()


class Game:
    def __init__(self, players: int, random=True) -> None:
        if not isinstance(players, int):
            raise ValueError('Invalid game: players must be integer')
        if not 2 <= players <= 15:
            raise ValueError('Invalid game: must be between 2 and 15 players')
        self.deck = create_deck(random=random)
        self.players = [
            Player(self.__deal_hand(), n) for n in range(players)
        ]
        self.__player_cycle = ReversibleCycle(self.players)
        self.__current_player = next(self.__player_cycle)
        self.__winner = None
        self.__check_first_card()

    def __next__(self) -> None:
        self.__current_player = next(self.__player_cycle)

    def __deal_hand(self) -> list:
        return [self.deck.pop() for i in range(7)]

    @property
    def current_card(self):
        return self.deck[-1]

    @property
    def is_active(self) -> bool:
        return all(len(player.hand) > 0 for player in self.players)

    @property
    def current_player(self) -> Any:
        return self.__current_player

    @property
    def winner(self) -> Player:
        return self.__winner

    def play(self, player: Any, card=None, new_color=None) -> None:
        __player = self.players[player]
        if not isinstance(player, int):
            raise ValueError('Invalid player: should be the index number')
        if not 0 <= player < len(self.players):
            raise ValueError('Invalid player: index out of range')
        if self.current_player != __player:
            raise ValueError('Invalid player: not their turn')
        if card is None:
            self.__pick_up(__player, 1)
            next(self)
            return
        self.__played_card(__player, card, new_color)

        if not self.is_active:
            raise ValueError('Game is over')

        played_card = __player.hand.pop(card)
        self.deck.append(played_card)
        self.__played_event(played_card, new_color)

        if self.is_active:
            next(self)
        else:
            self.__winner = __player
            self.__print_winner()

    def __played_card(self, player, card, new_color) -> None:
        __card = player.hand[card]
        if not self.current_card.playable(__card):
            raise ValueError(
                'Invalid card: {} not playable on {}'.format(
                    __card, self.current_card
                )
            )
        if __card.color == 'black':
            if new_color not in COLORS:
                raise ValueError(
                    'Invalid new_color: must be red, yellow, green or blue'
                )

    def __played_event(self, played_card, new_color):
        card_color = played_card.color
        card_type = played_card.card_type

        if card_color == 'black':
            self.current_card.temp_color = new_color
            if card_type == '+4':
                next(self)
                self.__pick_up(self.current_player, 4)
        elif card_type == 'reverse':
            self.__player_cycle.reverse()
        elif card_type == 'skip':
            next(self)
        elif card_type == '+2':
            next(self)
            self.__pick_up(self.current_player, 2)

    def __print_winner(self):
        print(self.__winner)
        if self.winner.player_id:
            winner_name = self.winner.player_id
        else:
            winner_name = self.players.index(self.winner)

        store_winner_hand(self.players[winner_name].initial_hand)
        print("Player {} wins!".format(winner_name))

    def __pick_up(self, player, n):
        penalty_cards = [self.deck.pop(0) for i in range(n)]
        player.hand.extend(penalty_cards)

    def __check_first_card(self):
        if self.current_card.color == 'black':
            color = choice(COLORS)
            self.current_card.temp_color = color
            print("Selected random color for black card: {}".format(color))


class ReversibleCycle:
    def __init__(self, iterable):
        self.__items = list(iterable)
        self.__position = None
        self.__reverse = False

    def __next__(self):
        if self.pos is None:
            self.pos = -1 if self.__reverse else 0
        else:
            self.pos = self.pos + self.__delta
        return self.__items[self.pos]

    @property
    def __delta(self):
        return -1 if self.__reverse else 1

    @property
    def pos(self):
        return self.__position

    @pos.setter
    def pos(self, value):
        self.__position = value % len(self.__items)

    def reverse(self):
        self.__reverse = not self.__reverse
