# Radiosounding to CSV

This code is aimed at creating a CSV file or a Pandas DataFrame of **atmospheric sounding datas**. it takes as inputs a time period as well as a station number. 

It works by scrapping the data available on the website of the Wyoming University (http://weather.uwyo.edu/upperair/sounding.html). 

## Get a list of available station : 

The code *get_uwyo_station_list.py* is a slightly modify version of the mercury code : https://github.com/vlouf/mercury. It prints the list of available station sorted by continents : 
```
South America:

                Station id - Station name
                78970 - Piarco Int. Airport (TTPP)
                78988 - Hato Airport, Curacao (TNCC)
                82332 - Manaus (Aeroporto) (SBMN)
                83746 - Galeao (SBGL)
                83827 - Foz Do Iguacu (Aero) (SBFI)
                83840 - Curitiba (Aeroporto) (SBCT)
                85586 - Santo Domingo (SCSN)
                ...........
```
## Radiosounding data scrapping : 

The main code is *get_uwyo_sounding.py*. It downloads radiosounding data for a specified station and a given period from the University of Wyoming and format it nicely either in CSV or Pandas Dataframe. 

It contains two functions : 
* get_uwyo_sounding(year, month, FROM, TO, stnm, save_csv = False )
* get_soundings_by_dates(stnm, start,stop, save_csv = False)

### get_uwyo_sounding
The first code returns data for a given month as a pandas DataFrame with an option to save a CSV file:
```
year : int
month : int
FROM : int --> DDHH with DD the day between 1 and 31 et HH the hour of the sounding, either 00 or 12
TO : int --> same format
stnm : int --> station number
```
For example to generate a CSV of the data in TENERIFE (60018) form 01/01/2020 to 14/01/2020 : 
```
get_uwyo_sounding(2020, 1, 100, 1412, 60018, save_csv = True )
```
You can also save a single sounding by setting TO equal to FROM. 

### get_soundings_by_dates

This code is a generalization of the first one and enable itteration on multiple month : 
```
stnm : int --> station number
start str --> start date in the form "YYYYMMDDHH" /!\ HH has to be 00 or 12 /!\
stop str --> stop date in the form "YYYYMMDDHH" /!\ HH has to be 00 or 12 /!\
```
For example to generate a CSV of the data in TENERIFE (60018) form 01/01/2020 to 31/12/2020 : 
```
get_soundings_date(60018, '2020010100', '2020123112')
```

### Form of the output : 

+-------------------------------------------+-------------+-----------+-----------+-----------+--------------+-------------+--------------+-----------+-----------+-----------+
|                                           |   PRES(hPa) |   TEMP(C) |   DWPT(C) |   RELH(%) |   MIXR(g/kg) |   DRCT(deg) |   SKNT(knot) |   THTA(K) |   THTE(K) |   THTV(K) |
+===========================================+=============+===========+===========+===========+==============+=============+==============+===========+===========+===========+
| (Timestamp('2020-01-01 00:00:00'), 105.0) |        1013 |      14.8 |       8.8 |        67 |         7.06 |         285 |            6 |     286.9 |     306.9 |     288.1 |
+-------------------------------------------+-------------+-----------+-----------+-----------+--------------+-------------+--------------+-----------+-----------+-----------+
| (Timestamp('2020-01-01 00:00:00'), 114.0) |        1012 |      15.8 |      11.4 |        75 |         8.43 |         286 |            6 |     288   |     311.8 |     289.4 |
+-------------------------------------------+-------------+-----------+-----------+-----------+--------------+-------------+--------------+-----------+-----------+-----------+
| (Timestamp('2020-01-01 00:00:00'), 132.0) |        1010 |      17.6 |      14.1 |        80 |        10.11 |         288 |            5 |     289.9 |     318.6 |     291.7 |
+-------------------------------------------+-------------+-----------+-----------+-----------+--------------+-------------+--------------+-----------+-----------+-----------+
| (Timestamp('2020-01-01 00:00:00'), 225.0) |        1000 |      16.8 |      14.2 |        85 |        10.28 |         300 |            4 |     289.9 |     319.1 |     291.7 |
+-------------------------------------------+-------------+-----------+-----------+-----------+--------------+-------------+--------------+-----------+-----------+-----------+
| (Timestamp('2020-01-01 00:00:00'), 294.0) |         992 |      16.2 |      13.9 |        86 |        10.16 |         319 |            3 |     290   |     318.8 |     291.8 |
+-------------------------------------------+-------------+-----------+-----------+-----------+--------------+-------------+--------------+-----------+-----------+-----------+
