import pygame # main import
from functions import darken_color
from collections.abc import Callable


from statics import *


# these are the elements that will be drawn to the screen
class Element:

    def __init__(self, 
                    position: tuple[int, int], 
                    size: tuple[int, int], 
                    display: pygame.Surface, 
                    color: tuple[int, int, int],
                    text: str,
                    text_color: tuple[int, int, int],
                    element_type: str = "Button",
                    name: str = "") -> None:
        
        self.position = position
        self.size = size
        self.display = display
        self.color = color
        self.text_color = text_color
        self.text = text
        self.name = name

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
        self.fit_text()
    
    def set_parent(self, value) -> None:
        self.parent_container = value
    
    def set_element_type(self, value) -> None:
        self.element_type = value
    
    def update_text(self, value) -> None:
        self.text = value
        self.fit_text()
    
    def fit_text(self, font_size: int = 32, buffer_size: int = 40):
    
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        the_size = self.font.size(self.text)
        width_multiple = the_size[0] / (self.size[0] - buffer_size)
        height_multiple = the_size[1] / (self.size[1] - buffer_size)
        if max(width_multiple, height_multiple) > 0:
            font_size = int(font_size / max(width_multiple, height_multiple))
        else:
            return


        # text = self.font.render(self.text, True, self.text_color) 

        while the_size[0] > self.size[0] - buffer_size or the_size[1] > self.size[1] - buffer_size:
            font_size -= 1
            self.font = pygame.font.Font('freesansbold.ttf', font_size)
            the_size = self.font.size(self.text)
            # text = self.font.render(self.text, True, self.text_color) 
            # the_size = text.get_rect()

        while the_size[0] < self.size[0] - buffer_size and the_size[1] < self.size[1] - buffer_size:
            font_size += 1
            self.font = pygame.font.Font('freesansbold.ttf', font_size)
            the_size = self.font.size(self.text)
            # text = self.font.render(self.text, True, self.text_color) 
            # the_size = text.get_rect()
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
        
        if self.element_type != "Label":
        
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
                        self.display.blit(text_outline, textRect_outline)
        
        textRect.center = text_center
        self.display.blit(text, textRect)
        

    def click_check(self, position: tuple[int, int], down_click: bool) -> bool:

        print("haha")

        # if the click was not a down click
        # or
        # if the element is not a button or a text box
        # the click is not valid
        if not down_click or self.element_type not in ["Button", "Text Box"]:
            self.pressed = False
            return False

        # if the element is not currently being drawn

        # print(current_container)
        print(self.parent_container.being_drawn)
        if self.parent_container.being_drawn == False:
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
            if self.name != "Sound Input":
                global currently_typing
                currently_typing = self
            return True


        elif self.element_type == "Button":
            self.pressed = True
            return True




# effectively a different "screen",
# holds different elements and can be
# switched between by pressing certain
# buttons
class Container:
    
    def __init__(self, display: pygame.Surface) -> None:
        self.elements: dict[Element, Callable] = {}
        self.display = display
        self.being_drawn = False
    
    @property
    def being_drawn(self) -> bool:
        return self._being_drawn

    @being_drawn.setter
    def being_drawn(self, value: bool) -> None:
        self._being_drawn = value
    
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
                print("iuahbfuiawbf")
                func()
                element.click_check(position, down_click)



# if a text box element is selected,
# this variable will hold the element
# that is currently selected
currently_typing: Element = None