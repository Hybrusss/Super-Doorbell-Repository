import pygame # main import
import os # for offsetting window open position
from collections.abc import Callable
import ctypes

from screens import *
import functions
from screens import editor_screen_maker

from tkinter import Tk

import screens
import classes

from statics import *

os.system('cls') # clears the terminal

pygame.init() # initializing for other things incase they are needed

info = pygame.display.Info()

# Screen width and height
width, height = info.current_w, info.current_h

# Tell Windows your app is DPI aware to prevent double-scaling
try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass # Non-Windows platforms or older Windows versions

# x and y offset of window open position
xOffset, yOffset = 0, 0

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xOffset,yOffset)

screen = pygame.display.set_mode((width,height)) # make the display object

font = pygame.font.Font('freesansbold.ttf', 32) # create font - (font, fontsize)

Running = True # set variable for stopping the loop


container_dict["title"] = title_screen_maker(screen)

container_dict["edit"] = update_edit_display(screen, 1)

container_dict["editor"] = editor_screen_maker(screen)


pygame.key.set_repeat(350, 35)


while Running: # start the loop

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
            # print(container_dict, current_container)

        # checks for left click up
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            container_dict[current_container].click_check(pygame.mouse.get_pos(), False)
        
        if event.type == pygame.KEYDOWN:
            if classes.currently_typing != None and functions.choosing_file == False:
                if event.unicode == "\b":
                    if len(classes.currently_typing.text) > 0:
                        classes.currently_typing.update_text(classes.currently_typing.text[:-1])
                else:
                    classes.currently_typing.update_text(classes.currently_typing.text + event.unicode)
