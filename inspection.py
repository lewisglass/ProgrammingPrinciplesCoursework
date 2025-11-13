
from datetime import datetime
class Inspection:
    
    def __init__(self, date, inspector, score, defects, recommendations):
        self.date = date
        self.inspector = inspector
        self.score = score
        self.defects = defects
        self.recommendations = recommendations
        
    @property
    def date(self):
        """Getter for __date"""
        return self.__date
    
    @date.setter
    def date(self, date):
        """Setter for __date"""
        date_format = '%Y-%m-%d'
        self.__date = datetime.strptime(date, date_format)
    
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
    def recommendations(self):
        """Getter for __recommendations"""
        return self.__recommendations
    
    @recommendations.setter
    def recommendations(self, recommendations):
        """Setter for __recommendations"""
        self.__recommendations = recommendations