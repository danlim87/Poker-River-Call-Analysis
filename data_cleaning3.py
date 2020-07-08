#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:37:00 2020

TRYING TO UTILIZE THE PS HH THIS TIME

@author: daniellim
"""

import numpy as np
import pandas as pd
import csv
import re

#https://stackoverflow.com/questions/59369684/pandas-read-files-with-blank-line-as-separator
def per_section(it, is_delimiter=lambda x: x.isspace()):
    ret = []
    for line in it:
        if is_delimiter(line):
            if ret:
                yield ' '.join(ret)
                ret = []
        else:
            ret.append(line.rstrip())
    if ret:
        yield ''.join(ret)

with open("2-5 NL HH_20200630.txt") as f:
    s = list(per_section(f))
    df = pd.DataFrame({'raw_hh':s})

with open("2-5 Zoom HH_20200630.txt") as f:
    s = list(per_section(f))
    df2 = pd.DataFrame({'raw_hh':s})
  

#FEATURE ENGINEERING
#Called river y/n, should've called river y/n, bet size, 3b pot, 4b pot, all in y/n, player position (opponent and me)
#df2.iloc[x]['raw_hh'].split('***')[-5] is river play


df2.iloc[1]['raw_hh'].split('***')[12]

#Divide street info and create separate columns
streets = ['Stack_info', 'Preflop', 'Flop', 'Turn', 'River', 'Showdown', 'Summary']
for idx, street in enumerate(streets):
    df2[street] = df2['raw_hh'].apply(lambda x: x.split('***')[idx*2])


#Fold y/n 
df2['fold y/n'] = df2['River'].apply(lambda x: 1 if 'Hero: folds' in x else 0)

#Obtaining villain position (is there a better way to write this?)
positions = ['UTG+2', 'UTG+1', 'UTG', 'Dealer', 'Big Blind', 'Small Blind']
def obtain_villain_position(hh):
    for position in positions:
        if position in hh:
            return position
df2['villain_position'] = df2['River'].apply(lambda x: obtain_villain_position(x))

positions[-5:]

def obtain_hero_position(hh):
    seat_counter = hh.count('Seat') - 1
    temp_positions = positions[-seat_counter:]
    for position in temp_positions:
        if position == 'UTG':
            if 'UTG ' not in hh:
                return position
        elif position not in hh:
            return position
df2['hero_position'] = df2['Stack_info'].apply(lambda x: obtain_hero_position(x))

#Hero OOP
df2['hero_OOP'] = df2['River'].apply(lambda x: 1 if x.split(']')[2].startswith(' Hero') else 0)
    
#If bet or raise is all in y/n
df2['all_in_y/n'] = df2['River'].apply(lambda x: 1 if 'all-in' in x else 0)

#Opponent raised river bet
df2['raised_y/n'] = df2['River'].apply(lambda x: 1 if 'raises' in x else 0)

#3b pot - count how many time "raises" appears
df2['3b_pot_y/n'] = df2['Preflop'].apply(lambda x: 1 if x.count('raises')==2 else 0)

#4b pot
df2['4b_pot_y/n'] = df2['Preflop'].apply(lambda x: 1 if x.count('raises')==3 else 0)


#River bet size calculator
def river_bet_size_calculator(hh):
'''Calculates bet size in relation to pot size'''
    #If not all in and i didn't call and i also didn't get raised
    bet = hh.split('***')[-3].split('$')[1].split()[0]
    final_pot = hh.split('***')[-3].split('$')[-1].split()[0]
    #If not all in and I called and also didn't get raised
    

#Should've folded y/n
def correct_play(hh):
    if '[ME] : Folds' in hh.split('***')[-3]:
        #Find what position I'm in
        obtain_hero_position
        hh.split('***')[-3]'[ME]'
    elif 'Mucks' in hh.split('***')[-3]:
        return 1
    elif '[ME] : Showdown' in hh.split('***')[-3]:
        return 0
    else:
        return np.nan
