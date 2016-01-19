
import random, sys, time, math, pygame, os
from pygame.locals import *
import stellar
import menu
import save
from constants import *

x = 90
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

def main():
    """Main function for the script. Sets up some global variables
    and initialises the pygame display window. Then runs the game loop.

    """
    global DISPLAYSURF, FPSCLOCK
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Gravity Sim')
        
    run_sim()
    

def run_sim():
    """The Game Loop. Contains the primary functionality of the simulation.
    The function is separated into a section for definitions and a section
    for the running loop.
    The definitions section initialises the object list, the coordinate
    scheme, the menu and some other default values.
    The main loop is organised into code segments which handle the time
    variables, colliding objects, object movement, drawing the objects/menu,
    and user interaction (event loop). 

    """

    SCALE = 1
    circles = []
    intCirc = [0, 0]
    lastFrame = 0
    velocity = 0
    planet_colour = BLUE
    star_colour = ORANGE
    draw_x = ((WINWIDTH-MENUWIDTH)*0.5+MENUWIDTH)
    draw_y = 0.5*WINHEIGHT
    mainMenu = menu.Menu(MENUWIDTH, WINHEIGHT)
    default_main(mainMenu, MENUWIDTH, WINHEIGHT)
    time_scale = 1
    #default selections
    _selection_list = ([False, PLANET, (0, 0), UP, False, False, False, False,
                       star_colour, planet_colour])
    # Reset Point
    current_save = save.Save(circles)
    
    while True:
        
        DISPLAYSURF.fill((0, 0, 0))
        

        # # # # TIME STUFF # # # #
        
        totalTime = pygame.time.get_ticks()
        delta = (totalTime - lastFrame)/1000
        lastFrame = totalTime
        scaled_delta = delta*time_scale

        # # # #            # # # #


        # Collisions #

        if len(circles) > 1:
            for i in range(len(circles) - 1, -1, -1):
                for j in range(len(circles) - 1, -1, -1):
                    if i == j: continue
                    if circles[i].check_collide(circles[j]):
                        if (circles[i].starMass) < (circles[j].starMass):
                            circles[j].absorb(circles[i])
                            circles.remove(circles[i])
                            break
                        else:
                            circles[i].absorb(circles[j])
                            circles.remove(circles[j])
                            i -= 1
                            break
        
        
        # Movement #

        for circ1 in circles:
            accelVector_x = 0
            accelVector_y = 0
            change_x = 0
            change_y = 0
            if len(circles) > 1:
                for circ in circles:

                    if circ1.xpos == circ.xpos and circ1.ypos == circ.ypos:
                        continue
                    dist_x = circ.xpos - circ1.xpos
                    dist_y = circ.ypos - circ1.ypos

                    accelTuple = circ1.grav_builder(dist_x, dist_y, circ.starMass)
                    accelVector_x += accelTuple[0]
                    accelVector_y += accelTuple[1]
                        
            circ1.vel_x += accelVector_x*abs(scaled_delta)
            circ1.vel_y += accelVector_y*abs(scaled_delta)
            change_x += circ1.vel_x*scaled_delta*60*60*24*30 #seconds in 30 days
            change_y += circ1.vel_y*scaled_delta*60*60*24*30

            circ1.move_stellar(change_x, change_y)
            
        # Draw the objects #
        for circ in circles:
            intCirc[0] = int(round(circ.xpos)*(SCALE) + draw_x)
            intCirc[1] = int(round(circ.ypos)*(SCALE) + draw_y)
            if 0 < intCirc[0] < WINWIDTH and 0 < intCirc[1] < WINHEIGHT:
                if circ.starMass > 59700000000000000000000000000:
                    pygame.draw.circle(DISPLAYSURF, star_colour, intCirc, round(circ.starRadius*SCALE))
                else:
                    pygame.draw.circle(DISPLAYSURF, planet_colour, intCirc, round(circ.starRadius*SCALE))

        # Draw the menu and labels#
        mainMenu.draw(DISPLAYSURF)
        font1 = pygame.font.Font(None, 22)
        instructions = font1.render(("Reset: R       Save: S       "
            +"Speed: Left/Right arrows       Zoom: Up/Down arrows"), 1, WHITE)
        DISPLAYSURF.blit(instructions, (MENUWIDTH+30, 10))
        

        # Reset placement booleans

        _selection_list[0] = False
        _selection_list[4] = False
        _selection_list[5] = False
        _selection_list[6] = False

        # Event handling loop.
        
        for event in pygame.event.get(): 
            if event.type == QUIT:
                quit_game()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    check_list = mainMenu.check_click(event.pos[0], event.pos[1])
                    mainMenu.grab_slider(event.pos[0], event.pos[1])
                    for selection in check_list:
                        change_index = selection[0]
                        change_amount = selection[2]
                        _selection_list[change_index] = change_amount
                        if change_index == 2:
                            _selection_list[7] = False
                    placeNow = _selection_list[0]
                    placeType = _selection_list[1]
                    objShift_x = _selection_list[2][0]
                    objShift_y = _selection_list[2][1]
                    direction = _selection_list[3]
                    velocity_x = velocity*direction[0]
                    velocity_y = velocity*direction[1]
                    binaryPlace = _selection_list[4]
                    solPlace = _selection_list[5]
                    messPlace = _selection_list[6]
                    click_select = _selection_list[7]
                    star_colour = _selection_list[8]
                    planet_colour = _selection_list[9]
                    if placeNow == True:
                        if placeType == STAR:
                            circles.append(stellar.Star(objShift_x,
                                objShift_y, 1990000000000000000000000000000, 
                                        STAR_RADIUS, velocity_x, velocity_y))
                        elif placeType == PLANET:
                            circles.append(stellar.Star(objShift_x,
                                objShift_y, 5970000000000000000000000,
                                        PLANET_RADIUS, velocity_x, velocity_y))
                    if binaryPlace == True:
                        first, second = make_binary()
                        circles.append(first)
                        circles.append(second)
                    if solPlace == True:
                        field_array = field()
                        for planet in field_array:
                            circles.append(planet)
