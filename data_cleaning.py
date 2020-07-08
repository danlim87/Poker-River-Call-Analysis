#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 11:53:49 2020

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

with open("2-5 NL HH.txt") as f:
    s = list(per_section(f))
    df = pd.DataFrame({'data':s})

with open("2-5 Zoom HH.txt") as f:
    s = list(per_section(f))
    df2 = pd.DataFrame({'data':s})
  

#FEATURE ENGINEERING
#Called river y/n, should've called river y/n, bet size, 3b pot, 4b pot, all in y/n, player position (opponent and me)

#Fold y/n
def folded_river(hh):
    #Determines whether or not hero folds river
    if '[ME] : Folds' in hh.split('***')[-3]:
        return 1
    else:
        return 0
    
df2['fold y/n'] = df2['data'].apply(folded_river)


#df2['data'].iloc[1].split('  [ME]')[-2].split(')')[-1:][0]

positions = ['UTG', 'UTG+1', 'UTG+2', 'Big Blind', 'Small Blind', 'Dealer']

#Obtaining hero position
def obtain_hero_position(hh):
    temp = hh.split('  [ME]')[-2].split(')')[-1:][0]
    temp2 = temp
    i = 0
    while temp2 not in positions: 
        i -= 1
        temp2 = temp[-i:]
    return temp2

df2['hero_position'] = df2['data'].apply(obtain_hero_position)

#Obtaining villain position
def obtain_villain_position(hh):
    
    
df2['data'].iloc[0].split('***')[-3]



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


def river_bet_size_calculator(hh):
    '''Calculates pot for an Ignition Poker HH'''
    if 'Does not show' in hh.split('***')[-3]:
        
            Return uncalled portion of bet x
            pot = Hand result x
            return bet/result
    elif 'Mucks' in hh.split('***')[-3]:
        -> Then retrieve contents of
            Calls X
            pot = Hand result - 2 * X
    elif 'Calls' in :
    elif 'All-in'









