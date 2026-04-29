import pygame # main import
import os # for offsetting window open position
from collections.abc import Callable
import random
import time
import ctypes
# from playsound import playsound
import threading

from tkinter import filedialog, Tk

# Hide the main Tkinter window
root = Tk()
root.withdraw()

the_sound_path = ""

# will hold all data that is relevant
# to the codes
# FORMAT: 
# [CODE] : {"Name"   : name,
#            "Sound" : sound data in bytes}
input_codes_data = {}
current_editing_code = None

# this is the page number that the 
# user was on before editing the
# code they are currently editing
last_viewed_page = 1

def play_sound():
    pass
#     sound_thread = threading.Thread(target=playsound, args=(the_sound_path,))
#     sound_thread.start()
    
def empty_function():
    pass

def connect_function():
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

doorbell_ip = '127.0.0.1'
the_socket = None


def setup_connection():
    global doorbell_ip, the_socket
    doorbell_ip = getDoorbellIP()
    if doorbell_ip != '127.0.0.1':
        the_socket = connectToPi(doorbell_ip)
    else:
        the_socket = None

# setup_connection()

def send_packet_data():
    packet = rqPacket(bytes(256))
    packet.kind = 1
    packet.size = 17
    packet.mainData = b"123456789\x00{SOUND FILE AS BYTES LAOLOOOl}"
    retPack = pcSendPacket(the_socket, packet)
    print(retPack.mainData)



os.system('cls') # clears the terminal

pygame.init() # initializing for other things incase they are needed

black = (0,0,0)
white = (255, 255, 255)
grey = (128, 128, 128)
dark_grey = (92, 92, 92)
red = (255, 64, 64)
green = (64, 255, 64)
blue = (64, 64, 255)
purple = (128, 64, 255)


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

class Element:

    def __init__(self, 
                    position: tuple[int, int], 
                    size: tuple[int, int], 
                    display: pygame.Surface, 
                    color: tuple[int, int, int],
                    text: str,
                    text_color: tuple[int, int, int],
                    element_type: str = "Button") -> None:
        
        self.position = position
        self.size = size
        self.display = display
        self.color = color
        self.text_color = text_color
        self.text = text

        self.element_type = element_type
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
    
    def set_element_type(self, value) -> None:
        self.element_type = value
    
    def update_text(self, value) -> None:
        self.text = value
        self.fit_text()
    
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

        if self.element_type == "Button":
            # button bottom
            pygame.draw.rect(   self.display,
                                darken_color(self.color),
                                the_rect_bottom,
                                border_radius = 15)
            
            # button bottom outline
            pygame.draw.rect(   self.display,
                                black,
                                the_rect_bottom,
                                width = 5,
                                border_radius = 15)
        
        # element 
        pygame.draw.rect(   self.display,
                            self.color,
                            the_rect,
                            border_radius = 15)
        
        # element outline
        pygame.draw.rect(   self.display,
                            black,
                            the_rect,
                            width = 5,
                            border_radius = 15)
        
        self.draw_element_text(the_rect, True, 2)
        

    def draw_element_text(self, button_rect: tuple[int, int], outline: bool = False, outline_thickness: int = 1):


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

        # if the click was not a down click
        # or
        # if the element is not a button or a text box
        if not down_click or self.element_type not in ["Button", "Text Box"]:
            self.pressed = False
            return False

        # if the element is not currently being drawn

        print(current_container)
        if self.parent_container != container_dict[current_container]:
            self.pressed = False
            return False
        
        # if the element does not have the correct x position
        if position[0] < self.position[0] or self.position[0] + self.size[0] < position[0]:
            self.pressed = False
            return False

        # if the element does not have the correct y position
        if position[1] < self.position[1] or self.position[1] + self.size[1] < position[1]:
            self.pressed = False
            return False

        if self.element_type == "Text Box":
            global currently_typing
            currently_typing = self
            return True

        elif self.element_type == "Button":
            self.pressed = True
            return True



# if a text box element is selected,
# this variable will hold the element
# that is currently selected
currently_typing: Element = None

# effectively a different "screen",
# holds different elements and can be
# switched between by pressing certain
# buttons
class Container:
    
    def __init__(self, display: pygame.Surface) -> None:
        self.elements: dict[Element, Callable] = {}
        self.display = display
    
    @property
    def elements(self) -> dict[Element, Callable]:
        return self._elements

    @elements.setter
    def elements(self, value: dict[Element, Callable]) -> None:
        self._elements = value
        
    @property
    def display(self) -> pygame.Surface:
        return self._display

    @display.setter
    def display(self, value: pygame.Surface) -> None:
        if type(value) != pygame.Surface:
            raise TypeError("Display value was not surface")
        self._display = value
    
    def add_element(self, element: Element, trigger: Callable) -> None:
        self.elements[element] = trigger
        element.set_parent(self)
    
    def draw(self, display: pygame.Surface = None) -> None:
        if display is None:
            for element, func in self.elements.items():
                element.draw()
        else:
            for element, func in self.elements.items():
                element.draw(display)
    
    def click_check(self, position: tuple[int, int], down_click: bool) -> None:
        for element, func in self.elements.items():
            if element.click_check(position, down_click):
                func()
                element.click_check(position, down_click)