##                        sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune = sol()
##                        circles.append(sun)
##                        circles.append(mercury)
##                        circles.append(venus)
##                        circles.append(earth)
##                        circles.append(mars)
##                        circles.append(jupiter)
##                        circles.append(saturn)
##                        circles.append(uranus)
##                        circles.append(neptune)
                    if messPlace == True:
                        mess_array = mess()
                        for mystery in mess_array:
                            circles.append(mystery)
                    if click_select == True:
                        if event.pos[0] > MENUWIDTH:
                            _selection_list[2] = ((event.pos[0] - draw_x)/SCALE,
                                (event.pos[1] - draw_y)/SCALE)
            elif event.type == pygame.MOUSEMOTION:
                mainMenu.move_slider(event.pos[0])
            elif event.type == pygame.MOUSEBUTTONUP:
                velocity = mainMenu.release_slider()
                if not velocity or velocity < 1000:
                    velocity = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    current_save = save.Save(circles)
                if event.key == pygame.K_r:
                    circles = current_save.reset()
                if event.key == pygame.K_UP:
                    SCALE*=1.5
                if event.key == pygame.K_DOWN:
                    SCALE/=1.5
                if event.key == pygame.K_RIGHT:
                    time_scale+=1
                if event.key == pygame.K_LEFT:
                    if time_scale > 0:
                        time_scale-=1
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
                    

