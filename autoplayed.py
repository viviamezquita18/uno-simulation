import random
import threading

from src.model.game import Game
from src.util.constants import COLORS, GAMES_COUNT


def self_game(game_count):
    players = random.randint(2, 15)
    game = Game(players)

    print("Game [{}]: starting a {} player game".format(game_count, players))

    cards_count = 0
    while game.is_active:
        cards_count += 1
        player = game.current_player
        player_id = player.player_id
        if player.can_play(game.current_card):
            for i, card in enumerate(player.hand):
                if game.current_card.playable(card):
                    if card.color == 'black':
                        new_color = random.choice(COLORS)
                    else:
                        new_color = None
                    game.play(player=player_id, card=i, new_color=new_color)
                    break
        else:
            game.play(player=player_id, card=None)

    print("Game [{}]: {} cards played".format(game_count, cards_count))


for games in range(GAMES_COUNT):
    t = threading.Thread(target=self_game, args=(games,))
    t.start()
