import pygame
from classes import Element, Container
from functions import *
from connection import setup_connection, upload_data

from statics import *


# this is the page number that the 
# user was on before editing the
# code they are editing
last_viewed_page = 1

# will hold all of the separate Containers
# to be switched between
container_dict: dict[str: Container] = {}

current_container: str = "title"

# will hold all data that is relevant
# to the codes
# FORMAT: 
# [CODE] : {"Name"   : name,
#            "Sound" : sound data in bytes}
input_codes_data = {"123": {"Name": "test", "Sound": "D:/College Stuff/Computer Science/Freshman Year/Q3/superdoorbell/applepay.mp3"}}


# this is triggered when the user presses the back button
# on the code editing screen, it adds a code to the
# dictionary of codes if the code is valid, else it should
# provide the user with an error below the back button
def update_codes(screen, container: Container, the_error_object):

    def output_func():
        global current_container

        name_container = [x for x in container.elements.keys() if x.name == "Name Input"][0]
        code_container = [x for x in container.elements.keys() if x.name == "Code Input"][0]
        sound_container = [x for x in container.elements.keys() if x.name == "Sound Input Secret"][0]


            
        if not code_container.text.isdecimal():
            the_error_object.text = "Code must be a number"
            return 

        code = code_container.text
        if code in input_codes_data:
            the_error_object.text = "Code already in use"
            return
        
        else:
            name = name_container.text
            sound_path = sound_container.text
            input_codes_data[code] = {"Name": name, "Sound": sound_path}
        
        container_dict[current_container].being_drawn = False

        current_container = "codes"

        container_dict[current_container].being_drawn = True

        container_dict["codes"] = update_codes_display(screen, last_viewed_page)
    
    return output_func


def editor_screen_maker(screen: pygame.Surface):
    
    width = screen.get_width()
    height = screen.get_height()

    code_editor_screen = Container(screen)

    editor_background = Element((width/2-400, 100), (800, height-200), screen, dark_grey, "", black, "Box")
    back_button = Element((5, 5), (100, 75), screen, red, "back", black)

    name_type_box = Element((width/2-300, 250), (600, 100), screen, black, "", white, "Text Box", "Name Input")
    code_type_box = Element((width/2-300, 550), (600, 100), screen, black, "", white, "Text Box", "Code Input")
    sound_type_box = Element((width/2-300, 850), (600, 100), screen, black, "", white, "Text Box", "Sound Input")

    # will hold the full path of the sound to allow the
    # user to see a truncated version to account for 
    # excessive path size
    secret_sound_holder = Element((-100, -100), (0, 0), screen, grey, "", grey, "Text Box", "Sound Input Secret")

    name_label = Element((width/2-300, 150), (300, 100), screen, black, "Name", white, "Label")
    code_label = Element((width/2-300, 450), (300, 100), screen, black, "Code", white, "Label")
    sound_label = Element((width/2-300, 750), (300, 100), screen, black, "Sound", white, "Label")

    error_display = Element((5, 100), (300, 100), screen, black, "", red, "Label", "Error Display")


    code_editor_screen.add_element(editor_background, empty_function)

    code_editor_screen.add_element(name_type_box, empty_function)
    code_editor_screen.add_element(code_type_box, empty_function)
    code_editor_screen.add_element(sound_type_box, get_file_path(sound_type_box, secret_sound_holder))

    code_editor_screen.add_element(secret_sound_holder, empty_function)

    code_editor_screen.add_element(name_label, empty_function)
    code_editor_screen.add_element(code_label, empty_function)
    code_editor_screen.add_element(sound_label, empty_function)

    code_editor_screen.add_element(error_display, empty_function)

    code_editor_screen.add_element(back_button, update_codes(screen, code_editor_screen, error_display))

    return code_editor_screen


