from src.model.card import Card


class Player:
    def __init__(self, cards: list, player_id=None) -> None:
        if len(cards) != 7:
            raise ValueError(
                'Invalid player: must be initialised with 7 UnoCards'
            )
        if not all(isinstance(card, Card) for card in cards):
            raise ValueError(
                'Invalid player: cards must all be UnoCard objects'
            )
        self.initial_hand = cards.copy()
        self.hand = cards
        self.player_id = player_id

    def __repr__(self) -> str:
        if self.player_id is not None:
            return '<Player: {}>'.format(self.player_id)
        else:
            return '<Player object>'

    def __str__(self) -> str:
        if self.player_id is not None:
            return str(self.player_id)
        else:
            return repr(self)

    def can_play(self, current_card: Card) -> bool:
        return any(current_card.playable(card) for card in self.hand)
