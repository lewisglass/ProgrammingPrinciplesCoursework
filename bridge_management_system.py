import bridge
import file_handler
import display
import menu

class BridgeManagementSystem:

    def __init__(self):
        """Contructor for BridgeManagementSystem class"""
        self.bridge_list = []
        self.file_manager = file_handler.FileOperations("bridge_data.json")
        self.display = display.Display()

        self.main_menu = menu.Menu("Main Menu", {
            1: ("Bridge menu", self.setup_bridge_menu),
            2: ("Add bridge", self.add_bridge),
            3: ("Exit", self.exit)
            })
        
        self.bridge_menu = menu.Menu("Bridge Menu", {
            1: ("Add bridge", self.add_bridge),
            2: ("Add inspection", self.add_inspection),
            3: ("Search bridges", self.bridge_search),
            4: ("Main menu", self.setup_main_menu)
            })
        
        self.add_bridge_menu = menu.Menu("Add Bridge Menu", {
            1: ("Add another bridge", self.add_bridge),
            2: ("Main menu", self.setup_main_menu)
            })

        self.current_menu = None

    @property
    def file_manager(self):
        """Getter for __file_manager"""
        return self.__file_manager

    @file_manager.setter
    def file_manager(self, file_manager):
        """Setter for __file_manager"""
        self.__file_manager = file_manager

    @property
    def bridge_list(self):
        """Getter for __bridge_list"""
        return self.__bridge_list

    @bridge_list.setter
    def bridge_list(self, bridge_list):
        """Setter for __bridge_list"""
        self.__bridge_list = bridge_list
        
    @property
    def display(self):
        """Getter for __display"""
        return self.__display
        
    @display.setter
    def display(self, display):
        """Setter for display"""
        self.__display = display

    def import_bridge_list(self):
        """Imports list of bridges from bridge_data.json"""
        from_file = self.file_manager.read_file()
        self.bridge_list = []
        for bridge_json in from_file:
            temp_inspections_list = []

            for inspection_json in bridge_json["inspections"]:
                new_inspection = bridge.inspection.Inspection(
                    date = inspection_json["date"],
                    inspector = inspection_json["inspector"],
                    score = inspection_json["score"],
                    defects = inspection_json["defects"],
                    recommendations = inspection_json["recommendations"])
                temp_inspections_list.append(new_inspection)

            new_bridge = bridge.Bridge(
                bridge_id = bridge_json["id"],
                name = bridge_json["name"],
                location = bridge_json["location"],
                bridge_type = bridge_json["bridge_type"],
                year_built = bridge_json["year_built"],
                inspections = temp_inspections_list)
            self.bridge_list.append(new_bridge)

    def add_bridge(self):
        """Add a bridge to the list of bridges"""
        while True:
            try:
                new_bridge = bridge.Bridge()
                new_bridge.bridge_id = input("Bridge ID: ")
                new_bridge.name = input("Bridge name: ")
                new_bridge.location = input("Bridge location: ")
                new_bridge.bridge_type = input("Bridge type: ")
                new_bridge.year_built = input("Bridge year of construction: ")
                new_bridge.inspections = []
                choice = input("Would you like to add Inspections? y/n")
                if choice == 'y':
                    while True:
                        new_bridge.inspections.append(new_inspection)
                        choice = input("Would you like to add another Inspection? y/n")
                        if choice == 'y':
                            continue
                        elif choice == 'n':
                            break
                        else:
                            raise ValueError
                elif choice != 'n':
                    raise ValueError
                self.bridge_list.append(new_bridge)
                break   
            except ValueError as e:
                print(f"Invalid value: {e}")
                del new_bridge

    def add_inspection(self):
        try:  
            new_inspection = bridge.inspection.Inspection()
            new_inspection.date = input("Inspection date (yyyy-mm-dd): ")
            new_inspection.inspector = input("Inspector name: ")
            new_inspection.score = input("Inspection score: ")
            new_inspection.defects = input("Inspection defects: ")
            new_inspection.recommendations = input("Inspection recommendations: ")
        except ValueError as e:
            print(e)
        return new_inspection

    def print_bridges(self, local_bridge_list):
        for i in local_bridge_list:
            print(f"Bridge ID    :  {i.bridge_id}")
            print(f"Name         :  {i.name}")
            print(f"Location     :  {i.location}")
            print(f"Type         :  {i.bridge_type}")
            print(f"Year built   :  {i.year_built}")
            print(f"Average score:  {i.average_score}")
            print("Inspections ")
            if i.inspections:
                for j in i.inspections:
                    print(f"Date           :  {j.date}")
                    print(f"Inspector      :  {j.inspector}")
                    print(f"Score          :  {j.score}")
                    print(f"Recommendations:  {j.recommendations}")
                    print(f"Defects        :  {j.defects}")
            else:
                print("None")
            print("------------------------------")
        input("Press enter to continue...")

    def exit(self):
        print("Goodbye!")
        quit()

    def bridge_search(self):
        search_name = input("Enter name of bridge to search for: ")
        local_bridge_list = [bridge for bridge in self.bridge_list
                              if bridge.name == search_name]
        self.print_bridges(local_bridge_list)

    def setup_add_bridge_menu(self):
        self.current_menu = self.add_bridge_menu
        self.start_menu()

    def setup_main_menu(self):
        self.current_menu = self.main_menu
        self.start_menu()
    
    def setup_bridge_menu(self):
        self.current_menu = self.bridge_menu
        self.print_bridges(self.bridge_list)
        self.start_menu()

    def start_menu(self):

        self.display.display_menu(self.current_menu.name, self.current_menu.options)
        while True:
            print(f"Enter a choice (1-{len(self.current_menu.options)}):")
            try:
                choice = int(input().strip())
                if choice in self.current_menu.options:
                    self.current_menu.option_func(choice)()
                else:
                    print("Invalid, make a new choice: ")
            except ValueError:
                print("Invalid, choice must be an integer, make a new choice")

    def run(self):
        
        try:
            self.import_bridge_list()
            self.setup_main_menu()
            
        except ValueError as error:
            print(error)
        
        except Exception as error:
            print(error)
        

         

