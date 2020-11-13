Part 3 - The generic Entity, the Engine and the render function
==================================================================

action.py
^^^^^^^^^

The ``action.py`` file remains the same::

    class Action:
        pass


    class EscapeAction(Action):
        pass


    class MovementAction(Action):
        def __init__(self, dx: int, dy: int):
            super().__init__()

            self.dx = dx
            self.dy = dy

input_handlers.py
^^^^^^^^^^^^^^^^^^

Event handling is moved to ``input_handlers.py``::

    import sdl2

    from actions import Action, EscapeAction, MovementAction


    def event_handler(event) -> None:
        action = None
        if event.type == sdl2.SDL_QUIT:
            action = EscapeAction()
        elif event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_UP:
                action = MovementAction(dx=0, dy=-1)
            elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                action = MovementAction(dx=0, dy=1)
            elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                action = MovementAction(dx=-1, dy=0)
            elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                action = MovementAction(dx=1, dy=0)
            elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                action = EscapeAction()

        return action

entity.py
^^^^^^^^^^

A new file is created for players, npcs, enemies, items - ``entity.py``::

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
            self.x += dx
            self.y += dy

            self.pixel_x = self.x * self.tile_size + self.x_offset
            self.pixel_y = self.y * self.tile_size + self.y_offset

In more detail:

Tile coordinates of the entity::

            self.x = x
            self.y = y

Character and color for the character::

            self.char = char
            self.color = sdl2.ext.Color(*color)

Creation of the text sprite::

            font_manager = sdl2.ext.FontManager(
                font_path="C:\\Windows\\Fonts\\arial.ttf",
                size=font_size,
                color=self.color,
                bg_color=self.bg_color,
            )
            factory = sdl2.ext.SpriteFactory(renderer=self.renderer)
            self.text = factory.from_text(self.char, fontmanager=font_manager)

Calculation of the pixel values: position, sprite offset, pixel text width and height::

            self.x_offset = -self.text.size[0] // 2
            self.y_offset = -self.text.size[1] // 2
            self.text_width = self.text.size[0]
            self.text_height = self.text.size[1]

            self.pixel_x = self.x * self.tile_size + self.x_offset
            self.pixel_y = self.y * self.tile_size + self.y_offset

In the move function::

        def move(self, dx: int, dy: int) -> None:

first the tile coordinates are updated::

            self.x += dx
            self.y += dy

then the pixel coordinates are updated::

            self.pixel_x = self.x * self.tile_size + self.x_offset
            self.pixel_y = self.y * self.tile_size + self.y_offset

engine.py
^^^^^^^^^^

The logic for handling events and rendering is moved to ``engine.py``::

    from typing import Set, Iterable, Any, List

    import sdl2.ext

    from actions import EscapeAction, MovementAction
    from entity import Entity
    from input_handlers import event_handler


    BLACK = sdl2.ext.Color(0, 0, 0)


    class Engine:
        def __init__(self, entities: List[Entity], player: Entity):
            self.entities = entities
            self.event_handler = event_handler
            self.player = player

        def handle_events(self, events: Iterable[Any]) -> None:
            for event in events:
                action = event_handler(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    self.player.move(dx=action.dx, dy=action.dy)

                elif isinstance(action, EscapeAction):
                    sdl2.ext.quit()
                    raise SystemExit()

        def render(self, renderer, screen_width: int, screen_height: int) -> None:
            for entity in self.entities:
                renderer.copy(
                    entity.text,
                    dstrect=(
                        entity.pixel_x + screen_width // 2,
                        entity.pixel_y + screen_height // 2,
                        entity.text_width,
                        entity.text_height,
                    ),
                )

            renderer.present()

            renderer.clear(BLACK)

main.py
^^^^^^^^

And the ``main.py`` file now is very small::

    import sdl2
    import sdl2.ext


    from entity import Entity
    from engine import Engine


    def run() -> None:
        sdl2.ext.init()

        screen_width = 640
        screen_height = 480

        window = sdl2.ext.Window(
            "PySDL2 Roguelike Tutorial", size=(screen_width, screen_height)
        )
        window.show()

        renderer = sdl2.ext.Renderer(window)

        player = Entity(0, 0, "@", (255, 255, 255), renderer)
        npc = Entity(0 - 5, 0, "@", (255, 255, 0), renderer)
        entities = [npc, player]

        engine = Engine(entities=entities, player=player)

        while True:
            engine.render(renderer, screen_width, screen_height)

            events = sdl2.ext.get_events()

            engine.handle_events(events)


    if __name__ == "__main__":
        run()