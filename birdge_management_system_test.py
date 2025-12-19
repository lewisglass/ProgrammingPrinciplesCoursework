import unittest
from bridge_management_system import BridgeManagementSystem
from bridge import Bridge
from file_handler import FileOperations
from display import Display

class TestController(unittest.TestCase):
    """test class to test non behaviouristic attributes and methods of BridgeManagementSystem"""

    def setUp(self):
        self.controller = BridgeManagementSystem(True)
        self.assertIsInstance(self.controller, BridgeManagementSystem)

    def test_total_bridges(self):
        self.controller.bridge_list = [Bridge("B0010", [], "TestBridge1", "Glasgow", "Cantilever", 1990), 
                                       Bridge("B0011", [], "TestBridge2", "Edinburgh", "Arch", 1991), 
                                       Bridge("B0012", [], "TestBridge3", "Dundee", "Beam", 1992)]
        self.assertEqual(self.controller.total_bridges(), 3)

    def test_setup_menu(self):
        change = self.controller.setup_menu("main_menu")
        self.assertTrue(callable(change))
        change()
        self.assertEqual(self.controller.current_menu, "main_menu")

    def test_file_manager(self):
        fm = FileOperations("My_file.txt")
        self.controller.file_manager = fm
        self.assertIs(self.controller.file_manager, fm)

    def test_bridge_list(self):
        bridges = [Bridge("B0014", [], "TestBridge4", "Hamilton", "Beam", 1994), 
                    Bridge("B0015", [], "TestBridge5", "Stirling", "Suspension", 1995), 
                    Bridge("B0016", [], "TestBridge6", "Aberdeen", "Truss", 1996)]
        self.controller.bridge_list = bridges
        self.assertEqual(self.controller.bridge_list, bridges)

    def test_bridge_list_empty(self):
        self.controller.bridge_list = []
        self.assertEqual(self.controller.bridge_list, [])

    def test_display_handler(self):
        disp = Display()
        self.controller.display_handler = disp
        self.assertIs(self.controller.display_handler, disp)



if __name__ == "__main__":
    unittest.main()