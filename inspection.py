from datetime import datetime
import input_validation

class Inspection:
    """class for controlling Inspection level logic"""
    
    max_str_length = 4000
    max_name_length = 70
    max_score = 100
    min_score = 0

    def __init__(self, date, inspector, score, defects, recommendations):
        """Inspection constructor"""
        self.date = date
        self.inspector = inspector
        self.score = score
        self.defects = defects
        self.recommendations = recommendations

    @staticmethod
    def validate_date(date: str) -> datetime:
        """Validation for datetime types from strings"""
        return input_validation.validate_date(date)
    @classmethod
    def validate_inspector(cls, inspector: str) -> str:
        """validation for strings"""
        return input_validation.validate_str(inspector,
                                             cls.max_name_length)
    @classmethod
    def validate_score(cls, score: int) -> int:
        """validation for ints"""
        return input_validation.validate_int(score, 
                                             cls.min_score, 
                                             cls.max_score)
    @classmethod
    def validate_defects(cls, defects: str) -> str:
        """validation for strings"""
        return input_validation.validate_str(defects,
                                             cls.max_str_length)
    @classmethod
    def validate_recommendations(cls, recommendations: str) -> str:
        """validation for strings"""
        return input_validation.validate_str(recommendations, 
                                             cls.max_str_length)

    @property
    def date(self) -> datetime:
        """Getter for __date"""
        return self.__date
    
    @date.setter
    def date(self, date: str):
        """Setter for __date"""
        self.__date = Inspection.validate_date(date)
        
    @property
    def inspector(self) -> str:
        """Getter for __inspector"""
        return self.__inspector
    
    @inspector.setter
    def inspector(self, inspector: str):
        """Setter for __inspector"""
        self.__inspector = Inspection.validate_inspector(inspector)
    
    @property
    def score(self) -> int:
        """Getter for __score"""
        return self.__score
    
    @score.setter
    def score(self, score: int):
        """Setter for __score"""
        self.__score = Inspection.validate_score(score)
        
    @property
    def defects(self) -> str:
        """Getter for __defects"""
        return self.__defects
    
    @defects.setter
    def defects(self, defects: str):
        """Setter for __defects"""
        self.__defects = Inspection.validate_defects(defects)
    
    @property
    def recommendations(self) -> str:
        """Getter for __recommendations"""
        return self.__recommendations
    
    @recommendations.setter
    def recommendations(self, recommendations: str):
        """Setter for __recommendations"""
        self.__recommendations = Inspection.validate_recommendations(recommendations)