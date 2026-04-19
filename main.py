import pygame # main import
import os # for offsetting window open position
from collections.abc import Callable
import random
import time
import ctypes
from playsound import playsound
import threading

from tkinter import filedialog, Tk

# Hide the main Tkinter window
root = Tk()
root.withdraw()

the_sound_path = ""

def play_sound():
    sound_thread = threading.Thread(target=playsound, args=(the_sound_path,))
    sound_thread.start()
    
def empty_function():
    pass

def get_file_path():
    global the_sound_path
    file_path = filedialog.askopenfilename(initialdir=r"C:\Users\Ryan\Desktop\temp sounds")
    the_sound_path = file_path
    # playsound(the_sound_path)

# Tell Windows your app is DPI aware to prevent double-scaling
try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass # Non-Windows platforms or older Windows versions

# text = font.render('Example Text Here', True, black, green) # create font surface object (text, antialias, stroke, background)
# textRect = text.get_rect() # get the rectangle around the text
# textRect.center = (textRect.width//2, textRect.height//2) # set the center to the width/2 and the height/2, will appear in top left
# screen.blit(text, textRect) # draw the text to the screen on its rectangle

os.system('cls') # clears the terminal

pygame.init() # initializing for other things incase they are needed

black = (0,0,0)
white = (255, 255, 255)
grey = (128, 128, 128)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


info = pygame.display.Info()

# Screen width and height
width, height = info.current_w, info.current_h

# x and y offset of window open position
xOffset, yOffset = 0, 0

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xOffset,yOffset)

screen = pygame.display.set_mode((width,height)) # make the display object

font = pygame.font.Font('freesansbold.ttf', 32) # create font - (font, fontsize)

Running = True # set variable for stopping the loop

current_text = []

