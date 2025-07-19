# Poker Odds Calculation Program

# Function that calculates the percentage chance (odds) of getting every possible poker hand given the currently held cards and the state of the cards on the table. Uses standard Texas Hold'em hands.
# Takes the following parameters:
# - Hole (list of the current two 'hole' cards the 'player' is has been dealt)
# - Community (list of the currently dealt 'community' cards on the table, can be 0, 3, 4 or 5 cards)
# Returns the following:
# - A list of hand types and their corresponding probabilities, in order of strongest to weakest hands (note: will only display the strongest hand if 100% probability)

import itertools
from collections import Counter
import random

from hand_eval import handEval

'''Define key values for the program'''
RANKS = "23456789TJQKA"
RANK_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
SUITS = "DCHS"
DECK = [r + s for r in RANKS for s in SUITS]
HAND_STRENGTH = { # Ranking value for hand strengths - value is mostly based on Balatro chip scores :)
    "Royal Flush": 100,
    "Straight Flush": 90,
    "Four of a Kind": 60,
    "Full House": 40,
    "Flush": 35,
    "Straight": 30,
    "Three of a Kind": 25,
    "Two Pair": 20,
    "Pair": 10,
    "High Card": 5
}
SAMPLE_SIZE = 10000 # Number of random samples used to approximate probability

'''Card object converter'''
def card(cardStr: str):
    return {'rank': cardStr[0], 'suit': cardStr[1]}

'''Poker odds calculator'''
def calcOdds(hole: list[dict], community: list[dict]):
    
    # Add community cards to the hole (as they are counted as part of the player's 'hand')
    hole = hole + community
    
    # Count occurrences of each hand type
    handCount = Counter()

    # If all 5 community cards are dealt, evaluate best hand from the current cards
    if len(community) == 5:
        # Loop through every 5-card combination within the current hand, and select the best combination according to handEval
        best5Hand = max(itertools.combinations(hole, 5), key=lambda x: handEval(list(x)))
        # Evaluates the best hand type from that combination
        eval = handEval(best5Hand)
        # Increments that hand type count
        handCount[eval[1]] += 1

    # If some community cards have yet to be dealt, simulate the possible completions
    else:
        # Remove hole cards from the deck
        remainingDeck = [card for card in DECK if card not in hole]
        # Count the number of remaining community cards to be dealt
        numRemainingCards = 5 - len(community)

        # If there are < 3 community cards, use sampling to approximate probabilities and reduce the number of calculations run
        if len(community) < 3:
            sampledBoards = random.sample(list(itertools.combinations(remainingDeck, numRemainingCards)), SAMPLE_SIZE)

        # Else loop through every possible combination of cards that can be dealt from the remaining deck - the number of cards that can be in the combination is (numRemainingCards)
        else:
            sampledBoards = itertools.combinations(remainingDeck, numRemainingCards)

        for remainingCards in sampledBoards:
            # Convert remainingCards into a list of card objects
            remainingCards = [card(c) for c in remainingCards]
            # Create a hand from the hole (+ community) cards and the remaining cards in the deck
            hand = hole + remainingCards
            # Choose the best 5 cards from the hand (making the strongest hand) to evaluate
            best5Hand = max(itertools.combinations(hand, 5), key=lambda x: handEval(list(x)))
            # Re-evaluates that combination to produce the hand type
            eval = handEval(best5Hand)
            handCount[eval[1]] += 1

    # Get the total number of counted hands
    possibleCombinations = sum(handCount.values())

    # If there was no samplng used, calculate probabilities as normal
    if len(community) >= 3:
        probabilities = {hand: count / possibleCombinations for hand, count in handCount.items()} # Probability = counted hands / total number of counted hands

    # If sampling was used, use Laplace Smoothing (+1 to every count) to avoid zero probabilities
    else:
        possibleCombinations = sum(handCount.values()) + len(HAND_STRENGTH) # Adjust the total count to add an extra hand of every type
        probabilities = {hand: (count + 1) / possibleCombinations for hand, count in handCount.items()} # Add +1 to the count of each observed hand

        # Ensures all hand types are included in probabilities even if unobserved
        for handType in HAND_STRENGTH:
            if handType not in probabilities:
                probabilities[handType] = 1 / possibleCombinations # Add the unobserved hand type and assign a small probability to it

    # Sort the probabilities by hand strength
    sortedProbabilities = dict(sorted(probabilities.items(), key=lambda x: -HAND_STRENGTH[x[0]]))

    return sortedProbabilities

'''Main function - asks for 'hole' and 'community' user input then runs the calculations'''
def main():
    # Display calculator intro and card terms
    print("\nPoker Hand Odds Calculator - Developed by Aaron Wang")
    print("Card Ranks:", RANKS)
    print("Card Suits:", SUITS)

    # Function for checking for valid card input
    def validateCards(input, expectedCountSet):
        cards = input.upper().split()

        if not all(len(c) == 2 and c[0] in RANKS and c[1] in SUITS for c in cards): # Invalid card format
            return
        if len(cards) != len(set(cards)): # Duplicate cards input
            return
        if len(cards) not in expectedCountSet: # Invalid number of cards
            return
        
        return [card(c) for c in cards]
    
    # Asks for user input for valid hole cards
    while True:
        holeInput = input("\nEnter your hole cards (e.g. 'AS TH' for Ace of Spades and 10 of Hearts): ")
        hole = validateCards(holeInput, {2})
        if hole:
            break
        print("Invalid hole card input - enter 2 valid hole cards")

    # Asks for user input for valid community cards
    while True:
        communityInput = input("\nEnter community cards (leave blank if none): ")
        if not communityInput:
            community = []
            break
        community = validateCards(communityInput, set(range(0, 6)))
        if community:
            break
        print("Invalid community card input - enter 0-5 valid hole cards")

    # Calculate the poker hand odds
    probabilities = calcOdds(hole, community)

    # Print probabilities
    print("\nHand Probabilities:")
    for handType, probability in probabilities.items():
        print(f"{handType}: {probability * 100:.2f}%")

# Run the main calculator program when file is executed
if __name__ == "__main__":
    main()
