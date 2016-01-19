import math, pygame
from constants import *

class Menu:
    """Class for building a customised in-game menu, with
    real-time functionality.

    """
    pygame.font.init()

    def __init__(self, MENUWIDTH, MENUHEIGHT):
        """Initialise the menu background and list of items.

        constructor: Menu(float, float)
        """
        
        self._menu_items = []
        self.menu_Text = []
        #Background
        self.menuRect = pygame.Rect((0, 0), (MENUWIDTH, MENUHEIGHT))

    def create_button(self, button_info_tuple):
        """Method with which to generate buttons; to be called from
        outside the class. Each button is composed of a dictionary, which
        stores information about the button aesthetics and functionality.

        create_button((float, float, float, float, colour-tuple, string
        , (int, string), var., string, boolean, var.)) -> None
        
        """
        
        font1 = pygame.font.Font(None, 26)
        font2 = pygame.font.Font(None, 36)

        xpos = button_info_tuple[0]
        ypos = button_info_tuple[1]
        width = button_info_tuple[2]
        height = button_info_tuple[3]
        colour = button_info_tuple[4]
        text = button_info_tuple[5]
        function = button_info_tuple[6]
        amount = button_info_tuple[7]
        highlight = button_info_tuple[8]
        persistence = button_info_tuple[9]
        menu_change = button_info_tuple[10]

        rendered_Text = font1.render(text, 1, BLACK)

        button_Dict = {'xpos'       : xpos,
                       'ypos'       : ypos,
                       'width'      : width,
                       'height'     : height,
                       'colour'     : colour,
                       'text'       : rendered_Text,
                       'rect'       : pygame.Rect((xpos, ypos), (width, height)),
                       'function'   : function[1],
                       'f_index'    : function[0],
                       'amount'     : amount,
                       'highlight'  : highlight,
                       'persistence': persistence,
                       'menuChange' : menu_change,
                       'menu_type'  : 'Button'}

        self._menu_items.append(button_Dict)

    def create_slider(self, slider_info_tuple):
        """Method used to generate sliders from outside the class.

        create_slider((float, float, float, float, colour-tuple, string
        , string, int, int)) -> None
        
        """

        xpos = slider_info_tuple[0]
        ypos = slider_info_tuple[1]
        width = slider_info_tuple[2]
        height = slider_info_tuple[3]
        colour = slider_info_tuple[4]
        text = slider_info_tuple[5]
        function = slider_info_tuple[6]
        minimum = slider_info_tuple[7]
        maximum = slider_info_tuple[8]

        font1 = pygame.font.Font(None, 26)
        font2 = pygame.font.Font(None, 16)
        rendered_Text_1 = font1.render(text[0], 1, BLACK)
        rendered_Text_2 = font2.render(text[1], 1, BLACK)
        rendered_Text_3 = font2.render(text[2], 1, BLACK)

        slider_Dict = {'xpos'       : xpos,
                       'ypos'       : ypos,
                       'width'      : width,
                       'height'     : height,
                       'colour'     : colour,
                       'text'       : (rendered_Text_1, rendered_Text_2, rendered_Text_3),
                       'rect'       : pygame.Rect((xpos-width/20, ypos-height/2), (width/12, height)),
                       'function'   : function,
                       'min'        : minimum,
                       'max'        : maximum,
                       'amount'     : minimum,
                       'grabbed'    : False,
                       'menu_type'  : 'Slider'}

        self._menu_items.append(slider_Dict)
        
        
    def draw(self, DISPLAYSURF):
        """Draw the menu and its items. In addition, draw highlights over the
        currently selected buttons or if the cursor hovers over a non-persistent
        button.

        """

        pygame.draw.rect(DISPLAYSURF, GREY, self.menuRect)

        for item in self._menu_items:
            if item['menu_type'] == 'Button':
                pygame.draw.rect(DISPLAYSURF, item['colour'], item['rect'])
                DISPLAYSURF.blit(item['text'], (item['rect'].left+7, item['rect'].top+4))
                # highlights
                if item['highlight'] == ACTIVE and item['persistence'] == True:
                    if item['colour'] != WHITE:
                        pygame.draw.rect(DISPLAYSURF, BLACK, item['rect'], 3)
                    else:
                        pygame.draw.rect(DISPLAYSURF, BLUE, item['rect'], 3)
            elif item['menu_type'] == 'Slider':
                pygame.draw.rect(DISPLAYSURF, item['colour'], item['rect'])
                DISPLAYSURF.blit(item['text'][0], (item['xpos']+10, item['ypos']-40))
                DISPLAYSURF.blit(item['text'][1], (item['xpos']-5, item['ypos']+15))
                DISPLAYSURF.blit(item['text'][2], (item['xpos']+item['width']-15, item['ypos']+15))
                pygame.draw.line(DISPLAYSURF, item['colour'], (item['xpos'], item['ypos']),
                                 (item['xpos']+item['width'], item['ypos']))
        for button in self._menu_items:
            if button['menu_type'] == 'Button':
                if button['persistence'] == False:
                    if button['rect'].collidepoint(pygame.mouse.get_pos()[0],
                            pygame.mouse.get_pos()[1]):
                        pygame.draw.rect(DISPLAYSURF, BLUE, button['rect'], 3)        
    
    def check_click(self, mouse_x, mouse_y):
        """Called in response to a user pressing the left mouse button, this
        method alters the button-highlights accordingly and then returns a
        list of tuples representing changes to the game state. The method is
        blind to the actual functionality of the buttons (and is thus re-usable
        for most conceivable functions.)

        check_click(float, float) -> list(tuple(int, str, var.))

        """

        check_list = []
        
        for button in self._menu_items:
            if (button['rect'].collidepoint(mouse_x, mouse_y) and
                button['menu_type'] == 'Button'):
                #highlights
                for item in self._menu_items:
                    if item['menu_type'] == 'Button':
                        if (item['function'] == button['function'] or
                            item['f_index'] == button['f_index']):
                            item['highlight'] = INACTIVE
                button['highlight'] = ACTIVE
                #functionality
                if button['persistence'] == False:
                    button['amount'] = True
                check_list.append((button['f_index'], button['function'],
                                   button['amount']))
                if button['menuChange']:
                    for item in self._menu_items:
                        if item['function'] == button['menuChange'][0]:
                            item[button['menuChange'][1]] = (
                             button['menuChange'][2])

        return check_list

    def grab_slider(self, mouse_x, mouse_y):
        """In response to the mouse button being pushed down, this method
        checks if a slider has been selected, and changes its state accordingly.

        grab_slider(float, float) -> None

        """

        for slider in self._menu_items:
            if slider['menu_type'] == 'Slider':
                if slider['rect'].collidepoint(mouse_x, mouse_y):
                    slider['grabbed'] = True
                
    def move_slider(self, mouse_x):
        """In response to mouse motion, move any selected sliders with the
        x-coordinate of the mouse.

        move_slider(float) -> None

        """

        for slider in self._menu_items:
            if slider['menu_type'] == 'Slider':
                if slider['grabbed'] == True:
                    if mouse_x > slider['xpos'] and mouse_x < (slider['xpos']
                        +slider['width']):
                        slider['rect'].move_ip(mouse_x-slider['rect'].centerx, 0)
                        
    def release_slider(self):
        """In response to a mouse-button-up, release any selected sliders
        and change their state according to their new position. Return the
        variable representing the resultant change to the simulation state.

        release_slider() -> var.

        """

        for slider in self._menu_items:
            if slider['menu_type'] == 'Slider':
                if slider['grabbed'] == True:
                    slider['amount'] = ((slider['rect'].centerx-
                           slider['xpos'])/slider['width'])*slider['max']
                    slider['grabbed'] = False
                return slider['amount']
