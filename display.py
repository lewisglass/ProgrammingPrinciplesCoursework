from datetime import datetime

class Display:
    
    console_length: int = 79

    @staticmethod    
    def add_line(console_string, alignment = 'l'):
        border = "|"
        if alignment == 'l':
            print (f"{border}{console_string.ljust(Display.console_length)}{border}")
        elif alignment == 'r':
            print (f"{border}{console_string.rjust(Display.console_length)}{border}")
        elif alignment == 'c':
            print (f"{border}{console_string.center(Display.console_length)}{border}")

    @staticmethod 
    def add_dividing_line():
        line = "_" * Display.console_length
        Display.add_line(line)

    @staticmethod 
    def display_bridge(bridge_id: str, name: str, location:str, 
                        bridge_type: str, year_built: int ):
        Display.add_line(f"ID: {bridge_id}")
        Display.add_line(f"name: {name}")
        Display.add_line(f"location: {location}")
        Display.add_line(f"type: {bridge_type}")
        Display.add_line(f"year built: {year_built}")
        Display.add_dividing_line()

    @staticmethod
    def display_inspection(name: str, date: datetime, inspector: str, 
                           score: int, defects: str, recommendations: str):
        Display.add_dividing_line()
        Display.add_line(f"Bridge: {name}")
        Display.add_line(f"Date: {date.strftime("%d %B %Y") }")
        Display.add_line(f"Inspector: {inspector}")
        Display.add_line(f"Score: {score}")
        Display.add_line(f"Defects: {defects}")
        Display.add_line(f"Recommendations: {recommendations}")
        Display.add_dividing_line()

    @staticmethod
    def display_menu(menu_name, options):
        Display.add_dividing_line()
        Display.add_line(menu_name, 'c')
        Display.add_dividing_line()
        Display.add_line("")
        Display.add_line("     Select an option:")
        Display.add_line("")
        counter = 1
        for key in options:
            name, _ = options[key]
            Display.add_line(f" {key}. {name}")
            counter += 1
        Display.add_dividing_line()
