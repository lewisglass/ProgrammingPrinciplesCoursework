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

    def verify_file(self):
        """Verifies that database exists and is accesible"""
        try:
            with open(self.filename) as open_file:
                pass
        except (FileNotFoundError, IsADirectoryError, PermissionError) as error:
            raise
        
    def read_file(self):
        with open(self.filename) as open_file:
            parsed_data = json.load(open_file)
            return parsed_data["bridges"]
            
            
            


