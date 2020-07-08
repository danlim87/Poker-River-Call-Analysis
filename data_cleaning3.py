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
#Divide streets and create separate columns
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
    
#If river bet or raise is all in y/n
df2['all_in_y/n'] = df2['River'].apply(lambda x: 1 if 'all-in' in x else 0)

#Opponent raised river bet
df2['raised_y/n'] = df2['River'].apply(lambda x: 1 if 'raises' in x else 0)

#3b pot - count how many time "raises" appears
df2['3b_pot_y/n'] = df2['Preflop'].apply(lambda x: 1 if x.count('raises')==2 else 0)

#4b pot
df2['4b_pot_y/n'] = df2['Preflop'].apply(lambda x: 1 if x.count('raises')==3 else 0)

df2[(df2['fold y/n'] ==0) & (df2['raised_y/n'] == 0) & (df2['all_in_y/n'] == 0)]






float(df2.iloc[0]['Stack_info'].split('Hero ($')[1].split(' ')[0])

df2.iloc[1]['Turn'].split('Hero: ')[2].split(' ')[1][1:]
df2.iloc[6]['Preflop']

def calculate_hero_chips_vested(hh):
    '''Calculates how many chips hero put into pot before river aggression'''
    streets = ['Stack_info', 'Preflop', 'Flop', 'Turn']
    hero_chips = 0
    for street in streets:
        hero_counter = hh[street].count('Hero: ')
        temp_list = hh[street].split('Hero: ')
        for i in range(1, hero_counter+1):
            if hh[street].split('Hero: ')[i].split()[0] == 'checks':
                continue
            elif (hh[street].split('Hero: ')[i].split()[0] == 'raises') or (hh[street].split('Hero: ')[i].split()[0] == 'posts'):
                hero_chips += float(hh[street].split('Hero: ')[i].split()[3][1:])
            else:
                hero_chips += float(hh[street].split('Hero: ')[i].split()[1][1:])
    return hero_chips


#River bet size calculator
def river_bet_size_calculator(hh):
    '''Calculates bet size in relation to pot size
    There are many different scenarios, which will vary how I retrieve/calculate this info
    I will be listing those scenarios in the comment'''
    #Calculate hero's remaining stack by river
    hero_starting_stack = float(df2.iloc[0]['Stack_info'].split('Hero ($')[1].split(' ')[0]) 
    villain_position = obtain_villain_position(hh['River'])
    villain_starting_stack = float(df2.iloc[0]['Stack_info'].split(villain_position + ' ($')[1].split(' ')[0]) 
    #I call, Not all in, not raised
    if villain_starting_stack > hero_starting_stack:
        #Some code
    else:
        river_bet = float(hh['River'].split(villain_position + ': bets $')[-1].split(' ')[0])
        final_pot = float(hh['Showdown'].split('collected $')[-1].split(' ')[0])
        if hh['fold y/n'] == 0 and hh['raised_y/n'] == 0:
            return river_bet / (final_pot - river_bet * 2) * 100
        elif hh['fold y/n'] == 1 and hh['raised_y/n'] == 0:
            return river_bet / (final_pot - river_bet) * 100
        elif hh['fold y/n'] == 1 and hh['raised_y/n'] == 1:
            return 

    

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
