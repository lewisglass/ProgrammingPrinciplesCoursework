import sys

class Display:
    
    def __init__(self, current_state):
        self.curent_state = current_state
        self.console_length = 79
        
    @property
    def current_state(self):
        """Getter for __current_state"""
        return self.current_state
    
    @current_state.setter
    def current_state(self, current_state):
        self.__current_state = current_state

    @property
    def console_length(self):
        """Getter for __console_length"""
        return self.__console_length
    
    @console_length.setter
    def console_length(self, console_length):
        """Setter for __console_length"""
        self.__console_length = console_length
        
    def add_line(self, console_string, left_aligned = False, right_aligned = False):
        border = "|"
        if left_aligned:
            print (f"{border}{console_string.ljust(self.console_length)}{border}")
        elif right_aligned:
            print (f"{border}{console_string.rjust(self.console_length)}{border}")
        else:
            print (f"{border}{console_string.center(self.console_length)}{border}")

    def add_dividing_line(self):
        line = "_" * self.console_length
        self.add_line(line)

    def main_menu_display(self):
        chosen = False
        self.add_dividing_line()
        self.add_line("Main Menu")
        self.add_dividing_line()
        self.add_line("")
        self.add_line("     Select an option:", left_aligned = True)
        self.add_line("")
        self.add_line(" 1. View all bridges", left_aligned = True)
        self.add_line(" 2. Add a bridge", left_aligned = True)
        self.add_line(" 3. Quit", left_aligned = True)
        self.add_dividing_line()
        
    def bridge_menu_display(self):
        self.add_dividing_line()
        self.add_line("Bridge Menu")
        self.add_dividing_line()
        self.add_line("")
        self.add_line("     Select an option:", left_aligned = True)
        self.add_line("")
        self.add_line(" 1. Add a bridge", left_aligned = True)
        self.add_line(" 2. Add an Inspection", left_aligned = True)
        self.add_line(" 2. Main Menu", left_aligned = True)
        self.add_dividing_line()
        