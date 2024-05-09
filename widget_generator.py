"""This script can generate widgets and save it to json files"""
import os
import json
import warnings
import cv2
import numpy as np
from typing import *

class Generator:
    """
    # Help you quikly generate a widgets

    This class will read a picture file and change it to CMDchars.
    
    A widget is a rectangle string. 
    When you add a widget to the root, t
    he scripts will automatically convert 
    the rectangle string to a list that contains each 
    line of the string. 
    It will insert each line to the root according to 
    the position properties that you have set previously.

    When you use this class to generate widgets, please read the
    parameters description carefully.

    Before you save the widget as json, you need to make sure
    that the size and the appearance of the widget should be proper.
    You can use method `cmdshow` to see the appearance and size.
    """

    def __init__(self, file: str | None=None, widget_name: str | None=None, *base: None | str, newbase:None | str=None, mapchar: str="mqpka89045321@#$%^&*()_=||||} "[::-1]) -> None:
        """
        - file: 
            In where your picture saved.

        - widget_name:
            The name of your widget.

        - base: 
            After you see your CMDwidgets, 
            you have to set this properties to 
            claim which char is your widgets background.
            For example, if your pictures background is composed by 'm', 
            then you should set base to 'm'. All of it will be replace by newbase.

        - newbase:
            Script will replace all of base char to newbase char. 
            For example, if you would like to change the background 
            char from 'm' to ' ', you should set this value to ' '.
        
        - mapchar:
            The script will convert you widget picture to string according to this string.
            The chars of this string should ordered from easy to complecated. 
            It maps the brightness of pixels onto chars. 
            Default is `"mqpka89045321@#$%^&*()_=||||} "[::-1]`
        
        Warnings:
            You have to make sure, the picture's back ground should not be complecated. 
            Otherwise the script will replace the char in your main widget.
        
        If you want to see the brief description of this class, try not to call the class
        (do not input brackets after the class name) 
        and suspend your pointer on the class name.
        """
        self.__origin_im = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        self.__im = self.__origin_im
        self.__base = base
        self.__newbase = newbase
        self.__mapchar = mapchar
        self.__widget_name = widget_name
        self.__string = None
        self.__string_list = None
        self.resize(fx=58/80, fy=33/92, dsize=None)  # This will rescale the picture to make is show properly in CMD.

    @property
    def widget_name(self):
        return self.__widget_name
    
    @widget_name.setter
    def widget_name(self, value):
        if isinstance(value, str)\
            and not '-' in value:
                self.__widget_name = value
        else:
            raise Exception("The name should not contains '-'.")

    @property
    def base(self):
        return self.__base
    
    @base.setter
    def base(self, value):
        flag = False
        if all([isinstance(char, str) for char in value]):
            if all([len(char)==1 for char in value]):
                flag = True
        if not flag:
            # If one of the value in base is not a single char
            raise TypeError("Values in base should all be a single char.")
        self.__base = value
        self.update()

    @property
    def newbase(self):
        return self.__newbase
    
    @newbase.setter
    def newbase(self, value):
        flag = False
        if isinstance(value, str):
            if len(value) == 1:
                flag = True
        if not flag:
            raise TypeError("Value of newbase should be a single char.")
        self.__newbase = value
        self.update()

    @property
    def mapchar(self):
        return self.__mapchar
    
    @mapchar.setter
    def mapchar(self, value):
        if not isinstance(value, str):
            raise TypeError("Mapchar should be a string.")
        self.__mapchar = value
        self.update()

    @property
    def string(self):
        return self.__string
    
    @property
    def string_list(self):
        return self.__string_list

    def resize(self, fx: float | None=None,fy: float | None=None, dsize=None) -> Self:
        """        
        This function can resize the widget. 
        To make the widget shown in a proper size and scale in CMD.

        - fx:
            Horizontal scaling ratio, default is None
        
        - fy:
            Vertical scaling ratio, default is None
        
        fx=58/80, fy=33/92, dsize=None
        """
        self.__im = cv2.resize(self.__im, dsize=dsize, fx=fx, fy=fy)
        self.update()
        return self

    def update(self):
        if not ((self.__base is None) or (self.__newbase is None)):
            # if both of base and newbase value are set
            mapchar = self.__mapchar
            for char in self.__base:
                mapchar = mapchar.replace(char, self.__newbase)  # Replace all of base char to newbase
        else:
            # if one of it have not set
            mapchar = self.__mapchar

        mapchar_lenth = len(mapchar)
        mapchar = np.array([ord(i) for i in mapchar], dtype=np.uint8)
        mapper = (self.__im / 255 * (mapchar_lenth-1)).astype(np.int_)
        mapped = mapchar[mapper]  # Map the brightness to chars
        enter_col = np.ones((mapped.shape[0], 1), dtype=np.uint8) * ord('\n')
        mapped = np.concatenate((mapped, enter_col), axis=1)
        self.__string = mapped.tobytes().decode("utf-8")
        self.__string_list = self.__string.split("\n")
    
    def cmdshow(self) -> Self:
        """
        This method will show your widget in cmd or powershell. 
        Please make sure you the widget can show properly before you save it to json.
        """
        print(self.__string, end="")
        return self
    
    def replace(self, *base, newbase) -> Self:
        """A method that can help you quikly set base and newbase."""
        self.base = base
        self.newbase = newbase
        return self
    
    def save(self, path: str | None=None, widget_name: str | None=None) -> Self:
        """
        This method can help you to save your widget into a json file.

        - path:
            The path to widgets.json file. Default is None, which means
            it will find json file in the current directory. It is not recommend
            to set it with default because the python interpreter might set this path
            depend on the directory of this script file.
            It should be a direcory but not a file path.
            For example: E://project/res/
        
        - widget_name:
            The name of the widget. If the value of widget_name is None,
            it will use the value that you have set previously. If both 
            of it have not been set, then it will raise an exception.
        """
        if widget_name is not None:
            self.widget_name = widget_name
        if self.__widget_name is None:
            raise Exception("You have not set the value of widget_name.")
        if path is None:
            path = "./"

        full_path = os.path.join(path, "widgets.json")
        flag = os.path.exists(full_path)
        if not flag:
            warnings.warn("File not found, widgets.json will be created.")
            with open(full_path, 'w', encoding="utf-8") as file:
                json.dump({}, file)
        with open(full_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
            data[self.__widget_name] = self.__string_list
        with open(full_path, 'w', encoding="utf-8") as file:
            json.dump(data, file)
        return self
    
    def __str__(self) -> str:
        return self.__string

class Editor:
    """
    # Quikly edit your widgets appearance
    By using this file, you can quikly edit your widgets appearance.
    It will show your widgets in CMD or powershell to where allows you to 
    edit your widgets appearance char by char. And of course, this class 
    provide you with a couple of method to help you edit your widgets. 
    """
    def __init__(self, file_path: str | None=None) -> None:
        """
        - fp:
            You must set this value to let the scripts find the widgets.json
            It should be a diractory rather a file. For example `example/path/to/your/file/`
        
        If you called `cmdeditor`, you can still call other method but this is not recommand.
        """
        self.__file_path_is_set = False
        self.__file_path = None
        self.__is_use_editor = None
        self.file_path = file_path
        with open(self.__file_path, 'r', encoding="utf-8") as file:
            self.__widgets: Dict[str, List] = json.load(file)

    @property
    def file_path(self):
        return self.__file_path
    
    @file_path.setter
    def file_path(self, value):
        if self.__file_path_is_set:
            raise Exception("The file_path should be only set once.")
        if self.__file_path is None:
            if value is None:
                value = "./"
            self.__file_path = os.path.join(value, "widgets.json")
            flag = os.path.exists(self.__file_path)
            if not flag:
                raise Exception("The widgets.json file has not found.")
        else:
            raise Exception("You have to set the value of file_path.")
        self.__file_path_is_set = True
    
    @property
    def widgets(self):
        return self.__widgets
    
    @property
    def widgets_list(self):
        return list(self.__widgets.keys())
        
    def __confirm(self):
        """Will be called while user needs to confirm."""
        while True:
            print("Input Y/n to continue: ", end="")
            char = input()
            if char == 'Y':
                flag = True
                break
            elif char == 'y':
                flag = True
                break
            elif char == 'N':
                flag = False
                break
            elif char == 'n':
                flag = False
                break
            else: pass
        return flag
    
    def save(self) -> Self:
        with open(self.__file_path, 'w', encoding="utf-8") as file:
            json.dump(self.__widgets, file)
        return self
    
    def delete(self, *widgets_name) -> Self:
        """You can only use this method to delete widgets"""
        flag_list = []
        for names in widgets_name:
            flag_list.append(names in self.__widgets.keys())
        if not all(flag_list):
            raise Exception("The widgets you want to delete does not exist.")
        for names in widgets_name:
            self.__widgets.pop(names)
        return self
    
    def __cmdshow(self, name):
        widget = self.__widgets[name]
        widget = "\n".join(widget)
        print(widget, end='',flush=True)
    def cmdshow(self):
        for name in self.__widgets.keys():
            self.__cmdshow(name)
            print()
        return self
    
    def get_info(self, name) -> Dict[Literal["name", "size", "shape", "is_proper"], Union[Tuple, bool, str]]:
        """
        Get the information of a widget.
        is_proper: Only True when the widget's width is equal to lenth.
        """
        widget = self.__widgets[name]
        name = name
        shape = (len(widget[0]), len(widget))
        size = len(widget[0]) * len(widget)
        is_proper = None
        proper_list = []
        for i in range(shape[1]):
            proper_list.append(widget[i] == shape[0])
        is_proper = all(proper_list)
        return {
            "name": name,
            "size": size,
            "shape": shape,
            "is_proper": is_proper
        }
    
    def scale(fx=None, fy=None) -> Self:
        """Scale your widget"""
        ...

    def __commands_parse(self, commands: str):
        """This help to parse the commands"""
        commands = commands.strip()
        key = commands.split('-')[0].strip()
        options = [i.strip() for i in commands.split('-')][1:]
        # options example: [], ['arg0 arg1 arg2', 'arg']
        return key, options
    def cmdeditor(self, use_editor: bool=True, commands: str | None="help"):
        """
# CMDEditor
## Recommanded!

    It is highly recommanded to only use this method to enter edit mode and
    edit your widgets. It offers you several commands, the words in '<>' are
    arguments, you shdould remember to replace it with your own arguments.
    Those arguments are all position parametors. You can input any number of 
    value if there is a '*' before the parametors.
    ---

    See the info of commands below:
    - help: This will show you the commands.
    - del -<*name>: This will delete the widgets.
    - show -<name>: This will show the widget.
    - edit -<name>: 
        This allows you to enter edit mode, which can edit widget 
        char by char.
    - replace -<*char> -<char> -<name>: 
        This will replace all of chars in the first parametors
        to the char in the second parametors.
    - eval -<code>: 
        This can execute any single-line python code.
        Usually, you can use it to print some information such as shape or something.
        When using this commands, make sure you know how this script work.
        This commands is not recommand because it might cause some unknown issues.
    - save: 
        Dump the data to json file. You have to save afer your changes. You don't 
        need to save each time you used command, you only have to save after the last time 
        you use the commands.
    - exit:
        After asking you whether save your widgets, it will exit the program instantly.
        But your script will still continue to execute.
    
#### Warnning: 
If you exit the program without saving it, you will loose all your changes. 
The options should be ordered as the context above.
        """
        self.__is_use_editor = use_editor
        # Map dict
        map_dict = {
            "help": self.__help,
            "del": self.__del,
            "show": self.__show,
            "cls": self.__cls,
            "list": self.__list,
            "info": self.__info,
            "edit": self.__edit,
            "replace": self.__replace,
            "eval": self.__eval,
            "save": self.__save,
            "exit": self.__exit
        }
        print("Welcome to CMDEditor, input help to see available commands!")
        while self.__is_use_editor:
            print("Editor.cmdeditor> ", end='')
            command_input = input()
            key, options = self.__commands_parse(command_input)
            if not key.strip():
                continue
            try:
                map_dict[key](*options)
            except KeyError as e:
                print(f"command not found: {key}")
                print(e)
            except Exception as e:
                print("Values are illegal, please retry.")
                print(e)
        if not self.__is_use_editor:
            key, options = self.__commands_parse(commands)
            map_dict[key](*options)
        return self
    
    "--------"
    def __help(self, *options):
        """unsolved"""
        raise Exception("unsolved")
        print()

    def __del(self, *options):
        name, = options
        name = name.split(' ')
        wids = " ".join(name)
        print(f"You are going to delete those widgets {wids}.\nThis operation cannot be canceled.")
        if self.__confirm():
            self.delete(*name)

    def __show(self, *options):
        name, = options
        self.__cmdshow(name)
        print("All of things above will be clear(cls).")
        if self.__confirm():
            os.system('cls')
    
    def __cls(self, *options):
        os.system("cls")

    def __list(self, *options):
        wids = ' '.join(self.widgets_list)
        print(wids)

    def __info(self, *options):
        name = options
        result = self.get_info(name)
        print(f"""
name: \t{result["name"]}
shape: \t{result['shape']}
size: \t{result['size']}
is_proper: \t{result['is_proper']}
""")

    def __edit(self, *options):
        """Using tkinter to implement"""
        import tkinter as tk
        # Initialize options
        name, = options
        name = name.strip()
        widget = self.__widgets[name]
        widget = '\n'.join(widget)
        # Set monitor
        class Mnt:
            def __init__(self) -> None:
                self.ctrl = None
                self.mouse_wheel = None
                self.replacement = None
                self.font = ["Consolas", 2, "normal"]
            
            def on_key_press(self, event: tk.Event):
                if event.keysym == "Control_L":
                    self.ctrl = True
            def on_key_release(self, event: tk.Event):
                if event.keysym == "Control_L":
                    self.ctrl = False
            def on_mouse_wheel(self, event: tk.Event):
                if self.ctrl:
                    if event.delta > 0:
                        if self.font[1] != 20:
                            self.font[1] += 1
                            print("editor: [log] scaling...")
                    elif event.delta < 0:
                        if self.font[1] != 1:
                            self.font[1] -= 1
                            print("editor: [log] scaling...")
                    cmdshow.config(font=self.font)
            def undo_action(self, event: tk.Event):
                try:
                    cmdshow.edit_undo()
                    print("editor: [log] redo")
                except tk.TclError as e:
                    print(f"editor: [Warning] failed to undo {e}")
                    pass
            def replacement_on_focus_in(self, event: tk.Event):
                replacement.delete(0, tk.END)
            def replacement_on_focus_out(self, event: tk.Event):
                char = replacement.get().strip()
                print("editor: [log] Read the entry.")
                if len(char) == 0:
                    replacement.insert(0, "Enter a single char and press replace.")
                    self.replacement = None
                elif len(char) == 1:
                    self.replacement = char
                elif char == "/SPC":
                    self.replacement = ' '
                elif len(char) > 1:
                    replacement.delete(0, tk.END)
                    replacement.insert(0, "It should be a single char.")
                    self.replacement = None
                else: self.replacement = None
        mnt = Mnt()
        # Callback funtions
        def __save(*args):
            widget = cmdshow.get('1.0', 'end')
            self.__widgets[name] = widget.split('\n')
            print("Editor: [log] Saving file")
            self.save()
        def __redo(*args):
            try:
                cmdshow.edit_redo()
                print("editor: [log] redo")
            except tk.TclError as e:
                print(f"editor: [Warning] redo failed {e}")
                pass
        def __replace(*args):
            # Get selected index
            try:
                first = cmdshow.index('sel.first')
                last = cmdshow.index('sel.last')
                print("editor: [log] Got selected index")
            except tk.TclError:
                first, last = None, None
                print("editor: [Warning] Get index failed")
            if bool(first) and bool(last):
                print("editor: [log] parsing index")
                line0, index0 = [int(i) for i in first.split('.')]
                line1, index1 = [int(i) for i in last.split('.')]
            else:
                line0, line1, index0, index1 = False, False, False, False
            # Calculate the chars
            line_char = self.get_info(name)["shape"][0]
            if line0 and line1:
                if line0 == line1:
                    replacement = mnt.replacement * (index1 - index0)
                    cmdshow.replace(first, last, replacement)
                # first line
                elif line1 > line0:
                    # first line
                    a = first
                    b = '.'.join([f"{line0}", f"{line_char}"])
                    replacement = mnt.replacement * (line_char-index0)
                    cmdshow.replace(a, b, replacement)
                    # last line
                    a = '.'.join([f"{line1}", f"0"])
                    b = '.'.join([f"{line1}", f"{index1}"])
                    replacement = mnt.replacement * index1
                    cmdshow.replace(a, b, replacement)
                    # middle line
                    for i in range(line0+1, line1):
                        a = '.'.join([f"{i}", f"0"])
                        b = '.'.join([f"{i}", f"{line_char}"])
                        replacement = mnt.replacement * (line_char)
                        cmdshow.replace(a, b, replacement)
                else: print("editor: [error] Failed when replacing the string with unkown reason"); pass
                print("editor: [log] Replaced")
            else: pass            

        # Set root
        root = tk.Tk()
        root.title("Editor") 
        root.minsize(width=800, height=600)
        root.bind('<KeyPress>', mnt.on_key_press)
        root.bind('<KeyRelease>', mnt.on_key_release)
        root.bind('<MouseWheel>', mnt.on_mouse_wheel)
        root.bind('<Control-z>', mnt.undo_action)
        root.bind('<Control-s>', __save)
        # Set Buttons]
        redo = tk.Button(root)
        redo.config(background="white", foreground="black", text="redo", command=__redo)
        redo.grid(row=0, column=0, sticky="nsew")
        save = tk.Button(root)
        save.config(background="white", foreground="black", text="save", command=__save)
        save.grid(row=0, column=1, sticky="nsew")
        replace = tk.Button(root)
        replace.config(background="white", foreground="black", text="replace", command=__replace)
        replace.grid(row=0, column=2, sticky="nsew")
        replacement = tk.Entry(root)
        replacement.insert(0, "Enter a single char and press replace.")
        replacement.grid(row=0, column=3, sticky="nsew")
        replacement.bind("<FocusIn>", mnt.replacement_on_focus_in)
        replacement.bind("<FocusOut>", mnt.replacement_on_focus_out)
        # Set Text
        cmdshow = tk.Text(root)
        cmdshow.insert(tk.END, widget)
        cmdshow.config(foreground="white", font=mnt.font, background="black", undo=True)
        cmdshow.grid(row=1, column=0, columnspan=4, sticky="nsew")
        # Start the mainloop
        root.columnconfigure(0, weight=2)
        root.columnconfigure(1, weight=2)
        root.columnconfigure(2, weight=2)
        root.columnconfigure(3, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=100)
        print("Editor starting in a new window...")
        root.mainloop()
        print("Editor has been closed.")
    
    def __replace(self, *options):
        name, chars, newchar = options
        chars = chars.split(' ')
        for i, char in enumerate(chars):
            if char == "/SPC":
                chars[i] = ' '
        if newchar == "/SPC":
            newchar = ' '
        widget = "\n".join(self.widgets[name])
        print("This will replace all of chars to new char.")
        if self.__confirm():
            for char in chars:
                widget = widget.replace(char, newchar)
        self.__widgets[name] = widget.split('\n')
     
    def __eval(self, *options):
        code, = options
        eval(code)

    def __save(self, *options):
        print("After you saved, the data will dump to json file.")
        if self.__confirm():
            self.save()

    def __exit(self, *options):
        print("This will exit the editor, would you like to save your widgets?")
        if self.__confirm():
            self.save()
        self.__is_use_editor = False
    "--------"
    


if __name__ == "__main__":
    # time module is only for demonstration.
    import time

    """
    This is an example about how to create widgets and save it to json file.
    And it will show you how to use editor to edit your widgets.
    This example does not show every method and function, it just used as a demonstration.
    Please run the code below in the cmd or powershell to display the widget properly.
    """
    # Add a rectangle widget.
    # This rectangle is black, so it won't show on the black background.
    rectangle = Generator("widget_rectangle.png", "rectangle").resize(0.5, 0.5).cmdshow()
    time.sleep(5)

    # We replace it's ' ' to 'm' to make it brighter.
    rectangle.replace(' ', newbase="m").cmdshow()
    time.sleep(5)

    # Then we figure out that the rectangle can be showed properly, 
    # we can save it to the json file by calling save method.
    rectangle.save()
    os.system("cls")


    # Now we can try to add another widget. Its a circle.
    circle = Generator("widget_circle.png", "circle").resize(0.5, 0.5).cmdshow()
    time.sleep(5)
    # Oops, it seems that the circle cannot shows properly, we want a bright circle, but it
    # seems like it appears like a black circle with white border.
    # Now let's change the border to black and change the inner circle to white.
    # First we replace all of 'm' to 'A', and save.
    circle.replace('m', newbase='A').cmdshow().save()
    time.sleep(5)
    
    # Then we use Editor to open json file, and enter this command to replace ' ' to 'm'.
    # You are using cmdeditor which use commands to edit your widgets. You might have to 
    # comfirm changes by inputing 'Y'.
    editor = Editor() 
    editor.cmdeditor(False, "replace -circle -/SPC -m").cmdeditor(False, "replace -circle -A -/SPC")
    editor.cmdshow()
    time.sleep(5)

    # It looks good... right?
    # now let's save it to json file
    editor.save()

    # Of couse if you want to edit your widget char by char, we still offer you a method.
    editor.cmdeditor(False, "edit -circle").cmdeditor(False, "exit").save()

    # Enjoy!



