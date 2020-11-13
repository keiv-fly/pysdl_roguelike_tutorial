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