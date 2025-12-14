import bridge
import file_handler
import display
import menu
import sys
import input_validation

class BridgeManagementSystem:

    def __init__(self):
        """Contructor for BridgeManagementSystem class"""
        self.bridge_list: list[bridge.Bridge] = []
        self.file_manager: file_handler.FileOperations = file_handler.FileOperations("bridge_data.json")
        self.display_handler = display.Display()

        self.main_menu = menu.Menu("Main Menu", {})
        self.bridges_menu = menu.Menu("Manage Bridges", {})
        self.inspections_menu = menu.Menu("View Inspection History", {})
        self.search_bridges_menu = menu.Menu("Search Bridges", {})
        self.reports_menu = menu.Menu("Reports & Analysis", {})
                                   
        self.main_menu.options = {
            1: ("Manage Bridges", self.setup_menu(self.bridges_menu)),
            2: ("Reports & Analysis", self.setup_menu(self.reports_menu)),
            3: ("Save and Exit", self.exit)
        }
        self.bridges_menu.options = {
            1: ("Add a new bridge", self.add_bridge),
            2: ("View all bridges", self.view_bridges),
            3: ("Search/filter inspections", self.setup_menu(self.inspections_menu)),
            4: ("Search/filter bridges", self.setup_menu(self.search_bridges_menu)),
            5: ("Back to Main Menu", self.setup_menu(self.main_menu))
        }
        self.inspections_menu.options = {
            1: ("View all inspections", self.view_inspections),
            2: ("Record a new inspection", self.record_inspection),
            #1: ("Search by bridge name", self.view_inspections),
            #2: ("Search by bridge ID", self.view_inspection_by_id),
            3: ("Back to Manage Bridges", self.setup_menu(self.bridges_menu))
        }
        self.search_bridges_menu.options = {
            #1: ("Search by name", self.search_by_name),
            #2: ("Search by location", self.search_by_location),
            #3: ("Search by type", self.search_by_type),
            1: ("Back to Manage Bridges", self.setup_menu(self.bridges_menu))
        }
        self.reports_menu.options = {
            #1: ("Generate maintenance priority list", self.generate_priority_list),
            #2: ("Generate summary report", self.generate_summary_report),
            1: ("Back to Main Menu", self.setup_menu(self.main_menu))
        }

        self.current_menu: menu.Menu = None

    def setup_menu(self, new_menu):
        def change_menu():
            self.current_menu = new_menu
        return change_menu
    
    @property
    def file_manager(self):
        """Getter for __file_manager"""
        return self.__file_manager

    @file_manager.setter
    def file_manager(self, file_manager):
        """Setter for __file_manager"""
        if not isinstance(file_manager, 
                          file_handler.FileOperations):
           raise TypeError("Error in file manager initialisation")
        self.__file_manager = file_manager

    @property
    def bridge_list(self):
        """Getter for __bridge_list"""
        return self.__bridge_list

    @bridge_list.setter
    def bridge_list(self, bridge_list):
        """Setter for __bridge_list"""
        if not isinstance(bridge_list, list):
            raise TypeError("Bridge list must be a list")
        if len(bridge_list) == 0:
            self.__bridge_list = bridge_list
        if not all(isinstance(instance, bridge.Bridge) 
                   for instance in bridge_list):
            raise TypeError("Bridge list must only contain bridges")
        self.__bridge_list = bridge_list
        
    @property
    def display_handler(self):
        """Getter for __display"""
        return self.__display_handler
        
    @display_handler.setter
    def display_handler(self, display_handler):
        """Setter for display"""
        if not isinstance(display_handler, display.Display):
           raise TypeError("Error in file manager initialisation")
        self.__display_handler = display_handler

    def import_bridge_list(self):
        """Imports list of bridges from bridge_data.json"""
        try:
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
        except ValueError as error:
            print(f"Error importing Json values: {error}")
        except TypeError as error:
            print(f"Error importing Json values: {error}")

    def check_input(self, validation_func, user_prompt):
        while True:
            try:
                user_value = validation_func(input(user_prompt))
            except ValueError as error:
                print(f"Invalid value: {error}\n try again")
                continue
            except TypeError as error:
                print(f"Invalid type: {error}\n try again")
                continue
            break
        return user_value

    def add_bridge(self):
        """Add a bridge to the list of bridges"""
        inspections: list[bridge.inspection.Inspection] = []
        bridge_id = self.check_input(bridge.Bridge.validate_bridge_id,
                                    "Bridge ID: ")
        name = self.check_input(bridge.Bridge.validate_name,
                                "Bridge name: ")
        location = self.check_input(bridge.Bridge.validate_location,
                                    "Bridge location: ")
        bridge_type = self.check_input(bridge.Bridge.validate_bridge_type,
                                       "Bridge type: ")
        year_built = self.check_input(bridge.Bridge.validate_year_built,
                                      "Bridge year of construction: ")
        try:
            new_bridge = bridge.Bridge(bridge_id,
                                        inspections,
                                        name,
                                        location,
                                        bridge_type,
                                        year_built)
            self.bridge_list.append(new_bridge)
        except ValueError as error:
            raise ValueError from error
        except TypeError as error:
            raise TypeError from error
        choice = input_validation.validate_y_n(input_validation.validate_y_n,
                                    "Would you like to add Inspections? y/n")
        if choice == 'y':
            while True:
                self.input_inspection(new_bridge)
                choice = input_validation.validate_y_n(input_validation.validate_str,
                                          "Would you like to add inspection? y/n")
                if choice == 'y':
                    continue
                else :
                    break
            self.bridge_list.append(new_bridge)

    def record_inspection(self):
        input_bridge_id = self.check_input(bridge.Bridge.validate_bridge_id, 
                                     "Enter the ID of the bridge you wish to record an inspection for")
        for loop_bridge in self.bridge_list:
            if loop_bridge.bridge_id == input_bridge_id:
                selected_bridge = loop_bridge
                break
        self.input_inspection(selected_bridge)
        

    def input_inspection(self, this_bridge: bridge.Bridge):
        date = self.check_input(bridge.inspection.Inspection.validate_date,
                                "Inspection date: ")
        inspector = self.check_input(bridge.inspection.Inspection.validate_inspector,
                                "Inspector: ")
        score = self.check_input(bridge.inspection.Inspection.validate_score,
                                "Inspection score: ")
        defects = self.check_input(bridge.inspection.Inspection.validate_defects,
                                "Defects: ")
        recommendations = self.check_input(bridge.inspection.Inspection.validate_recommendations,
                                "Recommendations: ")
        try:
            this_bridge.add_inspection(date, inspector, score, 
                                       defects, recommendations)
        except ValueError as error:
            raise ValueError from error
        except TypeError as error:
            raise TypeError from error

    def view_bridges(self, local_bridge_list: list[bridge.Bridge] = None):
        if local_bridge_list == None:
            local_bridge_list = self.bridge_list
        for bridge in local_bridge_list:
            self.display_handler.display_bridge(bridge.bridge_id,bridge.name,
                                                bridge.location, bridge.bridge_type,
                                                bridge.year_built)
        input("Press enter to continue...")

    def view_inspections(self, local_bridge_list: list[bridge.Bridge] = None):
        if local_bridge_list == None:
            local_bridge_list = self.bridge_list
        for bridge in local_bridge_list:
            for inspection in bridge.inspections:
                self.display_handler.display_inspection(bridge.name,
                                                        inspection.date,
                                                        inspection.inspector,
                                                        inspection.score,
                                                        inspection.defects,
                                                        inspection.recommendations)
        input("Press enter to continue...")

    def exit(self):
        self.display_handler.add_line("Goodbye!", 'c')
        sys.exit()

    def bridge_search(self):
        filter_types = ()
        search_name = input("Enter name of bridge to search for: ")
        local_bridge_list = [bridge for bridge in self.bridge_list
                              if bridge.name == search_name]
        self.view_bridges(local_bridge_list)

    def start_menu(self):
        max_input = len(self.current_menu.options)
        min_input = 1 #all menus start with 1
        self.display_handler.display_menu(self.current_menu.name, self.current_menu.options)
        while True:
            self.display_handler.add_line(f"Enter a choice (1-{len(self.current_menu.options)}):")
            try:
                choice = input_validation.validate_int(input(), min_input,
                                                        max_input)
                if choice in self.current_menu.options:
                    self.current_menu.option_func(choice)()
                else:
                    print("Invalid, make a new choice: ")
            except ValueError:
                print("Invalid, choice must be an integer, make a new choice")
            self.start_menu()

    def run(self):
        
        try:
            self.import_bridge_list()
            self.setup_menu(self.main_menu)()
            self.start_menu()
            
        except Exception as error:
            print(error)
        

         

