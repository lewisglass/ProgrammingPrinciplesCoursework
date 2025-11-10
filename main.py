import bridge_managment_system

def main():
    bridge_manager = bridge_managment_system.BridgeManagmentSystem()
    bridge_manager.import_bridge_list()
    bridge_manager.print_bridges()

    while(True):
        print("")

if __name__ == "__main__":
    main()