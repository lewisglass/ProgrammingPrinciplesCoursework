import bridge
import file_handler
import display
import menu
import sys
import input_validation

class BridgeManagementSystem:

    def __init__(self):
        """Contructor for BridgeManagementSystem class"""
        self.bridge_list = []
        self.file_manager = file_handler.FileOperations("bridge_data.json")
        self.display_handler = display.Display()

        self.main_menu = menu.Menu("Main Menu", {
            1: ("Manage Bridges", self.setup_menu(self.bridges_menu)),
            2: ("Reports & Analysis", self.setup_menu(self.reports_menu)),
            3: ("Save and Exit", self.exit)
        })
        self.bridges_menu = menu.Menu("Manage Bridges", {
            1: ("Add a new bridge", self.add_bridge),
            2: ("Record a new inspection", self.add_inspection),
            3: ("View all bridges", self.view_all_bridges),
            4: ("View inspections menu", self.setup_menu(self.inspections_menu)),
            5: ("Search/filter bridges", self.setup_menu(self.search_bridges_menu)),
            6: ("Back to Main Menu", self.setup_menu(self.main_menu))
        })
        self.inspections_menu = menu.Menu("View Inspection History", {
            #1: ("Search by bridge name", self.view_inspection_by_name),
            #2: ("Search by bridge ID", self.view_inspection_by_id),
            3: ("Back to Manage Bridges", self.setup_menu(self.bridges_menu))
        })
        self.search_bridges_menu = menu.Menu("Search Bridges", {
            #1: ("Search by name", self.search_by_name),
            #2: ("Search by location", self.search_by_location),
            #3: ("Search by type", self.search_by_type),
            4: ("Back to Manage Bridges", self.setup_menu(self.bridges_menu))
        })
        self.reports_menu = menu.Menu("Reports & Analysis", {
            #1: ("Generate maintenance priority list", self.generate_priority_list),
            #2: ("Generate summary report", self.generate_summary_report),
            3: ("Back to Main Menu", self.setup_menu(self.main_menu))
        })

        self.current_menu = None
    
    bride_ids = {}

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

    def check_input(self, validation_func, user_prompt, 
                    y_n_prompt = False, max_size = 1):
        while True:
            try:
                if not y_n_prompt:
                    user_value = validation_func(input(user_prompt))
                else:
                    user_value = validation_func(input(user_prompt), max_size)
            except ValueError as error:
                print(f"Invalid value: {error}\n try again")
                continue
            except TypeError as error:
                print(f"Invalid type: {error}\n try again")
                continue
            break

    def add_bridge(self):
        """Add a bridge to the list of bridges"""
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
        temp_inspections = []
        choice = self.check_input(input_validation.validate_str,
                                    "Would you like to add Inspections? y/n",
                                    True)
        if choice == 'y':
            while True:
                temp_inspections.inspections.append(self.add_inspection())
                choice = self.check_input(input_validation.validate_str,
                                          "Would you like to add Inspections? y/n",
                                          True)
                if choice == 'y':
                    continue
                else :
                    break
            try:
                new_bridge = bridge.Bridge(bridge_id,
                                            temp_inspections,
                                            name,
                                            location,
                                            bridge_type,
                                            year_built)
                self.bridge_list.append(new_bridge)
            except ValueError as error:
                print(f"Invalid value: {error}\n try again")
            except TypeError as error:
                print(f"Invalid type: {error}\n try again")


    def add_inspection(self):
        while True:
            try:  
                temp_date = bridge.inspection.Inspection.validate_date(
                                input("Inspection date (yyyy-mm-dd): "))
                temp_inspector = bridge.inspection.Inspection.validate_inspector(
                                input("Inspector name: "), 1, 70)
                temp_score = bridge.inspection.Inspection.validate_score(
                                input("Inspection score: "))
                temp_defects = bridge.inspection.Inspection.validate_defects(
                                input("Inspection defects: "))
                temp_recommendations = bridge.inspection.Inspection.validate_recommendations(
                                input("Inspection recommendations: "))
                new_inspection = bridge.inspection.Inspection(temp_date,
                                                            temp_inspector,
                                                            temp_score,
                                                            temp_defects,
                                                            temp_recommendations)
            except ValueError as error:
                print(error)
            except TypeError as error:
                print(error)
            return new_inspection

    def view_all_bridges(self, local_bridge_list : list[bridge.Bridge] = None ):
        if local_bridge_list == None:
            local_bridge_list = self.bridge_list
        for bridge in local_bridge_list:
            self.display_handler.display_bridge(bridge.bridge_id,bridge.name,
                                                bridge.location, bridge.bridge_type,
                                                bridge.year_built)
        input("Press enter to continue...")
        self.start_menu()

    def exit(self):
        print("Goodbye!")
        sys.exit()

    def bridge_search(self):
        search_name = input("Enter name of bridge to search for: ")
        local_bridge_list = [bridge for bridge in self.bridge_list
                              if bridge.name == search_name]
        self.print_bridges(local_bridge_list)

    def setup_menu(self, new_menu):
        def change_menu():
            self.current_menu = new_menu
        return change_menu

    def setup_bridges_menu(self):
        self.current_menu = self.bridges_menu
        self.start_menu()

    def setup_reports_menu(self):
        self.current_menu = self.reports_menu
        self.start_menu()

    def setup_search_inspections_menu(self):
        self.current_menu = self.search_inspections_menu
        self.start_menu()

    def setup_search_bridges_menu(self):
        self.current_menu = self.search_bridges_menu
        self.start_menu()

    def setup_main_menu(self):
        self.current_menu = self.main_menu
        self.start_menu()

    def start_menu(self):

        self.display_handler.display_menu(self.current_menu.name, self.current_menu.options)
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
                self.start_menu()

    def run(self):
        
        try:
            self.import_bridge_list()
            self.setup_main_menu()
            
        except Exception as error:
            print(error)
        

         

