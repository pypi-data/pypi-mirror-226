from .DSNavigator_Frame import *

class DSNavigator_App:
    """This class is responsible for the launch of Navigator frame and get the selected data in the form of a response Object"""

    def __init__(self, url, frameWidth, frameHeight):
        """1. wxpython toolkit is initialized only by wx.App
        2. An wx application should have only one wx.App
        3. Wx.App should be implemented in the main client class """
        self.dataResponse = None
        
        try:
            self.app = wx.App()
            self.navFrame = DSNavigator_Frame(url, frameWidth, frameHeight)
            self.navFrame.Bind(EVT_DATA_READY, self.Get_Data_Response) # On response data ready, Get_Data_Response gets the event response data 
            self.app.SetTopWindow(self.navFrame)
            self.app.MainLoop()
        except Exception as exp:
           print ("DSNavigator_App: ", "Exception Occured : ", str(exp))

    def Get_Data_Response(self, event):
        self.dataResponse = event.data
    
    def Get_Response_Object(self):
        self.app.Destroy()
        return self.dataResponse
        