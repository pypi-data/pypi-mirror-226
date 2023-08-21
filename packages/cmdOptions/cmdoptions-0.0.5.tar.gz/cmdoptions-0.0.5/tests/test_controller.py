import cmdOptions.Controller as c

class Test_Controller:
    '''
    This is the class that holds all of the testing for the Controller allowing for the tesing of a single instance of the Controller class.
    '''

    controller = c.Controller()

    def option1_test():
        ''' This is a throw away function for testing '''
        print("option1")

    def option2_test():
        ''' This is a throw away function for testing '''
        print("option2")

    def test_add_option(self):
        '''
        This tests adding option names and functions into the Controller class 
        '''

        self.controller.addOption("option1", Test_Controller.option1_test)
        self.controller.addOption("option2", Test_Controller.option2_test)

        assert self.controller.get_options() == ["option1", "option2"]

    def test_list_length(self):
        '''
        This tests getting option length of the list after adding options in the Controller class 
        '''

        assert self.controller.get_optionListLength() == 2
    
    def test_remove_option(self):
        '''
        This tests removing option names and functions into the Controller class 
        '''
        
        self.controller.removeOption("option1")

        assert self.controller.get_options() == ["option2"]

    def test_remove_list_length(self):
         '''
        This tests getting option length of the list after removing options in the Controller class 
        '''
         assert self.controller.get_optionListLength() == 1
        

    def test_clear_options(self):
        '''
        This tests the clearing of the list in the Controller class 
        '''
        self.controller.clearOptions()

        assert self.controller.get_optionListLength() == 0