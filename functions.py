from tkinter import filedialog, Tk

# Hide the main Tkinter window
root = Tk()
root.withdraw()

choosing_file = False

def darken_color(input_color: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple([x * 0.5 for x in input_color])


def empty_function():
    pass


def get_file_path(the_element = None, the_holder = None):

    def output_func_1():

        global the_sound_path

        file_path = filedialog.askopenfilename(initialdir=r"C:\Users\Ryan\Desktop\sounds")

        the_sound_path = file_path

    def output_func_2():

        global choosing_file

        choosing_file = True

        file_path = filedialog.askopenfilename(initialdir=r"C:\Users\Ryan\Desktop\sounds")

        choosing_file = False

        the_element.text = beautify_path(file_path)
        the_holder.text = file_path

    if the_element is None:

        return output_func_1

    elif the_element == "222":

        return filedialog.askopenfilename()
        
    else:
        return output_func_2
    

def beautify_path(path):
    while "/" in path:
        path = path[path.index("/")+1:]
    return path