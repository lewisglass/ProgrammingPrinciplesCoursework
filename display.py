import sys

class Display:
    
    def __init__(self):
        self.console_length = 79

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

    def display_menu(self, menu_name, options):
        self.add_dividing_line()
        self.add_line(menu_name)
        self.add_dividing_line()
        self.add_line("")
        self.add_line("     Select an option:", left_aligned = True)
        self.add_line("")
        counter = 1
        for key in options:
            name, _ = options[key]
            self.add_line(f" {key}. {name}", left_aligned = True)
            counter += 1
        self.add_dividing_line()
