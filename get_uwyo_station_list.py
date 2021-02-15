"""
.. module:: mercury
   :platform: Unix, Windows
   :synopsis: Retrieves radiosounding data for a specified station (e.g. YPDN
              for Darwin) at specified dates.

.. moduleauthor:: Valentin Louf <valentin.louf@bom.gov.au>


"""

import re
import os
import pickle
import string
import pandas
import datetime
import urllib.request

from bs4 import BeautifulSoup
from multiprocessing import Pool


def station_list():
    """
    List all available stations and their id number.
    """

    maps = ['samer', 'europe', 'naconf', 'pac', 'nz', 'ant', 'np',
            'africa', 'seasia', 'mideast']

    desc = {'samer': 'South America',
            'europe': 'Europe',
            'naconf': 'North America',
            'pac': 'South Pacific',
            'nz': 'New Zealand',
            'ant': 'Antartica',
            'np': 'Artic',
            'africa': 'Africa',
            'seasia': 'South-East Asia',
            'mideast': 'Middle East'}

    for suffix in maps:
        url = "http://weather.uwyo.edu/upperair/%s.html" % (suffix)
        with urllib.request.urlopen(url) as f:
            content = f.read()
        soup = BeautifulSoup(content, "html.parser")

        st_id = []
        st_nm = []

        print(desc[suffix] + ":\n")
        print("\t\tStation id - Station name")

        for ar in soup.find_all('area'):
            try :
                st = ar.get('title')
                rgm = re.findall("[0-9]+", st)
                dgm = re.split("[0-9]+", st)
                try:
                    st_nm.append(dgm[1][2:-2])
                    st_id.append(rgm[0] )
                    print("\t\t%s - %s" % (rgm[0], dgm[1][2:]))
                except IndexError:
                    break
            except TypeError:
                break 

        print("\n")

    return None
