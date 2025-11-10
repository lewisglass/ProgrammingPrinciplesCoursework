

class inspection:
    
    def __init__(self):
        self.__date = 0
        self.__inspector = "",
        self.__score = 0
        self.__defects = "",
        self.__recomedations = ""
        
    @property
    def date(self):
        """Getter for __date"""
        return self.__date
    
    @date.setter
    def date(self, date):
        """Setter for __date"""
        self.__date = date
    
    @property
    def inspector(self):
        """Getter for __inspector"""
        return self.__inspector
    
    @inspector.setter
    def inspector(self, inspector):
        """Setter for __inspector"""
        self.__inspector = inspector
    
    @property
    def score(self):
        """Getter for __score"""
        return self.__score
    
    @score.setter
    def score(self, score):
        """Setter for __score"""
        self.__score = score
        
    @property
    def defects(self):
        """Getter for __defects"""
        return self.__defects
    
    @defects.setter
    def defects(self, defects):
        """Setter for __score"""
        self.__defects = defects
    
    @property
    def recomedations(self):
        """Getter for __recomedations"""
        return self.__recomedations
    
    @recomedations.setter
    def recomedations(self, recomedations):
        """Setter for __score"""
        self.__recomedations = recomedations