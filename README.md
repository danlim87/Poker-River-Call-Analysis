# Poker-River-Call-Analysis

Results: TBD

**Goal:** Use a data-driven approach to optimize one's river calling efficiency in the game of 6-max Texas Hold-em (aka know when to hold'em and when to fold'em.) 

**Objective:** Analyze 541 instances of $2.5/$5 Zoom on Ignition poker where I was faced with river aggression between May 2020 - June 2020. 

**Why:** Capture the player pool's tendencies to maximize our EV (and our winnings).

**Application:** Essentially, poker is a business(risk and capital) where each decision point making is critical.  This analysis is going through the process of leveraging my own data (parallel: a business's data) to gain insights on how I could optimize my performance (parallel: improve KPI for a business).  This is why this dataset **not only focuses on the analysis itself, but more importantly how we use these insights to apply it to my business (poker game).**

*Note: Forking this repository will require you to provide your own hand histories, as I didn't want to have my own hand histories posted for the entire internet to see.  This will work with any PokerStars HH txt file or converting the Bovada or Ignition Poker hand history to a PokerStars HH via matt57225's excellent converter listed underneath Resources below.* 

**Skillsets demonstrated:** 
- Feature engineering: data_cleaning.py goes into extensive detail on how I filtered out relevant features just from a raw(unparsed) hand history and python code.
- Domain knowledge and its impact: feature engineering and its subsequent analysis/modeling was tremendously helpful in figuring out what features are relevant/need to be extracted). 
- Basic EDA
- Basic modeling

Caveats: 
- ***Poker is an extremely complex game against human beings in which dynamics could constantly change and therefore these varaibles are also constantly evolving.***  Therefore, it is important to note that this is an overly simplified approach - however, it still captures the overall tendencies of the player pool that attempts to capture any patterns with this rather limited sample size. 

Future Questions/Projects:
- My approach for if hero should call or not was strictly based on comparing hero and villain's hand strength.  However, **this does not capture villain's intentions**.  This is because villain could have a worse hand than ours and be value-betting (and we simply call because we do not have a hand that wants to raise but can beat some value hands), or conversely villain could be "bluffing with the best hand" where his intention was to bluff but he objectively ended up having the best hand.  The application for this in the real world setting would be analyzing hard numbers vs customer's intentions (for example). 

Lessons learned/pain points:
- Feature engineering and its difficulties. Luckily was able to scour the internet and found the "treys" library that made my life a lot easier. 
- Formulating the problem and its potential pain points and then moving forward will prove to be beneficial in the future. 

Misc.:
- Hand Histories were initially filtered from my own database via PokerTracker4.  
- The player pool at Ignition poker is anonymous where players' screennames are concealed and everyone's holecards are revealed after a 24 hour period.  This allows for analysis of whether or not hero(denoting the player in question) should've called or folded (aka our target variable).

## Resources
https://github.com/matt57225/bovada-hand-history-converter

https://github.com/worldveil/deuces

https://github.com/ihendley/treys
