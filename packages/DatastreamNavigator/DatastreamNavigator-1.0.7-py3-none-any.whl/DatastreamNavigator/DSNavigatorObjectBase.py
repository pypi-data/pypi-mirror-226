from enum import IntEnum
from datetime import date

class DSNavigatorResponseStatus(IntEnum):
    """ Defines the status of any search request on Datastream Navigator.

    NavigatorSuccess : Specifies the request completed successfully.
    NavigatorError : A generic Navigator error. See the object's ErrorMessage property for a description of the failure
    """
    NavigatorSuccess = 0
    NavigatorError = 1


class DSDatatypeFilter(IntEnum):
    """
    Datastream Navigator can be used to search for and return a list of selected datatypes. Datatypes can either be static or timeseries based.
    When launching the navigator to search for datatypes, you can specify if the search should be timeseries only, static only, or both.
    """
    AllDatatypes = 0   # Search across both timeseries and static datatypes.
    TimeseriesOnly = 1 # Search across timeseries datatypes only.
    StaticOnly = 2     # Search across static datatypes only.


class DSNavigatorCategory(IntEnum):
    """
    Datastream Navigator can be used to search for and return a list of selected instruments. Each returned instrument is defined
    in a DSNavigatorSeries class. The Category property of DSNavigatorSeries defines which classification the instrument is defined as,
    such as Equities, Commodities, Exchange Rates, etc.

    The DSNavigatorCategory can also be supplied in the SeriesSearch method to define a filter Datastream Navigator should apply.
    """
    Unspecified = -1           # When using DSNavigatorCategory in the SeriesSearch method this instructs Datastream Navigator to apply no filter on the instrument type.
    Equities = 0               # The returned instrument is a listed equity.
    ConstituentLists = 1       # The returned instrument is a constituent list.
    EquityIndices = 3          # The returned instrument is an equity index.
    Funds = 4                  # The returned instrument is a fund such as a unit trust.
    InvestmentTrusts = 5       # The returned instrument is an investment trust.
    Commodities = 6            # The returned instrument is a commodity.
    ExchangeRates = 7          # The returned instrument is an exchange rate.
    InterestRates = 8          # The returned instrument is an interest rate.
    BondIndicesCDS = 9         # The returned instrument is a bond index or contract for difference.
    Warrants = 11              # The returned instrument is a warrant.
    Economics = 12             # The returned instrument is an economic series.
    BondsConvertibles = 13     # The returned instrument is a bond or convertible.
    Options = 14               # The returned instrument is an option.
    Futures = 15               # The returned instrument is a future.
    CreditDefaultSwap = 32     # The returned instrument is a credit default swap.
    UserCreatedIndices = 42    # The returned instrument is a user created index.
    UserCreatedLists = 43      # The returned instrument is a user created list.
    UserCreatedTimeSeries = 57 # The returned instrument is a user created timeseries.


class DSNavigatorSeries:
    """ DSNavigatorSeries is class is used to represent the details of each instrument returned by Datastream Navigator.
   
        Properties :
        ----------
        PrimaryCode : The primary identifier for the instrument as returned by Datastream Navigator eg: the mnemonic @AAPL for Apple Inc.
        PrimaryCodeType : The type of the primary identifier. e.g. MNEM, DSCD, ISIN, etc.
        Category: A DSNavigatorCategory enumeration instance defining the classification of the instrument within Datastream.
        Name : The display name for the instrument. eg: APPLE.
        BaseDate : The date this instrument was created or first listed on Datastream.
        Codes : A list of Key-Value pairs defining all the returned identifiers for the instrument. The returned Key values can be:
                MNEM - This is a unique identification code assigned by Datastream. 
                DSCD - This is the unique six-digit identification code for every stock, allocated by Datastream.
                LOC - This is an identification code based on the instrument's official local exchange code.
                ISIN - The International Security Identification Number. A code that uniquely identifies a security.
                SECD - This is an identification code based on the code issued by the London Stock Exchange.
                RIC - The Reuters Instrument Code. Note this datatype is permissioned. Please consult your LSEG account manager.
                LTYPE - A description of the type of user created list returned. e.g. 'Datastream List'
    """
    def __init__(self, series_dict):
        self.PrimaryCode = series_dict.pop("Key", "")
        self.PrimaryCodeType = series_dict.pop("KeyType", "")
        try:
            self.Category = DSNavigatorCategory(int(series_dict.pop("CategoryID", "-1")))
        except:
            self.Category = DSNavigatorCategory.Unspecified
        series_dict.pop("CategoryName", '')  # We don't use this
        self.Name = series_dict.pop("NAME", "") 
        self.BaseDate = date.fromisoformat(series_dict.pop("BDATE", "0001-01-01")) 
        self.Codes = series_dict
      
        
class DSNavigatorDatatype:
    """ DSNavigatorDatatype is class is used to represent the details of each datatype returned by Datastream Navigator.
   
        Properties :
        ----------
        Key : Symbol of the datatype eg: BP for Price to Book Value
        Name : Description of the datatype eg: Price to Book Value
        """
    def __init__(self, dtypes_dict):
        self.Key = dtypes_dict.pop("Key", "")
        self.Name = dtypes_dict.pop("Name", "") 
        
class DSNavigatorSeriesResponse:
    """ Navigator series response returned to the User 
    
        Properties:
        ----------
        Series : A list of the DSNavigatorSeries objects describing each instrument returned from Datastream Navigator.
        SeriesCount : The number of instruments returned.
        ResponseStatus: This property will contain a DSNavigatorResponseStatus value. DSNavigatorResponseStatus.NavigatorSuccess represents a successful response.
        ErrorMessage: If ResponseStatus is not DSNavigatorResponseStatus.NavigatorSuccess this status string will provide a description of the error condition.
        """
    def __init__(self, navSeries, responseStatus = DSNavigatorResponseStatus.NavigatorSuccess, seriesCount = 0, errorMsg = ""):
       self.Series = navSeries
       self.SeriesCount = seriesCount
       self.ResponseStatus = responseStatus
       self.ErrorMessage = errorMsg    
       
class DSNavigatorDatatypesResponse:
    """ Navigator Datatypes response returned to the User 
    
        Properties:
        ----------
        Datatypes : A list of the DSNavigatorDatatype objects describing each datatype returned from Datastream Navigator.
        DatatypesCount : The number of datatypes returned.
        ResponseStatus: This property will contain a DSNavigatorResponseStatus value. DSNavigatorResponseStatus.NavigatorSuccess represents a successful response.
        ErrorMessage: If ResponseStatus is not DSNavigatorResponseStatus.NavigatorSuccess this status string will provide a description of the error condition.
        """ 
    def __init__(self, navDtypes, responseStatus = DSNavigatorResponseStatus.NavigatorSuccess, dtypesCount = 0, errorMsg = ""):
       self.Datatypes = navDtypes
       self.DatatypesCount = dtypesCount 
       self.ResponseStatus = responseStatus
       self.ErrorMessage = errorMsg       


    
    
    
   
    
    

