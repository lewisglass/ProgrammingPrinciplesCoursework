import inspection

class Bridge:

    def __init__(self, bridge_id, inspections, name, location, bridge_type, year_built):
        """Bridge class contructor"""
        self.bridge_id = bridge_id
        self.name = name
        self.location = location
        self.bridge_type = bridge_type
        self.year_built = year_built
        self.inspections = inspections
        self.average_score = self.calculate_average_score()

    @property
    def bridge_id(self):
        """Getter for __bridge_id"""
        return self.__bridge_id
    
    @bridge_id.setter 
    def bridge_id(self, bridge_id):
        """Setter for __bridge_id"""
        self.__bridge_id = bridge_id

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
        self.__inspections = inspections
        
    def calculate_average_score(self):
        """Sets average score"""
        total_score = 0
        for inspection in self.inspections:
            total_score += inspection.score
        if len(self.inspections) != 0:
            return total_score / len(self.inspections)
        else: 
            return None
        
    @property
    def average_score(self):
        """Getter for __average_score"""
        return self.__average_score
    
    @average_score.setter 
    def average_score(self, average_score):
        """Setter for __average_score"""
        self.__average_score = average_score        
    
        
        