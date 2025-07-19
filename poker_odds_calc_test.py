# Poker Odds Calculator Testing Suite

import unittest

from poker_odds_calc import card, handEval

class TestFunction(unittest.TestCase):

    '''Test card creation'''
    def test_card(self):
        c = card("AS")
        self.assertEqual(c, {"rank": "A", "suit": "S"})

    '''Test poker hand evaluator'''
    def test_handEvalALS(self): # Test Ace-low straight
        hand = [{'rank': "A", 'suit': "S"}, {'rank': "2", 'suit': "S"}, {'rank': "3", 'suit': "S"}, {'rank': "4", 'suit': "S"}, {'rank': "5", 'suit': "D"}]
        expected_output = (30, "Straight", [5, 4, 3, 2, 1])
        self.assertEqual(handEval(hand), expected_output)

    def test_handEvalRF(self): # Test royal flush
        hand = [{'rank': "A", 'suit': "S"}, {'rank': "K", 'suit': "S"}, {'rank': "Q", 'suit': "S"}, {'rank': "J", 'suit': "S"}, {'rank': "T", 'suit': "S"}]
        expected_output = (100, "Royal Flush", [14, 13, 12, 11, 10])
        self.assertEqual(handEval(hand), expected_output)

    def test_handEvalSF(self): # Test straight flush
        hand = [{'rank': "9", 'suit': "S"}, {'rank': "K", 'suit': "S"}, {'rank': "Q", 'suit': "S"}, {'rank': "J", 'suit': "S"}, {'rank': "T", 'suit': "S"}]
        expected_output = (90, "Straight Flush", [13, 12, 11, 10, 9])
        self.assertEqual(handEval(hand), expected_output)

    def test_handEvalFour(self): # Test four of a kind
        hand = [{'rank': "9", 'suit': "S"}, {'rank': "9", 'suit': "H"}, {'rank': "9", 'suit': "C"}, {'rank': "9", 'suit': "D"}, {'rank': "2", 'suit': "S"}]
        expected_output = (60, "Four of a Kind", [9, 9, 9, 9, 2])
        self.assertEqual(handEval(hand), expected_output)

    def test_handEvalFH(self): # Test full house
        hand = [{'rank': "9", 'suit': "S"}, {'rank': "9", 'suit': "H"}, {'rank': "9", 'suit': "C"}, {'rank': "8", 'suit': "D"}, {'rank': "8", 'suit': "S"}]
        expected_output = (40, "Full House", [9, 9, 9, 8, 8])
        self.assertEqual(handEval(hand), expected_output)

    def test_handEvalFlush(self): # Test flush
        hand = [{'rank': "9", 'suit': "S"}, {'rank': "8", 'suit': "S"}, {'rank': "7", 'suit': "S"}, {'rank': "6", 'suit': "S"}, {'rank': "4", 'suit': "S"}]
        expected_output = (35, "Flush", [9, 8, 7, 6, 4])
        self.assertEqual(handEval(hand), expected_output)

    def test_handEvalStraight(self): # Test straight
        hand = [{'rank': "9", 'suit': "S"}, {'rank': "8", 'suit': "S"}, {'rank': "7", 'suit': "S"}, {'rank': "6", 'suit': "S"}, {'rank': "5", 'suit': "D"}]
        expected_output = (30, "Straight", [9, 8, 7, 6, 5])
        self.assertEqual(handEval(hand), expected_output)

    def test_handEvalThree(self): # Test three of a kind
        hand = [{'rank': "9", 'suit': "S"}, {'rank': "9", 'suit': "H"}, {'rank': "9", 'suit': "C"}, {'rank': "6", 'suit': "S"}, {'rank': "5", 'suit': "D"}]
        expected_output = (25, "Three of a Kind", [9, 9, 9, 6, 5])
        self.assertEqual(handEval(hand), expected_output)

    def test_handEvalTP(self): # Test two pair
        hand = [{'rank': "9", 'suit': "S"}, {'rank': "9", 'suit': "H"}, {'rank': "6", 'suit': "C"}, {'rank': "6", 'suit': "S"}, {'rank': "5", 'suit': "D"}]
        expected_output = (20, "Two Pair", [9, 9, 6, 6, 5])
        self.assertEqual(handEval(hand), expected_output)

    def test_handEvalPair(self): # Test pair
        hand = [{'rank': "9", 'suit': "S"}, {'rank': "9", 'suit': "H"}, {'rank': "7", 'suit': "C"}, {'rank': "6", 'suit': "S"}, {'rank': "5", 'suit': "D"}]
        expected_output = (10, "Pair", [9, 9, 7, 6, 5])
        self.assertEqual(handEval(hand), expected_output)

    def test_handEvalHigh(self): # Test high card
        hand = [{'rank': "9", 'suit': "S"}, {'rank': "8", 'suit': "H"}, {'rank': "7", 'suit': "C"}, {'rank': "6", 'suit': "S"}, {'rank': "4", 'suit': "D"}]
        expected_output = (5, "High Card", [9, 8, 7, 6, 4])
        self.assertEqual(handEval(hand), expected_output)

# Run testing suite and then the main program when file is executed
if __name__ == "__main__":
    unittest.main()