def default_main(menu, MENUWIDTH, MENUHEIGHT):
    """Initialises the menu, creating the buttons and the slider, and
    deciding their functionality.

    default_main(menu, float, float) -> None

    """

    ACTIVE = 'active'
    INACTIVE = 'inactive'

    #Menu Boxes

    menu.create_button((0.17*MENUWIDTH, 0.89*MENUHEIGHT, 130,
        40, WHITE, 'Place', (0, 'Place'), True, INACTIVE, False, None))
    menu.create_button((0.11*MENUWIDTH, 0.11*MENUHEIGHT, 60,
        25, RED, STAR, (1, 'typeChange_s'), STAR, INACTIVE, True, None))
    menu.create_button((0.56*MENUWIDTH, 0.11*MENUHEIGHT, 60,
        25, BLUE, PLANET, (1, 'typeChange_p'), PLANET, ACTIVE, True, None))
    menu.create_button((0.22*MENUWIDTH, 0.21*MENUHEIGHT, 110,
        25, WHITE, 'Pos: 1', (2, 'Position'), (0, 0), ACTIVE, True, None))
    menu.create_button((0.22*MENUWIDTH, 0.26*MENUHEIGHT, 110,
        25, WHITE, 'Pos: 2', (2, 'Position'), (-200, 0), INACTIVE, True, None))
    menu.create_button((0.47*MENUWIDTH - 10, 0.56*MENUHEIGHT, 20,
        20, WHITE, None, (3, 'Direction'), UP, ACTIVE, True, None))
    menu.create_button((0.47*MENUWIDTH - 35, 0.56*MENUHEIGHT+25, 20,
        20, WHITE, None, (3, 'Direction'), LEFT, INACTIVE, True, None))
    menu.create_button((0.47*MENUWIDTH - 10, 0.56*MENUHEIGHT+50, 20,
        20, WHITE, None, (3, 'Direction'), DOWN, INACTIVE, True, None))
    menu.create_button((0.47*MENUWIDTH + 15, 0.56*MENUHEIGHT+25, 20,
        20, WHITE, None, (3, 'Direction'), RIGHT, INACTIVE, True, None))
    menu.create_button((0.17*MENUWIDTH, 0.72*MENUHEIGHT, 130, 30,
        WHITE, 'Binary Stars', (4, 'Binary'), True, INACTIVE, False, None))
    menu.create_button((0.17*MENUWIDTH, 0.77*MENUHEIGHT, 130, 30,
        WHITE, 'Sol', (5, 'Sol'), True, INACTIVE, False, None))
    menu.create_button((0.17*MENUWIDTH, 0.82*MENUHEIGHT, 130, 30,
        WHITE, 'Mess', (6, 'Mess'), True, INACTIVE, False, None))
    menu.create_button((0.22*MENUWIDTH, 0.31*MENUHEIGHT, 110,
        25, WHITE, 'Pos: Click', (7, 'Position'), True, INACTIVE, True, None))
    menu.create_button((0.11*MENUWIDTH, 0.08*MENUHEIGHT, 10,
        10, RED, '', (8, 'colourChange_s'), RED, INACTIVE, True, ('typeChange', 'colour', RED)))
    menu.create_button((0.21*MENUWIDTH, 0.08*MENUHEIGHT, 10,
        10, WHITE, '', (8, 'colourChange_s'), WHITE, INACTIVE, True, ('typeChange', 'colour', WHITE)))
    menu.create_button((0.31*MENUWIDTH, 0.08*MENUHEIGHT, 10,
        10, ORANGE, '', (8, 'colourChange_s'), ORANGE, ACTIVE, True, ('typeChange', 'colour', ORANGE)))
    menu.create_button((0.56*MENUWIDTH, 0.08*MENUHEIGHT, 10,
        10, BLUE, '', (9, 'colourChange_p'), BLUE, ACTIVE, True, ('typeChange_2', 'colour', BLUE)))
    menu.create_button((0.66*MENUWIDTH, 0.08*MENUHEIGHT, 10,
        10, WHITE, '', (9, 'colourChange_p'), WHITE, INACTIVE, True, ('typeChange_2', 'colour', WHITE)))
    menu.create_button((0.76*MENUWIDTH, 0.08*MENUHEIGHT, 10,
        10, GREEN, '', (9, 'colourChange_p'), GREEN, INACTIVE, True, ('typeChange_2', 'colour', GREEN)))

    #Velocity Slider
    
    menu.create_slider((0.15*MENUWIDTH, 0.47*MENUHEIGHT, 140, 12, BLACK,
        ('Velocity (km/s)', '0', '60,000'), 'Velocity', 0, 60000))


