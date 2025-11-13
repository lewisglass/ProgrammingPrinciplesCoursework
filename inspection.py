

class Inspection:
    
    def __init__(self, date, inspector, score, defects, recomendations):
        self.date = date
        self.inspector = inspector,
        self.score = score
        self.defects = defects,
        self.recomendations = recomendations
        
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
        """Setter for __defects"""
        self.__defects = defects
    
    @property
    def recomendations(self):
        """Getter for __recomendations"""
        return self.__recomendations
    
    @recomendations.setter
    def recomendations(self, recomendations):
        """Setter for __recomendations"""
        self.__recomendations = recomendations