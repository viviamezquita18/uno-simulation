from random import choice
from typing import Any

from src.model.game import Game
from src.model.game_data import GameData
from src.util.constants import COLORS


class GameOpponent:
    def __init__(self, game_data: GameData, players: list) -> None:
        self.game = Game(players)
        self.game_data = game_data
        self.player = choice(self.game.players)
        self.player_index = self.game.players.index(self.player)
        print('The game begins. You are Player {}.'.format(self.player_index))

    def __next__(self) -> None:
        game = self.game
        player = game.current_player
        player_id = player.player_id
        current_card = game.current_card
        self.__play_card(game, player, player_id)

    def __play_card(self, game: Game, player, player_id: str) -> None:
        if player == self.player:
            self.__validate_played(game, player, player_id)
        elif player.can_play(game.current_card):
            self.__validate_playable(game, player, player_id)
        else:
            self.game_data.log = "El jugador {} tomó una carta del mazo".format(player)
            game.play(player=player_id, card=None)

    def __validate_played(self, game: Game, player: Any, player_id: str, played=False) -> None:
        while not played:
            card_index = None
            while card_index is None:
                card_index = self.game_data.selected_card

            new_color = None
            if card_index is not False:
                card = player.hand[card_index]
                if not game.current_card.playable(card):
                    self.game_data.log = 'No puedes jugar esa carta!'
                    continue
                else:
                    self.game_data.log = 'Jugaste la carta: {:full}'.format(card)
                    if card.color == 'black' and len(player.hand) > 1:
                        self.game_data.color_selection_required = True
                        while new_color is None:
                            new_color = self.game_data.selected_color
                        self.game_data.log = 'Seleccionaste el color: {}'.format(new_color)
            else:
                card_index = None
                self.game_data.log = 'Tomaste una carta del mazo'

            game.play(player_id, card_index, new_color)
            played = True

    def __validate_playable(self, game: Game, player, player_id: str) -> None:
        for i, card in enumerate(player.hand):
            if game.current_card.playable(card):
                if card.color == 'black':
                    new_color = choice(COLORS)
                else:
                    new_color = None
                self.game_data.log = "El jugador {} jugó la carta: {:full}".format(player, card)
                game.play(player=player_id, card=i, new_color=new_color)
                break

    def print_hand(self):
        print('Your hand: {}'.format(
            ' '.join(str(card) for card in self.player.hand)
        ))
