

class Bridge:

    def __init__(self, id, inspections, name, location, bridge_type, year_built):
        """Bridge class contructor"""
        self.id = id
        self.name = name
        self.location = location
        self.bridge_type = bridge_type
        self.year_built = year_built
        self.inspections = inspections

    @property
    def id(self):
        """Getter for __id"""
        return self.__id
    
    @id.setter 
    def id(self, id):
        """Setter for __id"""
        self.__id = id

    @property
    def name(self):
        """Getter for __name"""
        return self.__name
    
    @name.setter
    def name(self, name):
        """Setter for __name"""
        self.__name = name
        
    @property
    def location(self):
        """Getter for __location"""
        return self.__location
    
    @location.setter 
    def location(self, location):
        """Setter for __location"""
        self.__location = location

    @property
    def bridge_type(self):
        """Getter for __bridge_type"""
        return self.__bridge_type
    
    @bridge_type.setter 
    def bridge_type(self, bridge_type):
        """Setter for __bridge_type"""
        self.__bridge_type = bridge_type

    @property
    def year_built(self):
        """Getter for __year_built"""
        return self.__year_built
    
    @year_built.setter 
    def year_built(self, year_built):
        """Setter for __year_built"""
        self.__year_built = year_built

    @property
    def inspections(self):
        """Getter for __inspections"""
        return self.__inspections
    
    @inspections.setter 
    def inspections(self, inspections):
        """Setter for __inspections"""
        self.__inspections = inspections