def darken_color(input_color: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple([x * 0.5 for x in input_color])

def brighten_color(input_color: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple([min(255, x * 2) for x in input_color])

class Button:

    def __init__(self, 
                    position: tuple[int, int], 
                    size: tuple[int, int], 
                    display: pygame.Surface, 
                    color: tuple[int, int, int],
                    text: str,
                    text_color: tuple[int, int, int]) -> None:
        
        self.position = position
        self.size = size
        self.display = display
        self.color = color
        self.text_color = text_color
        self.text = text
        self.pressed = False

        self.parent_container = None

        self.fit_text()


    @property
    def position(self) -> tuple[int, int]:
        return self._position

    @position.setter
    def position(self, value: tuple[int, int]) -> None:
        self._position = value
    
    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]) -> None:
        self._size = value
        
    @property
    def display(self) -> pygame.Surface:
        return self._display

    @display.setter
    def display(self, value: pygame.Surface) -> None:
        if type(value) != pygame.Surface:
            raise TypeError("Display value was not surface")
        self._display = value
    
    @property
    def color(self) -> tuple[int, int, int]:
        return self._color

    @color.setter
    def color(self, value: tuple[int, int, int]) -> None:
        self._color = value
    
    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value
    
    def set_parent(self, value) -> None:
        self.parent_container = value
    
    def fit_text(self, font_size: int = 32, buffer_size: int = 40):
    
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        text = self.font.render(self.text, True, self.text_color) 
        textRect = text.get_rect()

        while textRect.width > self.size[0] - buffer_size or textRect.height > self.size[1] - buffer_size:
            font_size -= 1
            self.font = pygame.font.Font('freesansbold.ttf', font_size)
            text = self.font.render(self.text, True, self.text_color) 
            textRect = text.get_rect()

        while textRect.width < self.size[0] - buffer_size and textRect.height < self.size[1] - buffer_size:
            font_size += 1
            self.font = pygame.font.Font('freesansbold.ttf', font_size)
            text = self.font.render(self.text, True, self.text_color) 
            textRect = text.get_rect()
        
    
    def draw(self, display: pygame.Surface = None) -> None:
        if not self.pressed:
            the_rect = self.position + self.size
        else:
            the_rect = (self.position[0], self.position[1]+10) + self.size

        the_rect_bottom = (self.position[0], self.position[1]+20) + self.size


        if display is None:
            display = self.display

        # bottom button
        pygame.draw.rect(   self.display,
                            darken_color(self.color),
                            the_rect_bottom,
                            border_radius = 15)
        
        # bottom button outline
        pygame.draw.rect(   self.display,
                            black,
                            the_rect_bottom,
                            width = 5,
                            border_radius = 15)
        
        # top button 
        pygame.draw.rect(   self.display,
                            self.color,
                            the_rect,
                            border_radius = 15)
        
        # top button outline
        pygame.draw.rect(   self.display,
                            black,
                            the_rect,
                            width = 5,
                            border_radius = 15)
        
        self.draw_button_text(the_rect, True, 2)
        

    def draw_button_text(self, button_rect: tuple[int, int], outline: bool = False, outline_thickness: int = 1):


        text = self.font.render(self.text, True, self.text_color) 
        textRect = text.get_rect()

        text_center = (button_rect[0] + self.size[0]//2, button_rect[1] + self.size[1]//2)

        if outline and self.text_color != black:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if (dx, dy) != (0, 0):
                        text_outline = self.font.render(self.text, True, black)
                        textRect_outline = text_outline.get_rect()
                        
                        temp_center = (text_center[0] + dx * outline_thickness, text_center[1] + dy * outline_thickness)

                        textRect_outline.center = temp_center
                        screen.blit(text_outline, textRect_outline)
        
        textRect.center = text_center
        screen.blit(text, textRect) 
        

    def click_check(self, position: tuple[int, int], down_click: bool) -> bool:
        if down_click:
            if self.parent_container == container_dict[current_container]:
                if self.position[0] < position[0] < self.position[0] + self.size[0]:
                    if self.position[1] < position[1] < self.position[1] + self.size[1]:
                        self.pressed = True
                        return True
        self.pressed = False
        return False


# effectively a different "screen",
# holds different buttons and can be
# switched between by pressing certain
# buttons
class Container:
    
    def __init__(self, display: pygame.Surface) -> None:
        self.buttons = {}
        self.display = display
    
    @property
    def buttons(self) -> dict[Button, Callable]:
        return self._buttons

    @buttons.setter
    def buttons(self, value: dict[Button, Callable]) -> None:
        self._buttons = value
        
    @property
    def display(self) -> pygame.Surface:
        return self._display

    @display.setter
    def display(self, value: pygame.Surface) -> None:
        if type(value) != pygame.Surface:
            raise TypeError("Display value was not surface")
        self._display = value
    
    def add_button(self, button: Button, trigger: Callable) -> None:
        self.buttons[button] = trigger
        button.set_parent(self)
    
    def draw(self, display: pygame.Surface = None) -> None:
        if display is None:
            for button, func in self.buttons.items():
                button.draw()
        else:
            for button, func in self.buttons.items():
                button.draw(display)
    
    def click_check(self, position: tuple[int, int], down_click: bool) -> None:
        for button, func in self.buttons.items():
            if button.click_check(position, down_click):
                func()
                button.click_check(position, down_click)


def make_keypad():

    button_list: list[Button] = []

    button_symbols = [1, 2, 3, 4, 5, 6, 7, 8, 9, "«", 0, "OK"]
    button_symbols = [str(x) for x in button_symbols]
    symbol_idx = 0


    for y in range(4):
        for x in range(3):
            button_list.append(Button(((x+1)*120, (y+1)*140), (100, 100), screen, red, button_symbols[symbol_idx], red))
            symbol_idx += 1
    
    return button_list


def type_number_contructor(input: str):
    if input == "«":
        def type_number():
            text_button.text = text_button.text[:-1]
    elif input == "OK":
        def type_number():
            text_button.text = ""
    else:
        def type_number():
            text_button.text += input
    
    return type_number


def swap_container_contstructor(new_container_name):

    def output_func():
        global current_container
        current_container = new_container_name
    
    return output_func


# will hold all of the separate Containers
# to be switched between
container_dict = {}

current_container = "title"

# make the testing buttons screen
testing_buttons = Container(screen)

for button in make_keypad():
    testing_buttons.add_button(button, type_number_contructor(button.text))

get_file_button = Button((600, 800), (100, 100), screen, red, "open file", red)
text_button = Button((600, 400), (700, 100), screen, black, "", green)
sound_button = Button((600, 600), (100, 100), screen, red, "Play Sound", red)

testing_buttons.add_button(get_file_button, get_file_path)
testing_buttons.add_button(sound_button, play_sound)
testing_buttons.add_button(text_button, text_button.text)

container_dict["testing"] = testing_buttons


# will be the first screen that greets the user
title_screen = Container(screen)

# this button will be part of the connection process
connect_button = Button((width/2-250, height/2-150), (500, 100), screen, red, "Connect to doorbell", black)

# this button will allow users to edit doorbell settings prior to
# connecting to their doorbell
edit_button = Button((width/2-250, height/2+50), (500, 100), screen, red, "Edit offline", black)

title_screen.add_button(connect_button, empty_function)
title_screen.add_button(edit_button, swap_container_contstructor("edit"))

container_dict["title"] = title_screen

edit_screen = Container(screen)

back_button = Button((50, 50), (100, 100), screen, green, "back", black)

edit_screen.add_button(back_button, swap_container_contstructor("title"))

container_dict["edit"] = edit_screen


while Running: # start the loop

    screen.fill(grey)
    
    container_dict[current_container].draw()

    pygame.display.update() # update the frame of the display object
    
    for event in pygame.event.get(): # looks through all the events

        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # if red x/esc key press
            
            Running = False # stop the loop

            pygame.quit() # kill the pygame application
        
        # checks for left click down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            container_dict[current_container].click_check(pygame.mouse.get_pos(), True)

        # checks for left click up
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            container_dict[current_container].click_check(pygame.mouse.get_pos(), False)

