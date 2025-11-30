import bridge
import file_handler
import display

class BridgeManagmentSystem:

    def __init__(self):
        """Contructor for BridgeManagmentSystem class"""
        self.bridge_list = []
        self.file_manager = file_handler.FileOperations("bridge_data.json")
        self.display = display.Display(1)

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
        for i in from_file:
            new_bridge = bridge.Bridge(
                id = i["id"],
                name = i["name"],
                location = i["location"],
                bridge_type = i["bridge_type"],
                year_built = i["year_built"],
                inspections = i["inspections"])
            self.bridge_list.append(new_bridge)

    def add_bridge(self, bridge):
        """Add a bridge to the list of bridges"""
        self.__bridge_list.append(bridge)

    def add_inspection(self):
        print("TO DO!!!!")

    def print_bridges(self):
        for i in self.bridge_list:
            print(f"Bridge ID    :  {i.id}")
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

    def bridge_menu(self):
        bridge_menu_dict = {
            1 : self.add_bridge,
            2 : self.add_inspection,
            3 : self.main_menu
        }
        choice = 0
        self.display.bridge_menu_display()
        self.print_bridges()
        while True:
            print("Enter a choice (1-3):")
            try:
                choice = int(input().strip())
                if choice in bridge_menu_dict:
                    bridge_menu_dict[choice]()
                else:
                    print("Invalid, make a new choice: ")
            except ValueError:
                print("Invalid, choice must be an integer, make a new choice")
        
    def exit(self):
        print("Goodbye!")
        quit()

    def main_menu(self):
        main_menu_dict = {
            1 : self.bridge_menu,
            2 : self.add_bridge,
            3 : self.exit
        }
        choice = 0
        self.display.main_menu_display()
        while True:
            print("Enter a choice (1-3):")
            try:
                choice = int(input().strip())
                if choice in main_menu_dict:
                    main_menu_dict[choice]()
                else:
                    print("Invalid, make a new choice: ")
            except ValueError:
                print("Invalid, choice must be an integer, make a new choice")

    def run(self):
        
        try:
            self.import_bridge_list()
            self.main_menu()
            
        except ValueError as error:
            print(error)
        

         

