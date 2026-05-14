import pygame # main import
import os # for offsetting window open position
import ctypes

import screens
import functions
import classes
import time

import connection

from statics import *

os.system('cls') # clears the terminal

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

pygame.init() # initializing for other things incase they are needed

info = pygame.display.Info()

# Screen width and height
width, height = info.current_w, info.current_h

# Tell Windows your app is DPI aware to prevent double-scaling

# x and y offset of window open position
xOffset, yOffset = 0, 0

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xOffset,yOffset)

screen = pygame.display.set_mode((width,height)) # make the display object

font = pygame.font.Font('freesansbold.ttf', 32) # create font - (font, fontsize)

Running = True # set variable for stopping the loop


screens.container_dict["title"] = screens.title_screen_maker(screen)

screens.container_dict["codes"] = screens.update_codes_display(screen, 1)

screens.container_dict["editor"] = screens.editor_screen_maker(screen)


pygame.key.set_repeat(350, 35)


connection.setup_connection()

last_keep_alive = time.time()

while Running: # start the loop

    if time.time() - last_keep_alive > 10:

        connection.keep_alive_packet()

        last_keep_alive = time.time()

    screen.fill(grey)
    
    screens.container_dict[screens.current_container].draw()

    pygame.display.update() # update the frame of the display object
    
    for event in pygame.event.get(): # looks through all the events

        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # if red x/esc key press
            
            Running = False # stop the loop

            pygame.quit() # kill the pygame application
        
        # checks for left click down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            screens.container_dict[screens.current_container].click_check(pygame.mouse.get_pos(), True)

        # checks for left click up
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            screens.container_dict[screens.current_container].click_check(pygame.mouse.get_pos(), False)
        
        if event.type == pygame.KEYDOWN:
            if classes.currently_typing != None and functions.choosing_file == False:
                if event.unicode == "\b":
                    if len(classes.currently_typing.text) > 0:
                        classes.currently_typing.update_text(classes.currently_typing.text[:-1])
                else:
                    classes.currently_typing.update_text(classes.currently_typing.text + event.unicode)
