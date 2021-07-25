
# Mexico Inflation Calculator


### What it does

A simple script used to determine inflation in Mexico between two periods.

The program connects through an API to the National Institute of Statistics and Geography in Mexico (INEGI) and retrieves the relevant monthly Consumer Price Index (INPC) values. 

The user will input an initial and final date. 

The script will then output the inflation for the period along with the INPC values for each month.


### How to Install

To use this script, you must have previously installed:
- Python 3
- IPython
- Pandas
- Numpy
- Requests

You will also need a (free) API token from INEGI, which can be obtained here:
[INEGI API KEY](https://www.inegi.org.mx/servicios/api_indicadores_1.0.html#token)

Once you have the API token, paste it in the file named: ```api_key_blank.py```

Rename the file to ```api_key.py```

You can then run the python script from terminal. 

If you use this information frequently, I recommend adding an alias to the script path to make it simpler. 


### How to Use

When run, it will automatically display the last value in Mexican Consumer Price Index (INPC) and will ask for two dates from the user. 

The program will then retrieve the monthly index values during the period and calculate the inflation between the two dates.

Output will display the inflation for the period, as well as the Index values of the period.

<img src="https://www.bite-size.mx/inpc_example.gif" alt="INPC_example" width="600" height="392">


### Use cases

The script is useful for accountants or administrative/financial professionals. 
It can help to quicky determine adjustments for:
- Rent prices
- A stock's cost basis
- A salary increase to maintain purchasing power
- Any asset value that is periodically adjusted for inflation


### Contributing
If you can help making this a simple executable file for windows and mac, so non-programmers can use it, it would be much appreciated. 

### Credits
Pablo Cruz Lemini.
February 2021
