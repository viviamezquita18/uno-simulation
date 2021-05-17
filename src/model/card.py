from pgzero.actor import Actor

from src.util.constants import ALL_COLORS, BLACK_CARD_TYPES, COLOR_CARD_TYPES, COLORS


def validate(color: str, card_type: str) -> None:
    if color not in ALL_COLORS:
        raise ValueError('Invalid color')
    if color == 'black' and card_type not in BLACK_CARD_TYPES:
        raise ValueError('Invalid card type')
    if color != 'black' and card_type not in COLOR_CARD_TYPES:
        raise ValueError('Invalid card type')


class Card:
    def __init__(self, color: str, card_type: str) -> None:
        validate(color, card_type)
        self.color = color
        self.card_type = card_type
        self.temp_color = None
        self.sprite = Actor('{}_{}'.format(color, card_type))

    def __repr__(self) -> str:
        return '<Card object: {} {}>'.format(self.color, self.card_type)

    def __str__(self) -> str:
        return '{}{}'.format(self.color_short, self.card_type_short)

    def __format__(self, format_type: str) -> str:
        if format_type == 'full':
            return '{} {}'.format(self.color, self.card_type)
        else:
            return str(self)

    def __eq__(self, other) -> bool:
        return self.color == other.color and self.card_type == other.card_type

    @property
    def color_short(self) -> str:
        return self.color[0].upper()

    @property
    def card_type_short(self) -> str:
        if self.card_type in ('skip', 'reverse', 'wildcard'):
            return self.card_type[0].upper()
        else:
            return self.card_type

    @property
    def __color(self) -> str:
        return self.temp_color if self.temp_color else self.color

    @property
    def temp_color(self) -> str:
        return self.__temp_color

    @temp_color.setter
    def temp_color(self, color: str) -> None:
        if color is not None:
            if color not in COLORS:
                raise ValueError('Invalid color')
        self.__temp_color = color

    def playable(self, other) -> bool:
        return (
                self.__color == other.color or
                self.card_type == other.card_type or
                other.color == 'black'
        )
