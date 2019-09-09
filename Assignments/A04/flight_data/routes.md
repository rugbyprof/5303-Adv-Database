## Routes

Source: https://openflights.org/data.html

### Overview / Notes
- As of June 2014, the OpenFlights/Airline Route Mapper Route Database contains 67663 routes between 3321 airports on 548 airlines spanning the globe. 
- The data is UTF-8 encoded. The special value \N is used for "NULL" to indicate that no value is available, and is understood automatically by MySQL if imported.
-  Each entry contains the following information:

### Data 

| Field | Explanation | 
|:------|:------------|
|Airline |	2-letter (IATA) or 3-letter (ICAO) code of the airline.|
|Airline ID|	Unique OpenFlights identifier for airline (see Airline).|
|Source airport|	3-letter (IATA) or 4-letter (ICAO) code of the source airport.|
|Source airport ID|	Unique OpenFlights identifier for source airport (see Airport)|
|Destination airport|	3-letter (IATA) or 4-letter (ICAO) code of the destination airport.|
|Destination airport ID|	Unique OpenFlights identifier for destination airport (see Airport)|
|Codeshare|	"Y" if this flight is a codeshare (that is, not operated by Airline, but another carrier), empty otherwise.|
|Stops|	Number of stops on this flight ("0" for direct)|
|Equipment|	3-letter codes for plane type(s) generally used on this flight, separated by spaces|
