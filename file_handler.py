import json
import os

class FileOperations:

    def __init__(self, filename):
        """FileOperations class constructor"""
        self.filename = filename
    
    @property
    def filename(self):
        """Getter for __filename"""
        return self.__filename

    @filename.setter
    def filename(self, filename):
        """Setter for __filename"""
        full_path = os.path.join(os.path.dirname(__file__), filename)
        self.__filename = full_path

    def verify_filename(self):
        """Verifies that database exists and is accesible"""
        if os.path.exists(self.filename):
            print("File exists!!!")
        else:
            print("File does not exist.")
        if os.path.isfile(self.filename):
            print("Is File!!!")
        else:
            print("Is not a file.")
        if os.access(self.filename, os.F_OK):
            print("Is readable!!!")
        else:
            print("File is not readable")
        if os.access(self.filename, os.W_OK):
            print("Is Writeable!!!")
        else:
            print("File is not writeable")

    def read_file(self):
        with open(self.filename) as open_file:
            parsed_data = json.load(open_file)
            return parsed_data["bridges"]
            
            
            


