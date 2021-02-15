# Radiosounding to CSV

This code is aimed at creating a CSV file or a Pandas DataFrame of **atmospheric sounding datas**. it takes as inputs a time period as well as a station number. 

It works by scrapping the data available on the website of the Wyoming University (http://weather.uwyo.edu/upperair/sounding.html). 

## Get a list of available station : 

The code *get_uwyo_station_list.py* is a slightly modify version of the mercury code : https://github.com/vlouf/mercury; It prints the list of available station sorted by continents : 
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
