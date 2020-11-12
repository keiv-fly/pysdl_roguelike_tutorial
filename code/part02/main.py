import sdl2
import sdl2.ext
from sdl2 import SDL_Color

from actions import Action, EscapeAction, MovementAction


def run():
    sdl2.ext.init()

    screen_width = 640
    screen_height = 480

    BLACK = SDL_Color(0, 0, 0)

    tile_size = 20
    player_font_size = 20

    player_x = screen_width // 2
    player_y = screen_height // 2

    window = sdl2.ext.Window(
        "PySDL2 Roguelike Tutorial", size=(screen_width, screen_height)
    )
    window.show()

    renderer = sdl2.ext.Renderer(window)

    fg = SDL_Color(255, 255, 255)
    bg = SDL_Color(0, 0, 0)

    font_manager = sdl2.ext.FontManager(
        font_path="C:\\Windows\\Fonts\\arial.ttf",
        size=player_font_size,
        color=fg,
        bg_color=bg,
    )
    factory = sdl2.ext.SpriteFactory(renderer=renderer)
    text = factory.from_text("@", fontmanager=font_manager)

    x_offset = player_x - text.size[0] // 2
    y_offset = player_y - text.size[1] // 2

    while True:
        renderer.clear(BLACK)
        renderer.copy(text, dstrect=(x_offset, y_offset, text.size[0], text.size[1]))

        renderer.present()

        events = sdl2.ext.get_events()
        for event in events:
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

            if action is None:
                continue

            if isinstance(action, MovementAction):
                player_x += action.dx * tile_size
                player_y += action.dy * tile_size
                x_offset = player_x - text.size[0] // 2
                y_offset = player_y - text.size[1] // 2

            elif isinstance(action, EscapeAction):
                sdl2.ext.quit()
                raise SystemExit()


if __name__ == "__main__":
    run()