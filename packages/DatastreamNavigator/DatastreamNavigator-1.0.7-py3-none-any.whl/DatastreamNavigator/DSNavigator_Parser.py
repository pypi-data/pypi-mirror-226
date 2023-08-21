import re 
from .DSNavigatorObjectBase import *

class DSNavigator_Parser(object):
    """description of class"""

    @staticmethod
    def GetSelected_Series(rawString):

        # rawString format should be of the following form with pipe delimited selections (first item is always control settings):
        # ds:_ITEMS_COUNT=7|Key=@AAPL;KeyType=MNEM;CategoryID=0;CategoryName=Equities;NAME=APPLE;BDATE=1980-12-12;MNEM=@AAPL;DSCD=992816;LOC=U037833100;ISIN=US0378331005;SECD=2046251|Key=MSWRLD$;KeyType=MNEM;CategoryID=3;CategoryName=Equity Indices;NAME=MSCI WORLD;BDATE=1969-12-31;MNEM=MSWRLD$|....
       
        if (rawString is None) or (len(rawString) == 0):
            return DSNavigatorSeriesResponse(None, DSNavigatorResponseStatus.NavigatorSuccess)
        
        try:
            selection = rawString.split("|")

            # First element is always present and identifies the response type and count of selected items.
            # Note, this is a semicolon separated list with subsequent sections for future enhancements
            # e.g. it could be  ds:_ITEMS_COUNT=7;futureControlSection1;futureControlSection2;...;futureControlSectionX
            # So, we ignore it
            if len(selection) <= 1:
                return DSNavigatorSeriesResponse(None, DSNavigatorResponseStatus.NavigatorSuccess)

            # parse all the elements after the first into DSNavigatorSeries items and return in a DSNavigatorSeriesResponse
            return DSNavigatorSeriesResponse(DSNavigator_Parser._getSeries(selection[1:]), DSNavigatorResponseStatus.NavigatorSuccess, len(selection) - 1)
        except Exception as exp:
            return DSNavigatorSeriesResponse(None, DSNavigatorResponseStatus.NavigatorError, errorMsg = str(exp))

    @staticmethod
    def GetSelected_Datatypes(rawString):
        # rawString format should be of the following form with pipe delimited selections (first item is always control settings):
        # ds:_TYPES_COUNT=4|Key=PI;Name=Price Index|Key=338E;Name=12M Forward Net Debt/Enterprise Value|Key=553E;Name=12M Forward Price/Book|Key=ISIN;Name=Code - Isin
       
        if (rawString is None) or (len(rawString) == 0):
            return DSNavigatorDatatypesResponse(None, DSNavigatorResponseStatus.NavigatorSuccess)
        
        try:
            selection = rawString.split("|")

            # First element is always present and identifies the response type and count of selected datatypes.
            # Note, this is a semicolon separated list with subsequent sections for future enhancements
            # e.g. it could be  ds:_TYPES_COUNT=4;futureControlSection1;futureControlSection2;...;futureControlSectionX
            # So, we ignore it
            if len(selection) <= 1:
                return DSNavigatorDatatypesResponse(None, DSNavigatorResponseStatus.NavigatorSuccess)

            # parse all the elements after the first into DSNavigatorDatatype items and return in a DSNavigatorDatatypesResponse
            return DSNavigatorDatatypesResponse(DSNavigator_Parser._getTypes(selection[1:]), DSNavigatorResponseStatus.NavigatorSuccess, len(selection) - 1)
        except Exception as exp:
            return DSNavigatorDatatypesResponse(None, DSNavigatorResponseStatus.NavigatorError, errorMsg = str(exp))

    @staticmethod
    def _parse(data):
        parsedData = []
        try:
            for x in data:
                data_fields = x.split(";") if (";" in x) else None
                if data_fields is not None:
                    data_dict = {}
                    for field in data_fields:
                        # If the value field has '=' in it as a valid character. Split only using the first '=' sign.
                        kv_Pair = field.split("=", 1) if ("=" in field) else None
                        if kv_Pair is not None:
                            data_dict.update( { kv_Pair[0].strip() : kv_Pair[1] } ) 
                    parsedData.append(data_dict)
            return parsedData
        except Exception as exp:
            raise exp
    
    @staticmethod
    def _getSeries(series):
        navSeries = []
        try:
            seriesList = DSNavigator_Parser._parse(series)
            for series_dict in seriesList:
                navSeries.append(DSNavigatorSeries(series_dict))
            return navSeries
        except Exception as exp:
             raise exp

    @staticmethod
    def _getTypes(dtypes):
        navDtypes = []
        try:
            dtypesList = DSNavigator_Parser._parse(dtypes)
            for dtypes_dict in dtypesList:
                navDtypes.append(DSNavigatorDatatype(dtypes_dict))
            return navDtypes
        except Exception as exp:
             raise exp

    

        


