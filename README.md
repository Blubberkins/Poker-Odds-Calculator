# Poker Odds Calculator

This program calculates the exact percentage chance (odds) of being dealt every possible poker hand given the currently dealt cards for the player and the table, listed from strongest to weakest.
Uses standard Texas Hold'em hands, and excludes any hands which cannot be made using the given cards.
The intention of the program is to be used in a practical scenario by a Poker player to calculate the exact odds of the possible hands they can be dealt in real time, informing their decisions in the game.

## How to use

Run the 'poker_odds_calc.py' file to execute the main program.

The program takes the following parameters:
- Hole (list of the current two 'hole' cards the player has been dealt - the exact card input format is detailed within the program)
- Community (list of the currently dealt 'community' cards on the table, can be 0, 3, 4 or 5 cards)

and returns the following:
- A list of hand types and their corresponding probabilities in order of strongest to weakest hands, excluding hand types which cannot be made or are weaker than the strongest hand already dealt

Run the 'poker_odds_calc_test.py' file to execute the Pytest testing suite.

## File structure

- poker_odds_calc.py: main file where the calculator program is located
- poker_odds_calc_test.py - test file which contains 12 different test cases for robustness
- hand_eval.py: helper file containing a function which evaluates the strength of a given 5-card hand in poker

## Detailed explanation of implementation

The program uses a simulation-based approach to exhaustively enumerate through every possible combination of hands that could be dealt to the player, combined with a hand evaluation function which picks the strongest hand from each combination. 
This method tallies the strongest hands from every simulated combination and divides by the total number of combinations to give the exact probability of getting every hand type, displayed from strongest possible hand to the weakest currently dealt hand.
The simulation method was chosen over the combinatorial mathematical one due to its simpler implementation, while maintaining the same 100% accuracy in results. However when processing extremely large numbers of simulations, such as when there are no community cards dealt (2,598,960 simulations!), the program does take an excessive amount of time to process, due to processing time needed to evaluate the strength of every single simulated 5-card combination. To resolve this issue, the Monte Carlo simulation apporach is used for 0-2 community card situations, randomly sampling up to a certain limit of simulations (currently chosen as 10,000). This massively reduces the processing time of the program for large simulation cases, keeping it at an O(1) time complexity with an observed < 0.5 second runtime, while maintaining relatively high accuracy. Using sampling also runs the risk of not encountering extremely rare hands such as the Royal/Straight Flush when tallying simulations, and the function accounts for this by using Laplace smoothing to add at least a single instance of every hand to the tally count.

The hand evaluator file is used as a helper function for the main calculator when evaluating the strength of each simulated 5-card combination. At times when more than 5 cards need to be evaluated by this function (eg. 2 hole cards + 5 unknown community cards), the best 5-card combination from that hand is chosen to be evaluated. This is done by using the same function to rank every 5-card combination within that 5+ card simulation, and choosing the one ranked highest from them.
The evaluator function itself works by following this process:
- Give each card rank an internal numerical 'strength' value
- Count the ranks and suits of the cards
- Identify special poker hand combinations (flush, straight) by checking the rank and suit counts, including the unique Ace-low straight (Ace, 2, 3, 4, 5)
- Identify other poker hand combinations by sorting rank counts in descending order
- Evaluate the best hand category by progressively checking each hand condition from strongest to weakest, and return it