import colorsys
from random import randint


class Color:
    def __init__(self):
        self._color = self.generate_random_color()

    def __str__(self):
        return self._color

    def __repr__(self):
        return f"Color({self._color})"

    def generate_random_color(self):
        return "#{:02x}{:02x}{:02x}".format(
            randint(0, 255),
            randint(0, 255),
            randint(0, 255)
        )

    def get_much_lighter(self, hex_color: str = None, v: float = 0.5, set_as_new_color: bool = False):

        if not hex_color:
            hex_color = self._color

        # Перетворення HEX-коду в RGB
        r = int(hex_color[1:3], 16) / 255.0
        g = int(hex_color[3:5], 16) / 255.0
        b = int(hex_color[5:7], 16) / 255.0

        # Перетворення RGB в HSV (відтінок, насиченість, значення)
        h, s, v_ = colorsys.rgb_to_hsv(r, g, b)

        # Перетворення HSV назад в RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)

        # Перетворення RGB назад в HEX
        new_hex_color = "#{:02X}{:02X}{:02X}".format(int(r * 255), int(g * 255), int(b * 255))

        if set_as_new_color:
            self.set_color(new_hex_color)

        return new_hex_color

    def set_color(self, new_hex_color: str):
        self._color = new_hex_color if new_hex_color.startswith("#") else "#" + new_hex_color
