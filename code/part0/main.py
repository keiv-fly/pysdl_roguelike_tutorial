import sdl2.ext
from sdl2 import SDL_Color


sdl2.ext.init()

screen_width = 640
screen_height = 480

window = sdl2.ext.Window(
    "PySDL2 Roguelike Tutorial", size=(screen_width, screen_height)
)
window.show()

# create renderer
renderer = sdl2.ext.Renderer(window)

fg = SDL_Color(255, 255, 255)
bg = SDL_Color(0, 0, 0)

font_manager = sdl2.ext.FontManager(
    font_path="C:\\Windows\\Fonts\\arial.ttf", size=16, color=fg, bg_color=bg
)
factory = sdl2.ext.SpriteFactory(renderer=renderer)  # Creating Sprite Factory
# Creating TextureSprite from Text
text = factory.from_text("@", fontmanager=font_manager)

x_offset = screen_width // 2 - text.size[0] // 2
y_offset = screen_height // 2 - text.size[1] // 2
renderer.copy(text, dstrect=(x_offset, y_offset, text.size[0], text.size[1]))

renderer.present()

processor = sdl2.ext.TestEventProcessor()
processor.run(window)
