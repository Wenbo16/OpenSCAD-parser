from parsing import Earley_Parser, findRoot
import unittest
import numpy as np
# Get the token map from the lexer.  This is required.
# Test it out

class Test_Tokenization(unittest.TestCase):
    def test_Earley_algorithm(self):
        grammar1= {
            "nonterminals" : [ "Start", "S", "NP", "VP", "prep", "N", "Adj" ,"Aux", "V"],
            "terminals" : set([ "the", "large", "can","hold", "water"]),
            "start" : "Start",
            "rules" : {
                        "Start" : ("S"),
                        "S" : ("NP VP",),
                        "NP" : ("prep Adj N", "prep N", "Adj N"),
                        "VP" : ("Aux VP", "V NP"),
                        "prep" : ("the",),
                        "Adj" : ("large",),
                        "N" : ("can", "water"),
                        "Aux" : ("can",),
                        "V" : ("can", "hold", "water"),
                      }
        }

        s1 = 'the large can can hold the water'
        input1 = s1.split(" ")
        expected1 =  [[('Start', 'S', 0, 0, ()), ('S', 'NP VP', 0, 0, ()), ('NP', 'prep Adj N', 0, 0, ()), ('NP', 'prep N', 0, 0, ()), ('NP', 'Adj N', 0, 0, ()), ('prep', 'the', 0, 0, ()), ('Adj', 'large', 0, 0, ())],
                     [('prep', 'the', 1, 0, ()), ('NP', 'prep Adj N', 1, 0, ((1, 0),)), ('NP', 'prep N', 1, 0, ((1, 0),)), ('Adj', 'large', 0, 1, ()), ('N', 'can', 0, 1, ()), ('N', 'water', 0, 1, ())],
                     [('Adj', 'large', 1, 1, ()), ('NP', 'prep Adj N', 2, 0, ((1, 0), (2, 0))), ('N', 'can', 0, 2, ()), ('N', 'water', 0, 2, ())],
                     [('N', 'can', 1, 2, ()), ('NP', 'prep Adj N', 3, 0, ((1, 0), (2, 0), (3, 0))), ('S', 'NP VP', 1, 0, ((3, 1),)), ('VP', 'Aux VP', 0, 3, ()), ('VP', 'V NP', 0, 3, ()), ('Aux', 'can', 0, 3, ()), ('V', 'can', 0, 3, ()), ('V', 'hold', 0, 3, ()), ('V', 'water', 0, 3, ())],
                     [('Aux', 'can', 1, 3, ()), ('V', 'can', 1, 3, ()), ('VP', 'Aux VP', 1, 3, ((4, 0),)), ('VP', 'V NP', 1, 3, ((4, 1),)), ('VP', 'Aux VP', 0, 4, ()), ('VP', 'V NP', 0, 4, ()), ('NP', 'prep Adj N', 0, 4, ()), ('NP', 'prep N', 0, 4, ()), ('NP', 'Adj N', 0, 4, ()), ('Aux', 'can', 0, 4, ()), ('V', 'can', 0, 4, ()), ('V', 'hold', 0, 4, ()), ('V', 'water', 0, 4, ()), ('prep', 'the', 0, 4, ()), ('Adj', 'large', 0, 4, ())],
                     [('V', 'hold', 1, 4, ()), ('VP', 'V NP', 1, 4, ((5, 0),)), ('NP', 'prep Adj N', 0, 5, ()), ('NP', 'prep N', 0, 5, ()), ('NP', 'Adj N', 0, 5, ()), ('prep', 'the', 0, 5, ()), ('Adj', 'large', 0, 5, ())],
                     [('prep', 'the', 1, 5, ()), ('NP', 'prep Adj N', 1, 5, ((6, 0),)), ('NP', 'prep N', 1, 5, ((6, 0),)), ('Adj', 'large', 0, 6, ()), ('N', 'can', 0, 6, ()), ('N', 'water', 0, 6, ())],
                     [('N', 'water', 1, 6, ()), ('NP', 'prep N', 2, 5, ((6, 0), (7, 0))), ('VP', 'V NP', 2, 4, ((5, 0), (7, 1))), ('VP', 'Aux VP', 2, 3, ((4, 0), (7, 2))), ('S', 'NP VP', 2, 0, ((3, 1), (7, 3))), ('Start', 'S', 1, 0, ((7, 4),))]]
        chart1 = Earley_Parser(grammar1, input1)
        self.assertEqual(chart1.tolist(), expected1)


        grammar2 = {
            "nonterminals" : [ "P", "S", "M", "T"],
            "terminals" : [ "1", "2", "3","4", "+","*"],
            "start" : "P",
            "rules" : {
                        "P" : ("S"),
                        "S" : ("S + M" , "M"),
                        "M" : ("M * T", "T"),
                        "T" : ("1", "2", "3", "4"),
                      }
        }

        s2 = '2 + 3 * 4'
        input2 = s2.split(" ")
        chart2 = Earley_Parser(grammar2, input2)
        expected2 =  [ [('P', 'S', 0, 0, ()), ('S', 'S + M', 0, 0, ()), ('S', 'M', 0, 0, ()), ('M', 'M * T', 0, 0, ()), ('M', 'T', 0, 0, ()), ('T', '1', 0, 0, ()), ('T', '2', 0, 0, ()), ('T', '3', 0, 0, ()), ('T', '4', 0, 0, ())],
                    [('T', '2', 1, 0, ()), ('M', 'T', 1, 0, ((1, 0),)), ('S', 'M', 1, 0, ((1, 1),)), ('M', 'M * T', 1, 0, ((1, 1),)), ('P', 'S', 1, 0, ((1, 2),)), ('S', 'S + M', 1, 0, ((1, 2),))],
                    [('S', 'S + M', 2, 0, ((1, 2),)), ('M', 'M * T', 0, 2, ()), ('M', 'T', 0, 2, ()), ('T', '1', 0, 2, ()), ('T', '2', 0, 2, ()), ('T', '3', 0, 2, ()), ('T', '4', 0, 2, ())],
                    [('T', '3', 1, 2, ()), ('M', 'T', 1, 2, ((3, 0),)), ('S', 'S + M', 3, 0, ((1, 2), (3, 1))), ('M', 'M * T', 1, 2, ((3, 1),)), ('P', 'S', 1, 0, ((3, 2),)), ('S', 'S + M', 1, 0, ((3, 2),))],
                    [('M', 'M * T', 2, 2, ((3, 1),)), ('T', '1', 0, 4, ()), ('T', '2', 0, 4, ()), ('T', '3', 0, 4, ()), ('T', '4', 0, 4, ())],
                    [('T', '4', 1, 4, ()), ('M', 'M * T', 3, 2, ((3, 1), (5, 0))), ('S', 'S + M', 3, 0, ((1, 2), (5, 1))), ('M', 'M * T', 1, 2, ((5, 1),)), ('P', 'S', 1, 0, ((5, 2),)), ('S', 'S + M', 1, 0, ((5, 2),))]]

        self.assertEqual(chart2.tolist(), expected2)