def update_codes_display(screen, page_number: int = None) -> Container:
    
    width = screen.get_width()
    height = screen.get_height()

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
        sound_display.update_text(beautify_path(str(input_codes_data[input_code]["Sound"])))

        output_container.add_element(data_background, empty_function)
        output_container.add_element(name_display, empty_function)
        output_container.add_element(code_display, empty_function)
        output_container.add_element(sound_display, empty_function)

        output_container.add_element(edit_background, empty_function)
        output_container.add_element(edit_button, swap_container_constructor(input_code, page_number))
        output_container.add_element(delete_code_button, delete_code_constructor(screen, input_code, page_number))

        new_code_button_y += 200

        # if 4 codes are displayed
        if new_code_button_y == 900:
            show_new_code_button = False
            break
    
    
    # if there are codes being displayed on screen
    if new_code_button_y != 100:

        name_label = Element((175, 15), (150, 75), screen, black, "Name", white)
        code_label = Element((575, 15), (150, 75), screen, black, "Code", white)
        sound_label = Element((975, 15), (150, 75), screen, black, "Sound", white)

        name_label.set_element_type("Box")
        code_label.set_element_type("Box")
        sound_label.set_element_type("Box")

        output_container.add_element(name_label, empty_function)
        output_container.add_element(code_label, empty_function)
        output_container.add_element(sound_label, empty_function)


    # if not on the first page we are going
    # to want to display a "back" arrow to
    # enable returning to previous pages
    if page_number != 1 > 0:
        previous_page_arrow = Element((width//3, height-150), (100, 100), screen, black, "<<", white)
        output_container.add_element(previous_page_arrow, page_switcher(screen, page_number - 1))

    # if not on the last page we are going
    # to want to display a "forward" arrow to
    # enable viewing new pages
    if page_number * 4 <= len(input_codes_data):
        next_page_arrow = Element((2*width//3, height-150), (100, 100), screen, black, ">>", white)
        output_container.add_element(next_page_arrow, page_switcher(screen, page_number + 1))


    upload_codes_button = Element((width-350, height-150), (300, 100), screen, purple, "Upload Data", white)
    import_codes_button = Element((50, height-150), (300, 100), screen, blue, "Import Data", white)
    export_codes_button = Element((width/2-150, height-150), (300, 100), screen, white, "Export Data", black)

    output_container.add_element(upload_codes_button, upload_data(input_codes_data))
    output_container.add_element(import_codes_button, get_file_data(screen))
    output_container.add_element(export_codes_button, save_file_path)

    back_button = Element((5, 5), (100, 75), screen, red, "back", black)
    output_container.add_element(back_button, swap_container_constructor("title"))

    if show_new_code_button:
        new_code_button = Element((width/2-150, new_code_button_y), (300, 100), screen, black, "Add Code", white)
        output_container.add_element(new_code_button, add_code(screen, page_number))
    
    output_container.being_drawn = True

    return output_container


# this function is triggered when the user presses the
# "add code" button on the screen that displays the codes
def add_code(screen, current_page: int = 1, number: int = 1, name: str = "1", path = ""):

    def output_func():

        global input_codes_data
        code = 1
        while str(code) in input_codes_data:
            code += 1
        input_codes_data[str(code)] = {"Name": name, "Sound": path}
        container_dict["codes"] = update_codes_display(screen, current_page)
    
    return output_func


def delete_code_constructor(screen, the_code, page_number):

    def output_func():
        global input_codes_data

        del input_codes_data[the_code]
        
        container_dict['codes'] = update_codes_display(screen, page_number)
    
    return output_func


# used when the user presses the left or right arrows
# at the bottom of the screens to view their codes
def page_switcher(screen, page_num):

    def output_func():

        container_dict["codes"] = update_codes_display(screen, page_num)
    
    return output_func


def swap_container_constructor(container_input_value, page_num = None):

    if type(container_input_value) == str and not container_input_value.isdecimal():

        def output_func():
            global current_container
            
            container_dict[current_container].being_drawn = False

            current_container = container_input_value

            container_dict[current_container].being_drawn = True

    elif container_input_value.isdecimal():

        def output_func():

            global current_container, last_viewed_page
            
            container_dict[current_container].being_drawn = False

            current_container = "editor"

            container_dict[current_container].being_drawn = True

            the_container: Container = container_dict["editor"]

            the_code = container_input_value

            name_box = [x for x in the_container.elements.keys() if x.position[1] == 250][0]
            code_box = [x for x in the_container.elements.keys() if x.position[1] == 550][0]
            sound_box = [x for x in the_container.elements.keys() if x.position[1] == 850][0]
            secret_sound_box = [x for x in the_container.elements.keys() if x.name == "Sound Input Secret"][0]

            name_box.update_text(input_codes_data[the_code]["Name"])
            sound_box.update_text(beautify_path(input_codes_data[the_code]["Sound"]))
            secret_sound_box.update_text(input_codes_data[the_code]["Sound"])
            code_box.update_text(str(the_code))


            if page_num is None:
                raise ValueError("Variable \"page_num\" was not given")
            last_viewed_page = page_num

            del input_codes_data[the_code]

            return output_func

            # This will be if the passed
            # in data is a code
            # it will fill the data
            # into the boxes unless its a blank
            # code
            pass
        
    return output_func


def title_screen_maker(screen):
    
    width = screen.get_width()
    height = screen.get_height()

    # will be the first screen that greets the user
    title_screen = Container(screen)

    # this button will be part of the connection process
    connect_button = Element((width/2-250, height/2-150), (500, 100), screen, red, "Connect to doorbell", black)

    # this button will allow users to edit doorbell settings prior to
    # connecting to their doorbell
    edit_button = Element((width/2-250, height/2+50), (500, 100), screen, red, "Edit", black)


    connection_display = Element((25, 25), (200, 100), screen, black, "Not Connected...", white, "Label", "Connection Box")


    title_screen.add_element(connect_button, setup_connection)
    title_screen.add_element(edit_button, swap_container_constructor("codes"))

    connection_display.set_element_type(False)

    title_screen.being_drawn = True

    return title_screen



    
def save_file_path():

    file = filedialog.asksaveasfile(
        initialfile='config.dbd',
        defaultextension=".dbd",
        filetypes=[("Doorbell Data","*.dbd"), ("All Files","*.*")]
    )
    
    if file:
        
        the_data_list = make_file_data(input_codes_data)

        for element in the_data_list:

            file.write(element)
            if element != the_data_list[-1]:
                file.write("\n")

        file.close()
    
def make_file_data(codes_data):
    output_list = []
    for code in codes_data:
        name = codes_data[code]["Name"]
        file_path = codes_data[code]["Sound"]

        output_list.append(f"{code}, {name}, {file_path}")
    
    return output_list
    
def get_file_data(screen):

    def output_func():

        global input_codes_data

        input_path = get_file_path("222")

        output_data = {}

        with open(input_path) as f:
            for line in f:
                line = line.strip().split(", ")
                the_code = line[0]
                the_name = line[1]
                the_path = line[2]

                output_data[the_code] = {"Name": the_name, "Sound": the_path}
        
        input_codes_data = output_data

        container_dict["codes"] = update_codes_display(screen, 1)
    
    return output_func