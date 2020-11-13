from typing import Tuple

import sdl2.ext


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: Tuple[int, int, int],
        renderer,
        font_size=20,
        tile_size=20,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = sdl2.ext.Color(*color)
        self.font_size = font_size
        self.bg_color = sdl2.ext.Color(0, 0, 0, 255)
        self.tile_size = tile_size
        self.renderer = renderer

        font_manager = sdl2.ext.FontManager(
            font_path="C:\\Windows\\Fonts\\arial.ttf",
            size=font_size,
            color=self.color,
            bg_color=self.bg_color,
        )
        factory = sdl2.ext.SpriteFactory(renderer=self.renderer)
        self.text = factory.from_text(self.char, fontmanager=font_manager)

        self.x_offset = -self.text.size[0] // 2
        self.y_offset = -self.text.size[1] // 2
        self.text_width = self.text.size[0]
        self.text_height = self.text.size[1]

        self.pixel_x = self.x * self.tile_size + self.x_offset
        self.pixel_y = self.y * self.tile_size + self.y_offset

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

        self.pixel_x = self.x * self.tile_size + self.x_offset
        self.pixel_y = self.y * self.tile_size + self.y_offset