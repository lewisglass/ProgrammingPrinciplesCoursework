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
        
    def add_line(self, console_string, alignment = 'l'):
        border = "|"
        if alignment == 'l':
            print (f"{border}{console_string.ljust(self.console_length)}{border}")
        elif alignment == 'r':
            print (f"{border}{console_string.rjust(self.console_length)}{border}")
        elif alignment == 'c':
            print (f"{border}{console_string.center(self.console_length)}{border}")

    def add_dividing_line(self):
        line = "_" * self.console_length
        self.add_line(line)

    def display_bridge(self, bridge_id: str, name: str, location:str, 
                        bridge_type: str, year_built: int ):
        self.add_line(f"Bridge ID: {bridge_id}")
        self.add_line(f"Bridge name: {name}")
        self.add_line(f"Bridge location: {location}")
        self.add_line(f"Bridge type: {bridge_type}")
        self.add_line(f"Bridge year built: {year_built}")
        self.add_dividing_line()

    def display_menu(self, menu_name, options):
        self.add_dividing_line()
        self.add_line(menu_name, 'c')
        self.add_dividing_line()
        self.add_line("")
        self.add_line("     Select an option:")
        self.add_line("")
        counter = 1
        for key in options:
            name, _ = options[key]
            self.add_line(f" {key}. {name}")
            counter += 1
        self.add_dividing_line()
