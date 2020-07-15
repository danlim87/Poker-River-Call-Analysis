#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:37:00 2020

Filtered for river aggression faced in HU pots, 2/5NL zoom

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
def obtain_villain_position(hh_river):
    for position in positions:
        if position in hh_river:
            return position
df2['villain_position'] = df2['River'].apply(lambda x: obtain_villain_position(x))


#Obtain Hero position
def obtain_hero_position(hh_stackinfo):
    seat_counter = hh_stackinfo.count('Seat') - 1
    temp_positions = positions[-seat_counter:]
    for position in temp_positions:
        if position == 'UTG':
            if 'UTG ' not in hh_stackinfo:
                return position
        elif position not in hh_stackinfo:
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


#River percentage calculator
def calculate_player_chips_vested(hh):
    '''Calculates how many chips hero put into pot before river aggression
    Using hero's stack to calcualte this but by rules of the game villain also has to put the same amount'''
    streets = ['Stack_info', 'Preflop', 'Flop', 'Turn']
    player_chips = 0
    for street in streets:
        hero_counter = hh[street].count('Hero: ')
        temp_list = hh[street].split('Hero: ')
        for i in range(1, hero_counter+1):
            if hh[street].split('Hero: ')[i].split()[0] == 'checks':
                continue
            elif (hh[street].split('Hero: ')[i].split()[0] == 'raises') or (hh[street].split('Hero: ')[i].split()[0] == 'posts'):
                player_chips += float(hh[street].split('Hero: ')[i].split()[3][1:])
            else:
                player_chips += float(hh[street].split('Hero: ')[i].split()[1][1:])
    return player_chips

def calculate_hero_starting_stack(hh_stackinfo):
    return float(hh_stackinfo.split('Hero ($')[1].split(' ')[0])

def calculate_villain_starting_stack(hh_stackinfo, hh_river):
    return float(hh_stackinfo.split(obtain_villain_position(hh_river) + ' ($')[1].split(' ')[0]) 

def river_bet_raise(hh_river):
    '''Returns villain's bet or raise on river'''
    try:
        return float(hh_river.split(obtain_villain_position(hh_river) + ': bets $')[1].split(' ')[0])
    except:
        return float(hh_river.split(obtain_villain_position(hh_river) + ': raises $')[1].split(' ')[0])

'''#Debugging:
for i in range(541):
    river_bet_raise(df2.iloc[i]['River'])
    print('iteration ' + str(i) + ' successful')'''

def final_pot_calculator(hh_showdown):
    '''Returns final pot of hand history'''
    if hh_showdown.count('collected') > 1: #Accounts for chopped pots
        return float(hh_showdown.split('collected $')[-1].split(' ')[0])*2
    else:
        return float(hh_showdown.split('collected $')[-1].split(' ')[0])

def river_bet_size_calculator(hh):
    '''Calculates bet size in relation to pot size
    My method is to work backwards from final pot
    Also accounts for effective size'''
    hero_starting_stack = calculate_hero_starting_stack(hh['Stack_info'])
    villain_starting_stack = calculate_villain_starting_stack(hh['Stack_info'], hh['River'])
    villain_position = obtain_villain_position(hh['River'])
    river_agg = river_bet_raise(hh['River'])
    final_pot = final_pot_calculator(hh['Showdown'])
    eff_river_stacks = hero_starting_stack - calculate_player_chips_vested(hh)
    #Account for effective river bet
    if villain_starting_stack > hero_starting_stack:
        if river_agg > eff_river_stacks:
            river_agg = eff_river_stacks
    #I call
    if hh['fold y/n'] == 0:
        return round(river_agg / (final_pot - river_agg * 2) * 100, 2)
    #I fold
    elif hh['fold y/n'] == 1:
        return round(river_agg / final_pot * 100, 2)

df2['river_bet_size_percentage'] = df2.apply(lambda x: river_bet_size_calculator(x), axis=1)

#River bet% is predefined (25, 50, 75, 100, 125, etc.)
df2['river_bet_predefined_y/n'] = 
    
#River bet itself is rounded (int)
df2['river_bet_int_y/n'] = 

#Should've folded y/n
def hero_hole_cards(hh_preflop):
    return ' '.join(hh_preflop.split('Dealt to Hero ')[1].split()[0:2])
    
def villain_hole_cards(hh_showdown, hh_river):
    ' '.join(hh_showdown.split(obtain_villain_position(hh_river) + ': shows ')[1].split()[0:2])

def winner(hero, villain):
    

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
