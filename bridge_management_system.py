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
        self.reports_menu = menu.Menu("Reports & Analysis", {})
                                   
        self.main_menu.options = {
            1: ("Manage Bridges", self.setup_menu(self.bridges_menu)),
            2: ("Reports & Analysis", self.setup_menu(self.reports_menu)),
            3: ("Save and Exit", self.exit)
        }
        self.bridges_menu.options = {
            1: ("Add a new bridge", self.add_bridge),
            2: ("View all bridges", self.view_bridges),
            3: ("Search/filter bridges", self.filter_bridges),
            4: ("Manage Inspections", self.setup_menu(self.inspections_menu)),
            5: ("Back to Main Menu", self.setup_menu(self.main_menu))
        }
        self.inspections_menu.options = {
            1: ("View all inspections", self.view_all_inspections),
            2: ("Record a new inspection", self.record_inspection),
            3: ("Search/filter inspections", self.filter_inspections),
            4: ("Back to Manage Bridges", self.setup_menu(self.bridges_menu))
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

    def add_bridge(self):
        """Add a bridge to the list of bridges"""
        inspections: list[bridge.inspection.Inspection] = []
        bridge_id = input_validation.check_input(bridge.Bridge.validate_bridge_id,
                                    "Bridge ID: ")
        name = input_validation.check_input(bridge.Bridge.validate_name,
                                "Bridge name: ")
        location = input_validation.check_input(bridge.Bridge.validate_location,
                                    "Bridge location: ")
        bridge_type = input_validation.check_input(bridge.Bridge.validate_bridge_type,
                                       "Bridge type: ")
        year_built = input_validation.check_input(bridge.Bridge.validate_year_built,
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
        choice = input_validation.check_input(input_validation.validate_y_n,
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
        input_bridge_id = input_validation.check_input(bridge.Bridge.validate_bridge_id, 
                                     "Enter the ID of the bridge you wish to record an inspection for")
        for loop_bridge in self.bridge_list:
            if loop_bridge.bridge_id == input_bridge_id:
                selected_bridge = loop_bridge
                break
        self.input_inspection(selected_bridge)
        
    def input_inspection(self, this_bridge: bridge.Bridge):
        date = input_validation.check_input(bridge.inspection.Inspection.validate_date,
                                "Inspection date: ")
        inspector = input_validation.check_input(bridge.inspection.Inspection.validate_inspector,
                                "Inspector: ")
        score = input_validation.check_input(bridge.inspection.Inspection.validate_score,
                                "Inspection score: ")
        defects = input_validation.check_input(bridge.inspection.Inspection.validate_defects,
                                "Defects: ")
        recommendations = input_validation.check_input(bridge.inspection.Inspection.validate_recommendations,
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

    def view_all_inspections(self, local_bridge_list: list[bridge.Bridge] = None):
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
    
    def filter_bridges(self):
        bridge_id_filter = {
            "attribute": "bridge_id",
            "prompt": "Enter Bridge ID to search for: ",
            "func": bridge.Bridge.bridge_id,
            "active": False
        }
        name_filter = {
            "attribute": "name",
            "prompt": "Enter name of bridge to search for: ",
            "active": False
        }
        location_filter = {
            "attribute": "location",
            "prompt": "Enter location of bridge to search for: ",  
            "active": False
        }
        bridge_type_filter = {
            "attribute": "bridge_type",
            "prompt": "Enter type of bridge to search for: ",
            "active": False
        }
        year_built_filter = {
            "attribute": "year_built",
            "prompt": "Enter year built of bridge to search for: ",
            "active": False
        }
        average_score_filter = {
            "attribute": "average_score",
        filter_list = [bridge_id_filter, name_filter,
                       location_filter,
                       bridge_type_filter,
                       year_built_filter]
        filtred_bridge_list: list[bridge.Bridge] = self.bridge_list
        filter_str = "Filters applied: "
        for filter in filter_list:
            printable_attribute = filter["attribute"].replace("_", " ")
            choice =input_validation.check_input(input_validation.validate_y_n,
                                     f"Would you like to filter by {printable_attribute}? y/n")
            if choice == 'y':
                filter['active'] = True
                input_value = input_validation.check_input(input_validation.validate_str,
                                              filter['prompt'])
                filtred_bridge_list = [bridge for bridge in filtred_bridge_list
                                       if input_value.lower().strip() in
                                        str(getattr(bridge, filter["attribute"])).lower().strip()]
                filter_str += f"{printable_attribute} = {input_value}; "
                choice = input_validation.check_input(input_validation.validate_y_n,
                                          "add other filters? y/n")
                if choice == 'y':
                    continue
                else:
                    self.display_handler.add_line(filter_str, 'c')
                    self.view_bridges(filtred_bridge_list)
                    return

    def filter_inspections(self):
        date_filter = {
            "attribute": "date",
            "prompt": "Enter Date to search for: ",
            "active": False
        }
        inspector_filter = {
            "attribute": "inspector",
            "prompt": "Enter name of inspector to search for: ",
            "active": False
        }
        score_filter = {
            "attribute": "score",
            "prompt": "Enter inspection score to search for: ",  
            "active": False
        }
        defects_filter = {
            "attribute": "defects",
            "prompt": "Enter defetcs to search for: ",
            "active": False
        }
        recommendations_filter = {
            "attribute": "year_built",
            "prompt": "Enter recommendations to search for: ",
            "active": False
        }
        filter_list = [date_filter, inspector_filter, score_filter,
                       defects_filter, recommendations_filter]
        filtred_inspection_list: list[bridge.inspection.Inspection] = self.inspections
        filter_str = "Filters applied: "
        for filter in filter_list:
            printable_attribute = filter["attribute"].replace("_", " ")
            choice =input_validation.check_input(input_validation.validate_y_n,
                                     f"Would you like to filter by {printable_attribute}? y/n")
            if choice == 'y':
                filter['active'] = True
                input_value = input_validation.check_input(input_validation.validate_str,
                                              filter['prompt'])
                filtred_inspection_list = [inspection for inspection in filtred_inspection_list
                                       if input_value.lower().strip() in
                                        str(getattr(inspection, filter["attribute"])).lower().strip()]
                filter_str += f"{printable_attribute} = {input_value}; "
                choice = input_validation.check_input(input_validation.validate_y_n,
                                          "add other filters? y/n")
                if choice == 'y':
                    continue
                else:
                    return filtred_inspection_list, filter_str



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
        

         

