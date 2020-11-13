Part 2 - Moving '@' around the screen
=====================================

Explanation
-----------

In this part we will be able to move the ``@`` around the screen. Like `Roguelike Tutorial in Python 3 and TCOD <http://rogueliketutorials.com/tutorials/tcod/v2/>`_ we will also add an Action class.

Add this to the ``actions.py`` file:

.. code::

    class Action:
        pass


    class EscapeAction(Action):
        pass


    class MovementAction(Action):
        def __init__(self, dx: int, dy: int):
            super().__init__()

            self.dx = dx
            self.dy = dy

Here we have different classes depending on the action that we need to perform. All classes are inherited from Action.

Now let's change the ``main.py`` file to allow moving of the ``@`` character:

.. code:: diff

    +import sdl2
    import sdl2.ext
    from sdl2 import SDL_Color

    +from actions import Action, EscapeAction, MovementAction

We need the sdl2 library to later import the key codes to identify specific keys. We also added the actions from the ``actions.py`` file.

.. code:: diff


    +def run():
        sdl2.ext.init()

        screen_width = 640
        screen_height = 480

        +BLACK = SDL_Color(0, 0, 0)

        +tile_size = 20
        +player_font_size = 20

        +player_x = screen_width // 2
        +player_y = screen_height // 2

        window = sdl2.ext.Window(
            "PySDL2 Roguelike Tutorial", size=(screen_width, screen_height)
        )

Here we wrapped the code into a run() function to make the code more structured. We also added a definition of the black color. We need the tile_size to calculate the jumps for the ``@`` character. In addition we also fixed the starting position of the ``@`` that will later change depending on the keyboard input.

In the following code we change the size of the font to be equal to a variable

.. code:: diff

    font_manager = sdl2.ext.FontManager(
        font_path="C:\\Windows\\Fonts\\arial.ttf",
        -size=16,
        +size=player_font_size,
        color=fg,
        bg_color=bg,
    )
    factory = sdl2.ext.SpriteFactory(renderer=renderer)

Now we insert the player coordinates into the calculation of the ``@`` sprite rectangle.

.. code:: diff

    -x_offset = screen_width // 2 - text.size[0] // 2
    -y_offset = screen_height // 2 - text.size[1] // 2
    +x_offset = player_x - text.size[0] // 2
    +y_offset = player_y - text.size[1] // 2

We also add a loop to process events. In our case it is the keyboard events that move the ``@``. The renderer.clear is needed to clear everything that was drawn in the previous iteration.

.. code:: diff

    +while True:
    +    renderer.clear(BLACK)
         renderer.copy(text, dstrect=(x_offset, y_offset, text.size[0], text.size[1]))

         renderer.present()

Now we add the keyboard event processing loop:

.. code:: diff

        +events = sdl2.ext.get_events()
        +for event in events:
        +    action = None
        +    if event.type == sdl2.SDL_QUIT:
        +       action = EscapeAction()
        +    elif event.type == sdl2.SDL_KEYDOWN:
        +        if event.key.keysym.sym == sdl2.SDLK_UP:
        +            action = MovementAction(dx=0, dy=-1)
        +        elif event.key.keysym.sym == sdl2.SDLK_DOWN:
        +            action = MovementAction(dx=0, dy=1)
        +        elif event.key.keysym.sym == sdl2.SDLK_LEFT:
        +            action = MovementAction(dx=-1, dy=0)
        +        elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
        +            action = MovementAction(dx=1, dy=0)
        +        elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
        +            action = EscapeAction()

        +    if action is None:
        +        continue

        +    if isinstance(action, MovementAction):
        +        player_x += action.dx * tile_size
        +        player_y += action.dy * tile_size
        +        x_offset = player_x - text.size[0] // 2
        +        y_offset = player_y - text.size[1] // 2

        +    elif isinstance(action, EscapeAction):
        +        sdl2.ext.quit()
        +        raise SystemExit()

Let's have a closer look at the lines.

.. code::

        events = sdl2.ext.get_events()

Reads all the events that were accumulated by SDL2 from the previous call of this line. ::

        for event in events:
            action = None

Loops over all accumulated events and sets an empty action at the beginning of the loop ::

            if event.type == sdl2.SDL_QUIT:
                action = EscapeAction()

If a quit signal was sent to the program (for example the close window button was clicked), then it is an EscapeAction ::

            elif event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    action = MovementAction(dx=0, dy=-1)
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    action = MovementAction(dx=0, dy=1)
                elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                    action = MovementAction(dx=-1, dy=0)
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    action = MovementAction(dx=1, dy=0)

Here if the event was ``keydown`` event then we check what key was pressed. If the key is an arrow then it is a ``MovementAction`` ::

                elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    action = EscapeAction()

If the key was ``Esc`` then it is an EscapeAction.

Now we process the actions depending on what action we have::

           if action is None:
                continue

If action is empty then check the next event ::

            if isinstance(action, MovementAction):
                player_x += action.dx * tile_size
                player_y += action.dy * tile_size
                x_offset = player_x - text.size[0] // 2
                y_offset = player_y - text.size[1] // 2

Here if the action was a movement then we need to change the coordinates of the ``@`` ::

            elif isinstance(action, EscapeAction):
                sdl2.ext.quit()
                raise SystemExit()

If the action was EscapeAction, then shut down SDL2 and finish the program.

Taking into account that we moved everything into ``run()``, we need to execute ``run()`` when the file is executed with ``python main.py``::

    if __name__ == "__main__":
        run()

After running this code with ``python main.py`` we see the same picture as in Part 1 but we can move the ``@`` with the keyboard keys

Full code of all files
------------------------------

actions.py
^^^^^^^^^^

.. code::

    class Action:
        pass


    class EscapeAction(Action):
        pass


    class MovementAction(Action):
        def __init__(self, dx: int, dy: int):
            super().__init__()

            self.dx = dx
            self.dy = dy

main.py
^^^^^^^

.. code::

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