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

from treys import Card
from treys import Evaluator

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
        return round(river_agg / (final_pot - river_agg * 2) * 100, 1)
    #I fold
    elif hh['fold y/n'] == 1:
        return round(river_agg / final_pot * 100, 1)

df2['river_bet_size_percentage'] = df2.apply(lambda x: river_bet_size_calculator(x), axis=1)

#River bet% is predefined (25, 50, 75, 100, 125, etc.)
df2['river_bet_predefined_y/n'] = df2.apply(lambda x: 1 if x['river_bet_size_percentage'] in [50, 75, 100] else 0, axis =1)

#River bet itself is increments of 5
df2['river_bet_int_y/n'] = df2.apply(lambda x: 1 if river_bet_raise(x['River']) % 5 == 0 else 0, axis=1)

#Should've folded y/n
def hero_hole_cards(hh_preflop):
    #Returns a list which contains the integer representation of two hole cards belonging to hero based on treys library. 
    hole_cards = []
    hole_cards.append(Card.new(hh_preflop.split('Dealt to Hero ')[1].split()[0][1:]))
    hole_cards.append(Card.new(hh_preflop.split('Dealt to Hero ')[1].split()[1][:-1]))
    return hole_cards

def villain_hole_cards(hh_showdown, hh_river):
    #Returns a list which contains the integer representation of two hole cards belonging to villain based on treys library. 
    hole_cards = []
    hole_cards.append(Card.new(hh_showdown.split(obtain_villain_position(hh_river) + ': shows ')[1].split()[0][1:]))
    hole_cards.append(Card.new(hh_showdown.split(obtain_villain_position(hh_river) + ': shows ')[1].split()[1][:-1]))
    return hole_cards


def community_board(hh_summary):
    board = []
    for i in range(0, 14, 3):
        board.append(Card.new(hh_summary.split('Board [')[1][i:i+2]))
    return board

def should_call(hh):
    #Strictly whether or not I should've called or not (but not necessarily the information I want). 
    #According to the treys library, score = rank ranging from 1(royal flush) to 7xxx(nut low).  Therefore the lower score (ex. rank 1) will beat the higher score (ex. rank 7xxx)
    evaluator = Evaluator()
    hero_score = evaluator.evaluate(community_board(hh['Summary']), hero_hole_cards(hh['Preflop']))
    villain_score = evaluator.evaluate(community_board(hh['Summary']), villain_hole_cards(hh['Showdown'], hh['River']))
    if villain_score > hero_score:
        return 1
    else:
        return 0
   
df2['should_call'] = df2.apply(lambda x: should_call(x), axis=1)


Card.int_to_str(hero_hole_cards(df2.iloc[0]['Preflop'])[0])



def villain_bluffing(hh):
    #An attempt to figure out whether my opponent was bluffing or not.  This is more of a nuanced approach
    '''Some possible solutions:
        The most important: If he's not utilizing any of his hole cards to make best hand: probably bluffing'
        If there is 5 to a straight or 5 to a flush on the board and he's betting: probably bluffing'
        Bluff freq. increases if there is 4 to a straight or 4 to a flush out on the board (unless he makes a flush with his hand)
        If there is two pair on the board and he bets his "two pair" could be for value (if it's ace high')
        Anytime the board equals his hand = bluff?
        If no flush or straight possible on board, and he bets > pair probably for value.  
