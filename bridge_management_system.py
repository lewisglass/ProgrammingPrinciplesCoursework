import bridge
import file_handler
import display
import menu
import sys
import input_validation

class BridgeManagementSystem:
    """Main class controlling high level app logic"""

    def __init__(self, debug = False):
        """Contructor for BridgeManagementSystem class"""
        self.bridge_list: list[bridge.Bridge] = []
        self.file_manager: file_handler.FileOperations = file_handler.FileOperations("bridge_data.json")
        self.display_handler = display.Display()
        self.debug = debug

        self.main_menu = menu.Menu("Main Menu", {})
        self.bridges_menu = menu.Menu("Manage Bridges", {})
        self.inspections_menu = menu.Menu("View Inspection History", {})
        self.reports_menu = menu.Menu("Reports & Analysis", {})
                                   
        self.main_menu.options = {
            1: ("Manage Bridges", self.setup_menu(self.bridges_menu)),
            2: ("Reports & Analysis", self.setup_menu(self.reports_menu)),
            3: ("Save", self.save_changes),
            4: ("Save and Exit", self.exit),
            5: ("Exit without saving", self.hard_exit)
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
            3: ("View inspections for specific bridge", self.view_inspection_prompt),
            4: ("Back to Manage Bridges", self.setup_menu(self.bridges_menu))
        }
        self.reports_menu.options = {
            1: ("Generate maintenance priority list", self.generate_priority_list),
            2: ("Generate summary report", self.summary_report),
            3: ("Back to Main Menu", self.setup_menu(self.main_menu))
        }

        self.current_menu: menu.Menu = None

    def total_bridges(self) -> int:
        """returns total bridges in system"""
        return len(self.bridge_list)

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

    def generate_priority_list(self):
        """generates a priority list based on low scores and lack of recent inspections"""
        priority_list = [brg for brg in self.bridge_list
                         if (due := brg.inspection_due())
                          is not None and due]
        self.display_handler.add_line("Bridges not inspected in over 2 years: ")
        self.view_bridges(priority_list, True)
        priority_list = [brg for brg in self.bridge_list
                         if (score := brg.calculate_average_score())
                          is not None and score < 40]
        self.display_handler.add_line("Bridges with poor score, requiring work: ")
        self.view_bridges(priority_list, True)
        priority_list = [brg for brg in self.bridge_list
                         if brg.inspections == []]
        self.display_handler.add_line("Bridges with no recorded: ")
        self.view_bridges(priority_list, True)

    def summary_report(self):
        """Summarieses the average scores across all briges in the system"""
        self.display_handler.add_line("Not scored", 'c')
        condition_list = [brg for brg in self.bridge_list
                          if brg.calculate_average_score() == None]
        self.view_bridges(condition_list, True)
        self.display_handler.add_line("Excellent 80 - 100", 'c')
        condition_list = [brg for brg in self.bridge_list
                          if (score := brg.calculate_average_score())
                          is not None and score >= 80]
        self.view_bridges(condition_list, True)
        self.display_handler.add_line("Good 60 - 79", 'c')
        condition_list = [brg for brg in self.bridge_list
                          if (score := brg.calculate_average_score())
                          is not None and score >= 60
                          and score < 80]
        self.view_bridges(condition_list, True)
        self.display_handler.add_line("Fair 40 - 59", 'c')
        condition_list = [brg for brg in self.bridge_list
                          if (score := brg.calculate_average_score())
                          is not None and score >= 40
                          and score < 60]
        self.view_bridges(condition_list, True)
        self.display_handler.add_line("Poor 0 - 39", 'c')
        condition_list = [brg for brg in self.bridge_list
                          if (score := brg.calculate_average_score())
                          is not None and score < 40]
        self.view_bridges(condition_list, True)
        
    def import_bridge_list(self):
        """Imports list of bridges from bridge_data.json"""
        try:
            self.file_manager.verify_file()
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
        except FileNotFoundError as error:
            self.display_handler.add_line("File not found, generating default file")
            self.setup_json()
        except PermissionError:
            self.display_handler.add_line("No permission to write/read file")
            self.exit()
        except IsADirectoryError:
            self.display_handler.add_line("Directory found, not file")
            self.exit()

    def setup_json(self):
        """Initialises the JSON information if no file is detected"""
        inspection_template = bridge.inspection.Inspection("2024-03-15",
                                                           "John Smith",
                                                           72,
                                                           "Minor paint deterioration on south tower",
                                                           "Schedule repainting in next 2 years")
        inspection_list = [inspection_template]
        bridge_template = bridge.Bridge("B0001",
                                        inspection_list,
                                        "Forth Bridge",
                                        "Queensferry",
                                        "Cantilever",
                                        1890)
        bridge_list = [bridge_template]
        if not self.debug:
            self.save_changes(bridge_list)

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
                choice = input_validation.check_input(input_validation.validate_y_n,
                                          "Would you like to add another inspection? y/n")
                if choice == 'y':
                    continue
                else :
                    break
            self.bridge_list.append(new_bridge)

    def record_inspection(self):
        """Records an inspection for a specific bridge"""
        input_bridge_id = input_validation.check_input(bridge.Bridge.validate_bridge_id, 
                                     "Enter the ID of the bridge you wish to record an inspection for: ")
        for loop_bridge in self.bridge_list:
            if loop_bridge.bridge_id == input_bridge_id:
                selected_bridge = loop_bridge
                break
        self.input_inspection(selected_bridge)
        
    def input_inspection(self, this_bridge: bridge.Bridge):
        """Allows the user to input data to create an inspection"""
        date = input_validation.check_input(bridge.inspection.Inspection.validate_date,
                                "Inspection date (yyyy-mm-dd): ")
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

    def view_bridges(self, local_bridge_list: list[bridge.Bridge] = None, skip = False):
        """Displays all bridge information in the system"""
        if local_bridge_list == []:
            self.display_handler.add_line("No Bridges found")
        if local_bridge_list == None:
            local_bridge_list = self.bridge_list
        for bridge in local_bridge_list:
            self.display_handler.display_bridge(bridge.bridge_id,bridge.name,
                                                bridge.location, bridge.bridge_type,
                                                bridge.year_built, bridge.calculate_average_score())
        if not skip:
            input("Press enter to continue...")

    def view_all_inspections(self, local_bridge_list: list[bridge.Bridge] = None):
        """Displays all inspection information in the system"""
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

    def view_inspection_prompt(self):
        """Prompts the user to select a bridge to view the inspections of"""
        brg_id = input_validation.check_input(bridge.Bridge.validate_bridge_id,
                                        "Enter bridge ID: ")
        selected_bridge = None
        for brg in self.bridge_list:
            if brg.bridge_id == brg_id:
                selected_bridge = brg
                break
        if selected_bridge == None:
            self.display_handler.add_line("Bridge not found")
            return
        local_list = [selected_bridge]
        self.view_all_inspections(local_list)

    def exit(self):
        self.display_handler.add_line("Goodbye!", 'c')
        sys.exit()

    def hard_exit(self):
        self.display_handler.add_line("Goodbye!", 'c')
        self.debug = True
        sys.exit()
    def filter_bridges(self):
        """User selects values to filter bridges by and then applies those selected"""
        id_str = None
        name_str = None
        location_str = None
        type_str = None
        year_val = None
        year_operator = None

        self.display_handler.add_line("Select all filters you want to apply")
        choice = input_validation.check_input(input_validation.validate_y_n,
                                     "Filter by ID? (y/n)")
        if choice == 'y':
            id_str = input_validation.check_input(input_validation.validate_str,
                                                  "Enter ID filter")
        choice = input_validation.check_input(input_validation.validate_y_n,
                                     "Filter by name? (y/n)")
        if choice == 'y':
            name_str = input_validation.check_input(input_validation.validate_str,
                                                  "Enter name filter")
        choice = input_validation.check_input(input_validation.validate_y_n,
                                     "Filter by location (y/n)?")
        if choice == 'y':
            location_str = input_validation.check_input(input_validation.validate_str,
                                                  "Enter location filter") 
        choice = input_validation.check_input(input_validation.validate_y_n,
                                     "Filter by type? (y/n)")
        if choice == 'y':
            location_str = input_validation.check_input(input_validation.validate_str,
                                                  "Enter type filter")
        choice = input_validation.check_input(input_validation.validate_y_n,
                                     "Filter by year built? (y/n)")
        if choice == 'y':
            year_val = input_validation.check_input(input_validation.validate_str,
                                                  "Enter year built filter")
            while True:
                try:
                    year_operator = input_validation.check_input(input_validation.validate_str,
                                                    "Show values greater than (1), less than (2) or equal (3) to entered value?")
                    if year_operator != '1' and year_operator != '2' and year_operator != '3':
                        raise ValueError
                    else:
                        break
                except ValueError as error:
                    self.display_handler.add_line("Select from above options: 1, 2 or 3")
                    continue
        self.apply_bridge_filters(id_str, name_str, location_str, 
                                  type_str, year_val, year_operator)
            
    def apply_bridge_filters(self, id_str: str = None, name_str: str = None, 
                             location_str: str = None, type_str: str = None, 
                             year_val: int = None, year_operator: str = None):
        """Filters are applied by removing non compliant bridge objects"""
        filtered_list = self.bridge_list
        if id_str is not None:
            search_str = id_str.strip().lower()
            filtered_list = [bridge for bridge in filtered_list
                             if search_str in 
                             bridge.bridge_id.strip().lower()]
        if name_str is not None:
            search_str = name_str.strip().lower()
            filtered_list = [bridge for bridge in filtered_list
                             if search_str in 
                             bridge.name.strip().lower()]
        if location_str is not None:
            search_str = location_str.strip().lower()
            filtered_list = [bridge for bridge in filtered_list
                             if search_str in 
                             bridge.location.strip().lower()]
        if type_str is not None:
            search_str = type_str.strip().lower()
            filtered_list = [bridge for bridge in filtered_list
                             if search_str in 
                             bridge.bridge_type.strip().lower()]
        if year_val is not None and year_val is not None:
            year_operator.strip()
            if year_operator == '>':
                filtered_list = [bridge for bridge in filtered_list
                                if year_val >= 
                                bridge.year_built]
            if year_operator == '<':
                filtered_list = [bridge for bridge in filtered_list
                                if year_val <= 
                                bridge.year_built]
            if year_operator == '=':
                filtered_list = [bridge for bridge in filtered_list
                                if year_val == 
                                bridge.year_built]
        self.view_bridges(filtered_list)

    def save_changes(self, bridge_list: list = None):
        """Saves JSON file with self.bridge_list contents"""
        if bridge_list == None:
            bridge_list = self.bridge_list
        data = {"bridges": []}
        for br in bridge_list:
            inspections = []
            for insp in getattr(br, "inspections", []):
                date_str = getattr(insp, "date", None).strftime("%Y-%m-%d")
                inspections.append({
                    "date": date_str,
                    "inspector": getattr(insp, "inspector", ""),
                    "score": getattr(insp, "score", None),
                    "defects": getattr(insp, "defects", ""),
                    "recommendations": getattr(insp, "recommendations", "")
                })

            data["bridges"].append({
                "id": getattr(br, "bridge_id", ""),
                "name": getattr(br, "name", ""),
                "location": getattr(br, "location", ""),
                "bridge_type": getattr(br, "bridge_type", ""),
                "year_built": getattr(br, "year_built", None),
                "inspections": inspections
            })
        self.file_manager.write_file(data)
        
    def start_menu(self):
        """Looping function which displays the menu and options avaialable.
        user then selects option which call a function in the mneus dictionary"""
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
            except KeyboardInterrupt:
                print("\nExited via keyboard")
            self.start_menu()

    def run(self):
        """main application starts from here"""
        try:
            self.import_bridge_list()
            self.setup_menu(self.main_menu)()
            self.start_menu()
            
        except Exception as error:
            print(error)
        
        finally:
            if not self.debug:
                self.save_changes()
        

         

