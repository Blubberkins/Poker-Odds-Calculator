# Poker Hand Strength Evaluator

# Function that determines the best hand category for a given 5-card combination
# Takes the following parameter:
# - Hand (a list of 'Card' dictionary types, which each contain a rank and suit)
# Returns the following:
# - A tuple containing the ranking value of the strongest possible hand, its name, and the ranking value of its cards (which is used for tiebreakers between the same type of hands)

from collections import Counter

RANK_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def handEval(hand: list[dict]):
    # Extract ranks and suits from 5-card hand
    ranks = [card['rank'] for card in hand] # eg. {'A', 'K', 'Q'}
    suits = [card['suit'] for card in hand] # eg. {D, C}

    # Convert extracted ranks into their numerical values, sorted by descending order
    rankVals = sorted([RANK_VALUES[rank] for rank in ranks], reverse=True) # eg. [14, 13, 12, 11, 10]

    # Identify special case of Ace-low straight
    if set(rankVals) == {14, 5, 4, 3, 2}:
        rankVals = [5, 4, 3, 2, 1] # count the Ace as a 1 in value

    # Count the number of ranks and suits in the hand
    rankCount = Counter(ranks) # eg. {'A': 2, 'K': 2, 'Q': 1}
    suitCount = Counter(suits) # eg. {'D': 3, 'C': 2}

    # Identify special poker hands
    isFlush = max(suitCount.values()) == 5 # every suit in the hand is the same (totalling 5 counts of the same suit)
    isStraight = (len(rankCount) == 5 and max(rankVals) - min(rankVals) == 4) # there are 5 different consecutive card ranks in the hand

    # Identify 4/3/2 card combos by sorting the rank counts in descending order
    sortedRankCount = sorted(rankCount.values(), reverse=True)

    # Evaluate the best hand category for the given hand, and return a tuple (ranking value, hand name, rankVals), rankVals is used for tiebreakers
    if isStraight and isFlush:
        return (100 if rankVals[0] == 14 else 90, "Royal Flush" if rankVals[0] == 14 else "Straight Flush", rankVals) # Royal Flush if highest rank is Ace, otherwise Straight Flush
    elif sortedRankCount == [4, 1]:
        return (60, "Four of a Kind", rankVals)
    elif sortedRankCount == [3, 2]:
        return (40, "Full House", rankVals)
    elif isFlush:
        return (35, "Flush", rankVals)
    elif isStraight:
        return (30, "Straight", rankVals)
    elif sortedRankCount == [3, 1, 1]:
        return (25, "Three of a Kind", rankVals)
    elif sortedRankCount == [2, 2, 1]:
        return (20, "Two Pair", rankVals)
    elif sortedRankCount == [2, 1, 1, 1]:
        return (10, "Pair", rankVals)
    else:
        return (5, "High Card", rankVals)