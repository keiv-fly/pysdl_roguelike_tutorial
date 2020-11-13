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