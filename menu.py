class Menu:
    """controls the menu diplsayed to the user and the functions that
    each option within it points to"""
    def __init__(self, name, options):
        """Menu constructor"""
        self.name = name
        self.options = options

    @property
    def name(self):
        """Getter for __name"""
        return self.__name
    
    @name.setter
    def name(self,name):
        """Setter for __name"""
        self.__name = name

    @property
    def options(self):
        """Getter for __options"""
        return self.__options
    
    @options.setter
    def options(self,options):
        """Setter for __options"""
        self.__options = options

    def option_name(self, index):
        """returns option name for displaying the menu"""
        name, _ = self.options.get(index)
        return name
    
    def option_func(self, index):
        """returns option function for displaying the menu"""
        _, func= self.options.get(index)
        return func