def make_keypad():

    button_list: list[Element] = []

    button_symbols = [1, 2, 3, 4, 5, 6, 7, 8, 9, "«", 0, "OK"]
    button_symbols = [str(x) for x in button_symbols]
    symbol_idx = 0


    for y in range(4):
        for x in range(3):
            button_list.append(Element(((x+1)*120, (y+1)*140), (100, 100), screen, red, button_symbols[symbol_idx], red))
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


def swap_container_constructor(container_input_value, page_num = None):

    if type(container_input_value) == str:
        def output_func():
            global current_container
            current_container = container_input_value
    else:
        def output_func():
            global current_container, current_editing_code, last_viewed_page
            current_container = "editor"
            current_editing_code = container_input_value
            the_container: Container = container_dict["editor"]

            name_box = [x for x in the_container.elements.keys() if x.position[1] == 200][0]
            code_box = [x for x in the_container.elements.keys() if x.position[1] == 400][0]
            sound_box = [x for x in the_container.elements.keys() if x.position[1] == 600][0]

            name_box.update_text(input_codes_data[current_editing_code]["Name"])
            sound_box.update_text(input_codes_data[current_editing_code]["Sound"])
            code_box.update_text(str(current_editing_code))


            if page_num is None:
                raise ValueError("Variable \"page_num\" was not given")
            last_viewed_page = page_num

            return output_func

            # This will be if the passed
            # in data is a code
            # it will fill the data
            # into the boxes unless its a blank
            # code
            pass
        
    return output_func






# will hold all of the separate Containers
# to be switched between
container_dict = {}

current_container = "title"



# make the testing buttons screen
testing_buttons = Container(screen)

for button in make_keypad():
    testing_buttons.add_element(button, type_number_contructor(button.text))

get_file_button = Element((600, 800), (100, 100), screen, red, "open file", red)
text_button = Element((600, 400), (700, 100), screen, black, "", green)
sound_button = Element((600, 600), (100, 100), screen, red, "Play Sound", red)

testing_buttons.add_element(get_file_button, get_file_path)
testing_buttons.add_element(sound_button, play_sound)
testing_buttons.add_element(text_button, text_button.text)

container_dict["testing"] = testing_buttons



# will be the first screen that greets the user
title_screen = Container(screen)

# this button will be part of the connection process
connect_button = Element((width/2-250, height/2-150), (500, 100), screen, red, "Connect to doorbell", black)

# this button will allow users to edit doorbell settings prior to
# connecting to their doorbell
edit_button = Element((width/2-250, height/2+50), (500, 100), screen, red, "Edit offline", black)


connection_display = Element((25, 25), (200, 100), screen, black, "Not Connected...", white)


title_screen.add_element(connect_button, setup_connection)
title_screen.add_element(edit_button, swap_container_constructor("edit"))
title_screen.add_element(connection_display, empty_function)

connection_display.set_element_type(False)

container_dict["title"] = title_screen



edit_screen = Container(screen)



