
class Display:
    
    def __init__(self, current_state):
        self.curent_state = current_state
        
    @property
    def current_state(self):
        """Getter for __current_state"""
        return self.current_state
    
    @current_state.setter
    def current_state(self, current_state):
        self.__current_state = current_state
        
    def main_menu(self):
        print("_" * 70)
        print("|", "Main Menu".center(68), "|")
        print("_" * 70)
        print("|", " " * 68, "|")
        print("|   Select an option:")
        print("|")
        print("|   1. View all bridges")
        print("|   2. Add a bridge")
    