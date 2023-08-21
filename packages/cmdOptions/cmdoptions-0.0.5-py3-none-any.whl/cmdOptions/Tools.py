from platform import system as platform
from os import system as command

class Tools:
    '''
    Class that holds helpful command-line tools.
    '''

    # Holds os platform command-line clear commands
    _ClearCommand = {
        "Windows": "cls",
        "Linux": "clear",
        "Darwin": "clear" # This is MacOS
    }

    def get_system_type() -> str:
        ''' Returns os platform. '''
        return platform()
    
    def clearScreen(os_name: str) -> None:
        '''
        Clears command-line based on os_name.
        NOTE: use "get_system_type" tools function to get os name.

        Args:
        - os_name (str): name of operating system
        '''
        command(Tools._ClearCommand[os_name])

    def waitForEnter() -> None:
        ''' Pauses input until enter key is pressed. '''
        input("\nPress enter to continue.....")