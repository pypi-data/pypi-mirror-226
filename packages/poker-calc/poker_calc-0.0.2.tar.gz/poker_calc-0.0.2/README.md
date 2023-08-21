# Poker Odds Calculator

## Calculate your hand odds against other players. 

For instructions run:
```bash 
poker_calc 
```
or 
```bash
poker_calc --help
```
You can easily give from 2-9 players.
if no -b argument is present then Pre-Flop odds are calculated.
Else if -b is 5 cards then it will simply give you who has the strongest hand (winner)
else if -b is between 3-4 cards then flop odds and respecetivly turn odds will be calculated.
After that you can either run arg mode version:
```bash
poker_calc -p 8s9s -p ThQd -b 8h9sJh --fast
```
Or you could try interactive mode (with limitations- 2 players only and board cards are mandatory)
```bash
poker_calc --interactive
```
