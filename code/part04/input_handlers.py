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
