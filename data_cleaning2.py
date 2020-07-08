#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 14:30:25 2020

@author: daniellim
"""


import numpy as np
import pandas as pd
import csv

#https://stackoverflow.com/questions/59369684/pandas-read-files-with-blank-line-as-separator
def per_section(it, is_delimiter=lambda x: x.isspace()):
    ret = []
    for line in it:
        if is_delimiter(line):
            if ret:
                yield ''.join(ret)
                ret = []
        else:
            ret.append(line.rstrip())
    if ret:
        yield ''.join(ret)

with open("2-5 NL HH_20200630.txt") as f:
    s = list(per_section(f))
    df = pd.DataFrame({'data':s})

with open("2-5 Zoom HH_20200630.txt") as f:
    s = list(per_section(f))
    df2 = pd.DataFrame({'data':s})
    
from poker.room.pokerstars import PokerStarsHandHistory
hh0 = PokerStarsHandHistory(df.iloc[0]['data'])
hh0.parse()


hh = PokerStarsHandHistory.from_file("2-5 Zoom HH_20200630.txt")
hh.parse()
hh.players
hh._parse_button()
hh._parse_winners()
