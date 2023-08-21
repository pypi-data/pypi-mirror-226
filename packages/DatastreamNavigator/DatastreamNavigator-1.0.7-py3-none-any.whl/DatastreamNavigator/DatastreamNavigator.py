from .DSNavigator_App import DSNavigator_App
from enum import IntEnum
from datetime import date
import urllib

from .DSNavigatorObjectBase import DSNavigatorSeriesResponse, DSNavigatorDatatypesResponse, DSNavigatorResponseStatus, DSNavigatorCategory, DSDatatypeFilter


class DatastreamNavigator:
    """
    This class is used to create a Client object to launch the Datastream Navigator for selecting the Series or the Datatypes.
    Note : Different client objects needs to be created for Series and Datatypes, as shown in example below.
    After selection of the Series or the datatypes, the client returns a Series Response object or Datatypes response object 
    respectively. 
   
    An example provided below on how to create a clent object to get the Data response

    navClient = DatastreamNavigator()
    seriesDataResponse = navClient.SearchSeries("Navigator Series Url")

    datatypesDataResponse = navClient.SearchDatatypes("Navigator Datatypes Url")
    """

    def __init__(self, frameWidth = 1400, frameHeight = 800):
        # The urls for browsing Datastream Navigator can be obtained when you logon to the Datastream Api using DatstreamUCS module
        self.seriesSearchUrl = None 
        self.datatypeSearchUrl = None 

        # user can override default frame dimensions
        if isinstance(frameWidth, int):
            self.frameWidth = max(700, min(frameWidth, 1600))
        else:
            self.frameWidth = 1250
        if isinstance(frameHeight, int):
            self.frameHeight = max(500, min(frameHeight, 1000))
        else:
            self.frameHeight = 800


    def SearchSeries(self, categoryFilter = DSNavigatorCategory.Unspecified, searchFilter = ""):
        """ Method used to launch the navigator for the selection of series
        URL to launch the navigator to select instruments can be obtained in 2 ways :
        1. From the JSON Response of ClientAPI by providing the username, password and adding the RequestOption=NavigatorSeries,NavigatorDatatypes in Options
        2. From the DatastreamUCS package, by creating a client and logging in to retrieve the urls as shown in below code.
        
        import DatastreamUCS as dsws
        dsClient = dsws.Datastream(None, "YourId", "YourPwd")
        navigator = dsNavigator.DatastreamNavigator()
        navigator.seriesSearchUrl = dsClient.navigatorSeriesUrl
        seriesSearchResponse = navigator.SearchSeries()

        Parameters : categoryFilter - An optional DSNavigatorCategory value specifying which type of instruments to filter on.
                     searchFilter - An optional string that filters the stocks by name
                                    eg: Vodafone* list all the instruments containing Vodafone.
        """
        try:
            if self.seriesSearchUrl is not None and isinstance(self.seriesSearchUrl, str) and self.seriesSearchUrl.startswith("https"):
                # safety checks on custom filters we can append to the url
                typeFilterParam = ""
                searchFilterParam = ""
                if isinstance(categoryFilter, DSNavigatorCategory) and categoryFilter != DSNavigatorCategory.Unspecified:
                    typeFilterParam = "&nav_category={}".format(categoryFilter.value)
                if isinstance(searchFilter, str) and len(searchFilter) > 0:
                    if len(searchFilter) > 100:
                        searchFilter = searchFilter[0:100] + "*"
                    searchFilterParam = "&q=" + urllib.parse.quote(searchFilter)

                # Let's launch navigator with optional settings provided by the user
                compUrl = self.seriesSearchUrl + typeFilterParam + searchFilterParam
                series = DSNavigator_App(compUrl, self.frameWidth, self.frameHeight)
                data = series.Get_Response_Object()
                if isinstance(data, DSNavigatorSeriesResponse):
                    return data
                else:
                    return DSNavigatorSeriesResponse(None)
            else:
                return DSNavigatorSeriesResponse(None, DSNavigatorResponseStatus.NavigatorError, errorMsg = "Please set seriesSearchUrl with a valid url")
        except Exception as exp:
            return DSNavigatorSeriesResponse(None, DSNavigatorResponseStatus.NavigatorError, errorMsg = str(exp))
            

    def SearchDatatypes(self, typeFilter = DSDatatypeFilter.AllDatatypes, searchFilter = ""):
        """ Method used to launch the navigator for the selection of Datatypes

        URL to launch the navigator to select datatypes can be obtained in 2 ways :
        1. From the JSON Response of ClientAPI by providing the username, password and adding the RequestOption=NavigatorSeries,NavigatorDatatypes in Options
        2. From the DatastreamUCS package, by creating a client and logging in to retrieve the urls as shown in below code.
        
        import DatastreamUCS as dsws
        dsClient = dsws.Datastream(None, "YourId", "YourPwd")
        navigator = dsNavigator.DatastreamNavigator()
        navigator.datatypeSearchUrl = dsClient.navigatorDatatypesUrl
        datatypesSearchResponse = navigator.SearchDatatypes()

        Parameters : typeFilter -  An optional DSDatatypeFilter value specifying whether to filter to timeseries datatypes only, static datatypes, or both.
                     searchFilter - An optional string that filters the datatypes by name
                                    eg: Vol* list all the datatypes containing "vol".
        """
        try:
            if self.datatypeSearchUrl is not None and isinstance(self.datatypeSearchUrl, str) and self.datatypeSearchUrl.startswith("https"):
                # safety checks on custom filters we can append to the url
                typeFilterParam = ""
                searchFilterParam = ""
                if isinstance(typeFilter, DSDatatypeFilter) and typeFilter != DSDatatypeFilter.AllDatatypes:
                    typeFilterParam = "&nav_frequency={}".format("Static" if typeFilter == DSDatatypeFilter.StaticOnly else "Time%2BSeries")
                if isinstance(searchFilter, str) and len(searchFilter) > 0:
                    if len(searchFilter) > 100:
                        searchFilter = searchFilter[0:100] + "*"
                    searchFilterParam = "&q=" + urllib.parse.quote(searchFilter)

                # Let's launch navigator with optional settings provided by the user
                compUrl = self.datatypeSearchUrl + typeFilterParam + searchFilterParam

                datatypes = DSNavigator_App(compUrl, self.frameWidth, self.frameHeight)
                data = datatypes.Get_Response_Object()
                if isinstance(data, DSNavigatorDatatypesResponse):
                    return data
                else:
                    return DSNavigatorDatatypesResponse(None, DSNavigatorResponseStatus.NavigatorSuccess)
            else:
                return DSNavigatorDatatypesResponse(None, DSNavigatorResponseStatus.NavigatorError, errorMsg = "Please set datatypeSearchUrl to a valid url")
        except Exception as exp:
            return DSNavigatorDatatypesResponse(None, DSNavigatorResponseStatus.NavigatorError, errorMsg = str(exp))
            



