import json
import os

class FileOperations:

    def __init__(self, directory):
        """FileOperations class constructor"""
        self.directory = directory
    
    @property
    def directory(self):
        """Getter for __directory"""
        return self.__directory

    @directory.setter
    def directory(self, filename):
        """Setter for __directory"""
        directory = os.path.join(os.path.dirname(__file__), filename)
        self.__directory = directory

    def verify_filename(self):
        """Verifies that database exists and is accesible"""
        if os.path.exists(self.directory):
            print("File exists!!!")
        else:
            print("File does not exist.")
        if os.path.isfile(self.directory):
            print("Is File!!!")
        else:
            print("Is not a file.")
        if os.access(self.directory, os.F_OK):
            print("Is readable!!!")
        else:
            print("File is not readable")
        if os.access(self.directory, os.W_OK):
            print("Is Writeable!!!")
        else:
            print("File is not writeable")

    def read_file(self):
        open_file = open(self.directory)
        parsed_data = json.load(open_file)
        return parsed_data["bridges"]
            
        open_file.close()
            
            


