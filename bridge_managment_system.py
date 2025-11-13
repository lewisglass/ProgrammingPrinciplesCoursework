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
        
    def add_bridge(self, bridge):
        """Add a bridge to the list of bridges"""
        self.__bridge_list.append(bridge)

    def print_bridges(self):
        for i in self.bridge_list:
            print(i.id)
            print(i.name)
            print(i.location)
            print(i.bridge_type)
            print(i.year_built)
            for j in i.inspections:
                print(j.date)
                print(j.inspector)
                print(j.score)
                print(j.recomendations)
                print(j.defects)
        self.display.main_menu()

    def import_bridge_list(self):
        """Imports list of bridges from bridge_data.json"""
        from_file = self.file_manager.read_file()
        print(from_file)
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
        
    def run(self):
        self.display.main_menu()
    
        
