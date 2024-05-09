"""This script can monitor user keyboard input"""
import msvcrt as mt
import time
from threading import Thread


"""
Here is a simple program to indicate how to use msvcrt to monitor user keyboard.

while True:
    a = mt.getch().decode("utf-8")
    print(a, end="", flush=True)

Run this program, you will be able to input chars in console.
"""

class Keyboard:
    """
    This class will set another thread to run this script
    to ensure user keyboard will be constantly monitored in the
    background. Actually, this is a subprocess of your main programm.
    So you have to make sure that you have started it properly before your
    main process by calling start_monitor method. 

    """

    def __init__(self) -> None:
        """
        # Example Code
        This is a little script that shows you how to use this class, and how to take actions
        when user press a button on the key board. You can monitor the change of pressing time
        to know if the user have pressed a button. 
        
        ```python
        keyboard.start_monitor()
        input_time = keyboard.trigger_time
        count = 0
        while keyboard.KEY != 'q': 
            if input_time != keyboard.trigger_time:
                count += 1
                print(f"{keyboard.KEY} {keyboard.trigger_time:.2f}", end=", ", flush=True)
                if count % 3 == 0:
                    print()
                input_time = keyboard.trigger_time
        ```
        """
        self.__KEY = None
        self.__trigger_time = None

    @property
    def KEY(self):
        return self.__KEY
    
    @KEY.setter
    def KEY(self, value):
        """If necessary, you can change KEY to fit your functions"""
        if isinstance(value, str):
            self.__KEY = value
        else:
            raise TypeError("The value of KEY should be a str.")

    @property
    def trigger_time(self):
        return self.__trigger_time

    def monitor(self) -> None:
        while True:
            if mt.kbhit():
                self.__KEY = mt.getch().decode("utf-8")
                self.__trigger_time = time.time()
        
    def start_monitor(self) -> None:
        thread = Thread(target=self.monitor, name="keyboard_monitor", daemon=True)
        thread.start()


keyboard = Keyboard()

if __name__ == "__main__":

    """
    This is a little script that shows you how to use this class, and how to take actions
    when user press a button on the key board. You can monitor the change of pressing time
    to know if the user have pressed a button. 
    """
    keyboard.start_monitor()
    input_time = keyboard.trigger_time
    count = 0
    while keyboard.KEY != 'q': 
        if input_time != keyboard.trigger_time:
            count += 1
            print(f"{keyboard.KEY} {keyboard.trigger_time:.2f}", end=", ", flush=True)
            if count % 3 == 0:
                print()
            input_time = keyboard.trigger_time
    