def make_binary():
    """Creates a binary star system. The stars are identical, but with
    opposite velocities and different positions.

    make_binary() -> (stellar, stellar)
    
    """

    first = stellar.Star(-150, 0, 1990000000000000000000000000000, STAR_RADIUS, 0, 15000)
    second = stellar.Star(150, 0, 1990000000000000000000000000000, STAR_RADIUS, 0, -15000)

    return first, second

def sol():
    """Creates a model of the Earth's solar system. Each of the eight planets
    has an accurate position, mass and velocity.

    sol() -> (stellar x 8)

    """
    sun = stellar.Star(0, 0, 1990000000000000000000000000000, STAR_RADIUS+3, 0, 0)
    mercury = stellar.Star(-77, 0, 328000000000000000000000, PLANET_RADIUS+2, 0, 47000)
    venus = stellar.Star(-145, 0, 4870000000000000000000000, PLANET_RADIUS+2, 0, 35021)
    earth = stellar.Star(-200, 0, 5970000000000000000000000, PLANET_RADIUS+2, 0, 30000)
    mars = stellar.Star(-305, 0, 639000000000000000000000, PLANET_RADIUS+2, 0, 24131)
    jupiter = stellar.Star(-1041, 0, 1900000000000000000000000000, PLANET_RADIUS+3, 0, 13070)
    saturn = stellar.Star(-1916, 0, 568000000000000000000000000, PLANET_RADIUS+3, 0, 9673)
    uranus = stellar.Star(-3846, 0, 86800000000000000000000000, PLANET_RADIUS+3, 0, 6835)
    neptune = stellar.Star(-6020, 0, 102000000000000000000000000, PLANET_RADIUS+3, 0, 5478)


    return sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune

def mess():
    """Creates a random, messy series of objects.

    mess() -> (tuple(stellar x 50))

    """

    mess = []
    for i in range(0, 26):
       mess.append(stellar.Star(random.randint(-800, 800),
            random.randint(-600, 600), random.randint(328000000000000000000,
                1990000000000000000000000000000), random.randint(PLANET_RADIUS,
                    STAR_RADIUS), random.randint(-20000, 20000),
                        random.randint(-20000, 20000)))
    for i in range(0, 26):
       mess.append(stellar.Star(random.randint(-600, 600),
            random.randint(-600, 600), random.randint(3280000000000,
                1900000000000000000000000000), random.randint(PLANET_RADIUS,
                    STAR_RADIUS), random.randint(-100000, 100000),
                        random.randint(-100000, 100000)))
    return mess

def field():

    field = []
    for i in range(0, 11):
        for j in range(0, 11):
            field.append(stellar.Star(i*15, j*15, 5970000000000000000000000, PLANET_RADIUS,
                                  random.randint(-1000, 0), 0))
            field.append(stellar.Star(-1*i*15, j*15, 5970000000000000000000000, PLANET_RADIUS,
                                  0, random.randint(-1000, 0)))
            field.append(stellar.Star(i*15, -1*j*15, 5970000000000000000000000, PLANET_RADIUS,
                                  0, random.randint(0, 1000)))
            field.append(stellar.Star(-1*i*15, -1*j*15, 5970000000000000000000000, PLANET_RADIUS,
                                  random.randint(0, 1000), 0))
        
        
    return field

def quit_game():
    """Terminates pygame and ends the program."""
    pygame.quit()
    sys.exit()
    


if __name__ == '__main__':
    main()
