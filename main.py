from threading import Thread
from time import sleep

from pgzero.actor import Actor

from src.model.game_data import GameData
from src.model.opponent import GameOpponent
from src.util.constants import COLORS, NUM_PLAYERS, WIDTH, HEIGHT

game_data = GameData()
game = GameOpponent(game_data, NUM_PLAYERS)

deck = Actor('back')
color_images = {color: Actor(color) for color in COLORS}


def game_loop():
    while game.game.is_active:
        sleep(1)
        next(game)


game_loop_thread = Thread(target=game_loop)
game_loop_thread.start()


def draw_deck() -> None:
    deck.pos = (250, 70)
    deck.draw()
    current_card = game.game.current_card
    current_card.sprite.pos = (330, 70)
    current_card.sprite.draw()
    if game_data.color_selection_required:
        for i, card in enumerate(color_images.values()):
            card.pos = (410 + i * 80, 70)
            card.draw()
    elif current_card.color == 'black' and current_card.temp_color is not None:
        color_img = color_images[current_card.temp_color]
        color_img.pos = (410, 70)
        color_img.draw()


def draw_players_hands() -> None:
    for p, player in enumerate(game.game.players):
        color = '#1a73e8' if player == game.game.current_player else '#454545'
        text = 'Jugador {} {}'.format(p + 1, ' - Ganador!' if game.game.winner == player else '')
        screen.draw.text(text, (25, 180 + p * 130), fontname="montserrat-light", fontsize=32, color=color)

        for c, card in enumerate(player.hand):
            if player == game.player:
                sprite = card.sprite
            else:
                sprite = Actor('back')
            sprite.pos = (250 + c * 80, 210 + p * 130)
            sprite.draw()


def show_log() -> None:
    screen.draw.text(game_data.log, fontname="montserrat-light", midbottom=(WIDTH / 2, HEIGHT - 50), color='black')


def update() -> None:
    screen.clear()
    screen.fill((255, 255, 255))
    draw_deck()
    draw_players_hands()
    show_log()


def on_mouse_down(pos) -> None:
    if game.player == game.game.current_player:
        for card in game.player.hand:
            if card.sprite.collidepoint(pos):
                game_data.selected_card = game.player.hand.index(card)
                print('Selected card {} index {}'.format(card, game.player.hand.index(card)))

        if deck.collidepoint(pos):
            game_data.selected_card = False
            print('Selected pick up')

        for color, card in color_images.items():
            if card.collidepoint(pos):
                game_data.selected_color = color
                game_data.color_selection_required = False
