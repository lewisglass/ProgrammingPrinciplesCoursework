import inspection
from datetime import datetime
import input_validation

class Bridge:

    bridge_types = ("Arch", "Tied Arch", "Suspension", "Beam", 
                             "Truss", "Cantilever", "Cable-Stayed")

    def __init__(self, bridge_id, inspections, name,
                  location, bridge_type, year_built):
        """Bridge class contructor"""
        self.bridge_id = bridge_id
        self.name = name
        self.location = location
        self.bridge_type = bridge_type
        self.year_built = year_built
        self.inspections = inspections
    
    max_str_length = 4000
    max_name_length = 70
    min_year_built = 1320
    max_year_built = datetime.now().year

    @classmethod
    def validate_bridge_id(cls, bridge_id: str) -> str:
        """Static method for validating bridge id"""
        input_validation.validate_str(bridge_id, 5, 5)
        if not bridge_id[0] == 'B':
            raise ValueError("Bridge id must start with a 'B'")
        try:
            int(bridge_id[1:])
        except ValueError as error:
            raise ValueError("""Bridge id must have format 
                            'Bnnnn' where n is numerical""") from error
        return bridge_id
    
    @classmethod
    def validate_name(cls, name: str) -> str:
        return input_validation.validate_str(name, 
                                      cls.max_name_length)
        
    @classmethod
    def validate_location(cls, location: str) -> str:
        return input_validation.validate_str(location, 
                                      cls.max_name_length)
        
    @classmethod
    def validate_bridge_type(cls, bridge_type : str) -> str:
        """Class method for validating bridge type"""
        if not isinstance(bridge_type, str):
            raise TypeError("Bridge type field must be a string")
        if not bridge_type.strip():
            raise ValueError("Bridge type must not be an empty string")
        refined_bridge_type = bridge_type.strip().title()
        if refined_bridge_type not in cls.bridge_types:
            error_message = "Bridge type must be one of the following:\n" + "\n".join(cls.bridge_types)
            raise ValueError(error_message)
        return refined_bridge_type

    @classmethod
    def validate_year_built(cls, year_built: int | str) -> int:
        return input_validation.validate_int(year_built, 
                                      cls.min_year_built, 
                                      cls.max_year_built)

    def validate_inspections(self, inspections: list[inspection.Inspection]) -> list[inspection.Inspection]:
        """Method for validating inspections"""
        if not isinstance(inspections, list):
            raise TypeError("Bridge inspections list is not a list")
        if len(inspections) == 0:
            return inspections
        if not all(isinstance(instance, inspection.Inspection) 
                for instance in inspections):
            raise TypeError("Bridge inspections list contains non inspections")
        if not all(instance.date.year >= self.year_built 
                for instance in inspections):
            raise ValueError("Inspection cannot be older than the bridge")
        return inspections
    
    @property
    def bridge_id(self) -> str:
        """Getter for __bridge_id"""
        return self.__bridge_id
    
    @bridge_id.setter 
    def bridge_id(self, bridge_id: str):
        """Setter for __bridge_id"""
        self.__bridge_id = self.validate_bridge_id(bridge_id)

    @property
    def name(self) -> str:
        """Getter for __name"""
        return self.__name
    
    @name.setter
    def name(self, name: str):
        """Setter for __name"""
        self.__name = Bridge.validate_name(name)
        
    @property
    def location(self) -> str:
        """Getter for __location"""
        return self.__location
    
    @location.setter 
    def location(self, location: str):
        """Setter for __location"""
        self.__location = Bridge.validate_location(location)

    @property
    def bridge_type(self) -> str:
        """Getter for __bridge_type"""
        return self.__bridge_type
    
    @bridge_type.setter 
    def bridge_type(self, bridge_type: str):
        """Setter for __bridge_type"""
        self.__bridge_type = self.validate_bridge_type(bridge_type)

    @property
    def year_built(self) -> int:
        """Getter for __year_built"""
        return self.__year_built
    
    @year_built.setter 
    def year_built(self, year_built: int | str):
        """Setter for __year_built"""
        self.__year_built = Bridge.validate_year_built(year_built)
    @property
    def inspections(self) -> list[inspection.Inspection]:
        """Getter for __inspections"""
        return self.__inspections
    
    @inspections.setter 
    def inspections(self, inspections: list[inspection.Inspection]):
        """Setter for __inspections"""
        self.__inspections = self.validate_inspections(inspections) 

    def calculate_average_score(self) -> float | None:
        """Sets average score"""
        total_score = 0
        if self.inspections == []:
            return None
        for inspection in self.inspections:
            total_score += inspection.score
        return total_score / len(self.inspections)