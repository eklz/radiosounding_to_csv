import numpy as np 
import pandas as pd
from datetime import datetime, timedelta
import calendar
import re



import requests
from bs4 import BeautifulSoup


def get_uwyo_sounding(year, month, FROM, TO, stnm, save_csv = False ):

    url = f'http://weather.uwyo.edu/cgi-bin/sounding?region=europe&TYPE=TEXT%3ALIST&YEAR={year}&MONTH={month:02d}&FROM={FROM:04d}&TO={TO:04d}&STNM={stnm}'
    #only the STNM is usefull not the region 

    uwyo = requests.get(url)
    uwyo_soup = BeautifulSoup(uwyo.text, 'html.parser')

    data = uwyo_soup.find_all('pre') # list of each sounding between FROM and TO
    title = uwyo_soup.find_all('h2') # the title of each sounding in the form "...Observations at %HZ %d %b %Y"

    data_sounding = data[::2] # excludes Station information and sounding indices keeps only the table of mesurments
    info_sounding = data[1::2] # keeps only Station information and sounding indices

    columns_name=['PRES(hPa)', 'HGHT(m)', 'TEMP(C)', 'DWPT(C)', 'RELH(%)', 'MIXR(g/kg)', 'DRCT(deg)', 'SKNT(knot)', 'THTA(K)', 'THTE(K)', 'THTV(K)']

    result = pd.DataFrame()

    for i, table in enumerate(data_sounding):
        table = str(table).split('\n')[5:-1]  # list of lines of the table without the header and HTML tags
        table = [[float(i) if i else np.nan for i in re.split("\s{1,6}", j)[1:]]for j in table] # list(each line of the table) of list(each column) with values as float
        
        # It appends that there are no mesurments for the first lines, if it is the case then the first lines don't have the right len 
        table = [line[:11] for line in table]            
        date = re.findall("[0-9]*Z [0-9][0-9] \w* [0-9]{4}",str(title[i]))[0] # the date from the tile format = '%HZ %d %b %Y'
        date = datetime.strptime(date, '%HZ %d %b %Y')
        df = pd.DataFrame(table, columns = columns_name)
        df['DATE']=date     # convert the list to pandas DataFrame to wich a column date is added 

        result = pd.concat([result, df])
    
    result.set_index(['DATE','HGHT(m)'],  inplace = True) #DataFrame with multi index level1 date and level2 alt(m)
    if save_csv:
        result.to_csv('{stnm}_{year}{month:02d}_{FROM:04d}_{TO:04d}.csv')

    return result

    

def get_soundings_by_dates(stnm, start,stop, save_csv = False):

    '''region in {'samer': 'South America', 'europe': 'Europe', 'naconf': 'North America', 'pac': 'South Pacific',
                'nz': 'New Zealand','ant': 'Antartica', 'np': 'Artic', 'africa': 'Africa', 'seasia': 'South-East Asia',
                'mideast': 'Middle East'}
        stnm : station number
        start, stop : 'YYYYMMDDHH'
    '''
    start, stop = [datetime.strptime(_, '%Y%m%d%H') for _ in [start,stop]] # start, stop as datetime

    total_months = lambda dt: dt.month + 12 * dt.year
    tot_m = total_months(stop)-total_months(start)+1 # number of months to itterate on 

    result = pd.DataFrame()

    for i in range(tot_m):

        FROM = start
        _, day_max=calendar.monthrange(start.year, start.month)
        TO = datetime(start.year, start.month, day_max, 12)

        if TO>=stop: 
            TO = stop

        start = TO + timedelta(days=1) # change start value for next month
    
        df = get_uwyo_sounding(FROM.year, FROM.month, int(f'{FROM.day}{FROM.hour:02d}'), int(f'{TO.day}{TO.hour:02d}'), stnm, save_csv = False )
        result = pd.concat([result,df])

    if save_csv:
        result.to_csv('{stnm}__{start}_{stop}.csv')
    return result

   