from datetime import datetime

class Display:
    """controls the output display for the user"""
    
    console_length: int = 79

    @staticmethod
    def multi_line(*input_str):
        """Combines strings to display multiline strings together"""
        output_str = ""
        for i in input_str:
            Display.add_line(i)
        
    @staticmethod    
    def add_line(console_string, alignment = 'l'):
        """prints text surounded by a border"""
        border = "|"
        if alignment == 'l':
            print (f"{border}{console_string.ljust(Display.console_length)}{border}")
        elif alignment == 'r':
            print (f"{border}{console_string.rjust(Display.console_length)}{border}")
        elif alignment == 'c':
            print (f"{border}{console_string.center(Display.console_length)}{border}")

    @staticmethod 
    def add_dividing_line():
        """prints a line dividing the page"""
        line = "_" * Display.console_length
        Display.add_line(line)

    @staticmethod 
    def display_bridge(bridge_id: str, name: str, location:str, 
                        bridge_type: str, year_built: int, average_score ):
        """displays the attributes of a bridge in a user friendly format"""
        Display.multi_line(f"ID: {bridge_id}",
                           f"name: {name}",
                           f"location: {location}",
                           f"type: {bridge_type}",
                           f"year built: {year_built}")
        if average_score is not None:
            Display.add_line(f"average score: {average_score}")
        else:
            Display.add_line(f"No inspections recorded")
        Display.add_dividing_line()

    @staticmethod
    def display_inspection(name: str, date: datetime, inspector: str, 
                           score: int, defects: str, recommendations: str):
        """displays the attributes of a inspection in a user friendly format"""
        Display.add_dividing_line()
        Display.multi_line(f"Bridge: {name}",
                            f"Date: {date.strftime('%d %B %Y') }",
                            f"Inspector: {inspector}",
                            f"Score: {score}",
                            f"Defects: {defects}",
                            "Recommendations: {recommendations}")
        Display.add_dividing_line()

    @staticmethod
    def display_menu(menu_name, options):
        """displays the attributes of a menu in a user friendly format"""
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
