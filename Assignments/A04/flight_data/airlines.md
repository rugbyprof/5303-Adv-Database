## Airlines

Source: https://openflights.org/data.html

### Overview / Notes
- As of January 2012, the OpenFlights Airlines Database contains 5888 airlines. 
- The data is UTF-8 encoded. The special value \N is used for "NULL" to indicate that no value is available, and is understood automatically by MySQL if imported.
-  Each entry contains the following information:

### Data 

| Field | Explanation | 
|:------|:------------|
|Airline ID	 | Unique OpenFlights identifier for this airline.|
|Name	 | Name of the airline.|
|Alias	 | Alias of the airline. For example, All Nippon Airways is commonly known as "ANA".|
|IATA	 | 2-letter IATA code, if available.|
|ICAO	 | 3-letter ICAO code, if available.|
|Callsign	 | Airline callsign.|
|Country	 | Country or territory where airline is incorporated.|
|Active	 | "Y" if the airline is or has until recently been operational, "N" if it is defunct. This field is not reliable: in particular, major airlines that stopped flying long ago, but have not had their IATA code reassigned (eg. Ansett/AN), will incorrectly show as "Y".|
