
# Mexico Inflation Calculator

## What it does

A simple script used to determine inflation in Mexico between two periods.

The program connects through an API to the National Institute of Statistics and Geography in Mexico (INEGI) and retrieves the relevant monthly Consumer Price Index (INPC) values.

- The user will input an initial and final date.

- The script will then output the index values for each month.

- It will also calculate the inflation percentage for the period.

## How to Install

To use this script, you must have previously installed python 3 and the following python libraries:

- Python 3
- IPython
- Pandas
- Numpy
- Requests

You will also need a (free) API token from INEGI, which can be obtained here:
[INEGI API KEY](http://en.www.inegi.org.mx/app/api/denue/v1/tokenVerify.aspx)

Once you have the API token, paste it in the file named: ```api_key_blank.py```

Rename the file to ```api_key.py```

You can then run the python script from terminal.

## How to Use

When running the script, the terminal will automatically display the last value in Mexican Consumer Price Index (INPC) and will ask for two dates from the user in the format: yyy-mm

The program will then retrieve the monthly index values during the period and calculate the inflation between the two dates.

Output will display the inflation for the period, as well as the Index values of the period.

<img src="https://www.bite-size.mx/inpc_example.gif" alt="INPC_example" width="600" height="392">

## Use cases

The script may be useful for accountants, administrative, financial professionals or anyone who needs to determine inflation over specific time periods.

It can help to quickly determine adjustments for:

- Rent prices.
- A stock's inflation adjusted cost basis.
- A salary increase to maintain purchasing power.
- Any asset value that is periodically adjusted for inflation.

## Contributing

Any help making the script into an executable file for windows and mac would be very helpful.

This would allow non-programmers to use it.
