
"""A collection of constants and default definitions."""

FPS = 120
WINWIDTH = 1100
WINHEIGHT = 650
MENUWIDTH = 0.189*WINWIDTH
OPERATIONAL_WIDTH = WINWIDTH - MENUWIDTH
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
ORANGE    = (255,  70,   0)
BLUE      = (  0,   0, 255)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
GREY      = (200, 200, 200)
DARKGRAY  = ( 40,  40,  40)
PURPLE    = (150,   0, 150)
BGCOLOUR = BLACK

PLANET = "Planet"
STAR = "Star"

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

INACTIVE = 'inactive'
ACTIVE = 'active'

STAR_RADIUS = 6
PLANET_RADIUS = 2
