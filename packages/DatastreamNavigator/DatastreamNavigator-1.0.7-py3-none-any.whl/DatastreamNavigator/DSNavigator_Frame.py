import wx
from wx import html2 as webview
import wx.lib.newevent as wxevent
import urllib
import time
import os

from .DSNavigatorObjectBase import *
from .DSNavigator_Parser import *

# Custom event handler 
(data_ready_event, EVT_DATA_READY) = wxevent.NewEvent()
class Data_Ready_Event(wx.EvtHandler):
    """ Event handler to return the Navigator Series or Datatypes"""
    data = None
    def __init__(self, navData):
        wx.EvtHandler.__init__(self)
        self.data = navData
        EVT_DATA_READY(self, self.set_navData)

    def set_navData(self, event):
        event.Skip()

    def get_navData(self):
        return self.data

class DSNavigator_Frame(wx.Frame):
    """ This class helps in launching the Navigator in a window frame. """
    
    def __init__(self, url, frameWidth, frameHeight, title = "Datastream Navigator"):
        if isinstance(frameWidth, int):
            frameWidth = max(400, min(frameWidth, 1600))
        else:
            frameWidth = 1250
        if isinstance(frameHeight, int):
            frameHeight = max(300, min(frameHeight, 1200))
        else:
            frameHeight = 800

        wx.Frame.__init__(self, None, title = title, size = (frameWidth, frameHeight))
       
        try:
            self.Url = url

            # Set the LSEG icon
            abspath = os.path.dirname(os.path.abspath(__file__))
            if os.path.exists(abspath + "/AppIcon.ico"):
                icon = wx.Icon(abspath + "/AppIcon.ico")
                self.SetIcon(icon)
             
            # Web browser
            self.browser = webview.WebView.New(self, backend = webview.WebViewBackendEdge, size = (800, 700))
            self.browser.LoadURL(self.Url)
            #time.sleep(3) # Wait for 3 seconds for the page to load
            
            mainBox = wx.BoxSizer(wx.VERTICAL)
            mainBox.Add(self.browser, 1, wx.EXPAND)
            
            self.browser.Bind(webview.EVT_WEBVIEW_NAVIGATING, self.Browser_Navigating)

            self.SetSizer(mainBox)
            self.Show()
        except Exception as exp:
            raise exp

    def Browser_Navigating(self, event):
        """ This is method is used to keep an eye on the Navigating Urls. After selection of the Series or datatypes, 
       the url from the Navigator is further parsed to get the key details of the selected Items"""

        navUrl = event.GetURL()

        try:
            if navUrl is not None:
                if navUrl.startswith("https"):
                    pass
                elif navUrl.startswith("ds:_ITEMS_COUNT="):
                    try:
                        SeriesResponse = DSNavigator_Parser.GetSelected_Series(urllib.parse.unquote(navUrl))
                    except Exception as exp:
                        SeriesResponse = DSNavigatorSeriesResponse(None, DSNavigatorResponseStatus.NavigatorError, errorMsg = str(exp))
                    wx.PostEvent(self, data_ready_event(data = SeriesResponse))
                    self.Close()
                elif navUrl.startswith("ds:_TYPES_COUNT="):
                    try:
                        DatatypesResponse = DSNavigator_Parser.GetSelected_Datatypes(urllib.parse.unquote(navUrl))
                    except Exception as exp:
                        DatatypesResponse = DSNavigatorDatatypesResponse(None, DSNavigatorResponseStatus.NavigatorError, errorMsg = str(exp))
                    wx.PostEvent(self, data_ready_event(data = DatatypesResponse))
                    self.Close()
        except Exception as exp:
            raise exp

    def OnClose(self, event):
        self.Destroy()


    


 



        
     
   