def update_edit_display(page_number: int = None) -> Container:

    output_container = Container(screen)

    new_code_button_y = 100

    # if we have 4 codes on one screen the
    # "new code" button needs to be on the
    # next screen that does not have 4 
    # codes on it
    show_new_code_button = True

    # amount of codes to skip over displaying
    # based on which page of the codes is
    # being viewed at the time
    # (number starts at 1)
    skip_amount = (page_number-1) * 4

    for input_code in input_codes_data.keys():
        print(input_codes_data, 1)

        if skip_amount > 0:
            skip_amount -= 1
            continue

        edit_button = Element((1325, new_code_button_y+15), (200, 100), screen, green, "Edit Code", white)
        delete_code_button = Element((1575, new_code_button_y+15), (200, 100), screen, red, "Delete Code", white)

        data_background = Element((100, new_code_button_y), (1100, 150), screen, dark_grey, "", black)
        edit_background = Element((1300, new_code_button_y), (500, 150), screen, dark_grey, "", black)
        name_display = Element((125, new_code_button_y+25), (250, 100), screen, black, "", white)
        code_display = Element((525, new_code_button_y+25), (250, 100), screen, black, "", white)
        sound_display = Element((925, new_code_button_y+25), (250, 100), screen, black, "", white)

        data_background.set_element_type("Box")
        edit_background.set_element_type("Box")
        name_display.set_element_type("Box")
        code_display.set_element_type("Box")
        sound_display.set_element_type("Box")

        name_display.update_text(str(input_codes_data[input_code]["Name"]))
        code_display.update_text(str(input_code))
        sound_display.update_text(str(input_codes_data[input_code]["Sound"]))

        output_container.add_element(data_background, empty_function)
        output_container.add_element(name_display, empty_function)
        output_container.add_element(code_display, empty_function)
        output_container.add_element(sound_display, empty_function)

        output_container.add_element(edit_background, empty_function)
        output_container.add_element(edit_button, swap_container_constructor(input_code, page_number))
        output_container.add_element(delete_code_button, delete_code_constructor(input_code))

        new_code_button_y += 200

        # if 4 codes are displayed
        if new_code_button_y == 900:
            show_new_code_button = False
            break


    # if not on the first page we are going
    # to want to display a "back" arrow to
    # enable returning to previous pages
    if page_number != 1 > 0:
        previous_page_arrow = Element((width//3, height-150), (100, 100), screen, black, "<<", white)
        output_container.add_element(previous_page_arrow, page_switcher_constructor(page_number - 1))

    # if not on the last page we are going
    # to want to display a "forward" arrow to
    # enable viewing new pages
    if page_number * 4 <= len(input_codes_data):
        next_page_arrow = Element((2*width//3, height-150), (100, 100), screen, black, ">>", white)
        output_container.add_element(next_page_arrow, page_switcher_constructor(page_number + 1))


    upload_codes_button = Element((width-350, height-150), (300, 100), screen, purple, "Upload Data", white)
    import_codes_button = Element((50, height-150), (300, 100), screen, blue, "Import Data", white)
    export_codes_button = Element((width/2-150, height-150), (300, 100), screen, white, "Export Data", black)

    output_container.add_element(upload_codes_button, send_packet_data)
    output_container.add_element(import_codes_button, empty_function)
    output_container.add_element(export_codes_button, empty_function)

    back_button = Element((5, 5), (100, 75), screen, red, "back", black)
    output_container.add_element(back_button, swap_container_constructor("title"))

    if show_new_code_button:
        new_code_button = Element((width/2-150, new_code_button_y), (300, 100), screen, black, "Add Code", white)
        output_container.add_element(new_code_button, add_code_constructor(page_number))

    return output_container

def add_code_constructor(current_page: int = 1, number: int = 1, name: str = "1", data = "1"):

    def output_func():

        global input_codes_data
        input_codes_data[len(input_codes_data)] = {"Name": name, "Sound": data}
        container_dict["edit"] = update_edit_display(current_page)
    
    return output_func


def delete_code_constructor(number):

    def output_func():
        global input_codes_data
        del input_codes_data[number]
        i = number+1
        while i in input_codes_data:
            input_codes_data[i-1] = input_codes_data[i]
            del input_codes_data[i]
            i += 1
        
        container_dict['edit'] = update_edit_display(1)
    
    return output_func

def page_switcher_constructor(page_num):

    def output_func():

        container_dict["edit"] = update_edit_display(page_num)
    
    return output_func


container_dict["edit"] = update_edit_display(1)

def update_code_constructor(container: Container):

    def output_func():
        global current_container
        #name code sound

        name_container = [x for x in container.elements.keys() if x.position[1] == 200][0]
        code_container = [x for x in container.elements.keys() if x.position[1] == 400][0]
        sound_container = [x for x in container.elements.keys() if x.position[1] == 600][0]

        print(current_editing_code)
        print(input_codes_data)
        
        input_codes_data[current_editing_code]["Name"] = name_container.text
        input_codes_data[current_editing_code]["Sound"] = sound_container.text

        if int(code_container.text) in input_codes_data:
            return

        input_codes_data[int(code_container.text)] = input_codes_data[current_editing_code]
        del input_codes_data[current_editing_code]

        current_container = "edit"

        container_dict["edit"] = update_edit_display(last_viewed_page)
    
    return output_func
    


code_editor_screen = Container(screen)

editor_background = Element((width/2-400, 100), (800, height-200), screen, dark_grey, "", black, "Box")
back_button = Element((5, 5), (100, 75), screen, red, "back", black)

name_type_box = Element((width/2-300, 200), (600, 100), screen, black, "", white, "Text Box")
code_type_box = Element((width/2-300, 400), (600, 100), screen, black, "", white, "Text Box")
sound_type_box = Element((width/2-300, 600), (600, 100), screen, black, "", white, "Text Box")

code_editor_screen.add_element(editor_background, empty_function)
code_editor_screen.add_element(name_type_box, empty_function)
code_editor_screen.add_element(code_type_box, empty_function)
code_editor_screen.add_element(sound_type_box, empty_function)
code_editor_screen.add_element(back_button, update_code_constructor(code_editor_screen))


container_dict["editor"] = code_editor_screen




pygame.key.set_repeat(350, 35)


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
        
        if event.type == pygame.KEYDOWN:
            if currently_typing != None:
                if event.unicode == "\b":
                    if len(currently_typing.text) > 0:
                        currently_typing.update_text(currently_typing.text[:-1])
                else:
                    currently_typing.update_text(currently_typing.text + event.unicode)
