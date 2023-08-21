import time
from cmdOptions.Tools import Tools

class Controller:

    def __init__(self):
        self._optionsList = list()
        self._optionListLength = 0
        self.userInput = ''
        self._system_type = Tools.get_system_type()

    def addOption(self, option: str, funcLink) -> None:
        '''
        Adds the specified option to the Controller instance.
        
        Args:
       - option (str): Display name of the option to add
       - funcLink (function): Function that is called when option is selected by user
        
        Returns:
        - None
        '''
        self._optionsList.append( [option, funcLink] )
        self._optionListLength = len(self._optionsList)
    
    def removeOption(self, option: str) -> None:
        '''
        Removes the specified option from the Controller instance.

        Args:
        - option (str): Display name of the option to remove

        Returns:
        - None
        '''
        for index, item in enumerate(self._optionsList):
            if item[0] == option:
                del self._optionsList[index]
        self._optionListLength -= 1

    def get_optionListLength(self) -> int:
       '''
       Returns the number of options in Controller instance.

       Returns:
       - int
       '''
       return self._optionListLength
    
    def get_options(self) -> list:
        '''
        Returns all option names in the Controller instance and returns them in a list.

        Returns:
        - list(str)
        '''
        return [item[0] for item in self._optionsList]
    
    def clearOptions(self) -> None:
        ''' Removes all options from the Controller instance. '''
        self._optionsList.clear()
        self._optionListLength = len(self._optionsList)

    def printOptions(self) -> None:
        ''' Prints out all options in the Controller instance. '''
        for index, item in enumerate(self._optionsList):
            print(f'{index + 1}. {item[0]}')
    
    def _runFunc(self, id: int) -> None:
        '''
        Runs the function of the specified option.

        Args:
        - id(int): The index of the option in the controller instance list

        Returns:
        - None
        '''
        self._optionsList[id - 1][1]()

    def runLoop(self) -> None:
        '''
        Displays the options and checks for inputs for all options in the Controller instance.
        (The main loop of the Control instance)
        '''
        self._optionListLength = len(self._optionsList)
        while self.userInput != str(self._optionListLength +1):

            print("Enter one of the options: \n")
            self.printOptions()
            print(f"{len(self._optionsList)+1}. Quit")
            self.userInput = input("\n> ")

            if self.userInput == str(self._optionListLength + 1):
                Tools.clearScreen(self._system_type)
                break
            
            elif self.userInput.isnumeric() and 0 < int(self.userInput) <= self._optionListLength:
                Tools.clearScreen(self._system_type)
                self._runFunc(int(self.userInput))

            else:
                Tools.clearScreen(self._system_type)

                print(f"\nOption \"{self.userInput}\" does not exist, please try again.")
                time.sleep(3)

                Tools.clearScreen(self._system_type)