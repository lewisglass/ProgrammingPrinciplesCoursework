import bridge
import file_handler

class BridgeManagmentSystem:

    def __init__(self):
        """Contructor for BridgeManagmentSystem class"""
        self.__bridge_list = []
        self.__file_manager = file_handler.FileOperations("bridge_data.json")

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
        
    def add_bridge(self, bridge):
        """Add a bridge to the list of bridges"""
        self.__bridge_list.append(bridge)

    def print_bridges(self):
        for i in self.bridge_list:
            print(i)
            print(i.id)
            print(i.name)
            print(i.location)
            print(i.bridge_type)
            print(i.year_built)
            print(i.inspections)

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
    
        
