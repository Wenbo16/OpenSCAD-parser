# -*- coding: UTF-8 -*-
from __future__ import absolute_import
import unittest
from tokenization import getTokens


# Test it out

class Test_Tokenization(unittest.TestCase):
    def test_token_number(self):
        data1 = '''
                  inf = 1e200 * 1e200;
               '''
        expected = ["TOK_ID", '=', 'TOK_NUMBER', '*', 'TOK_NUMBER', ';']
        self.assertEqual(getTokens(data1), expected)

        data2 = '''
            2e+123
        '''
        expected = ['TOK_NUMBER']
        self.assertEqual(getTokens(data2), expected)

        data3 = '''
            333.989e-6
        '''
        expected = ['TOK_NUMBER']
        self.assertEqual(getTokens(data3), expected)

        data4 = '''
                    .989e-6
                '''
        expected = ['TOK_NUMBER']
        self.assertEqual(getTokens(data4), expected)



    def test_Unicode(self):
        data1 = '''
            数学
        '''
        expected = ['TOK_ERROR']
        self.assertEqual(getTokens(data1), expected)



    def test_syntax(self):
        data1 = '''
            translate([0, 0, 30]) {
                cylinder(h=40, r=10);
            }
        '''
        expected = ['TOK_ID', '(', '[', 'TOK_NUMBER', ',', 'TOK_NUMBER', ',', 'TOK_NUMBER', ']', ')', '{', 'TOK_ID', '(', 'TOK_ID',
                    '=', 'TOK_NUMBER', ',', 'TOK_ID',  '=', 'TOK_NUMBER', ')', ';', '}']
        self.assertEqual(getTokens(data1), expected)



        data2 = '''
             0.5+sin(10*i)/2
        '''
        expected = ['TOK_NUMBER', '+', 'TOK_ID', '(', 'TOK_NUMBER', '*', 'TOK_ID',')','/','TOK_NUMBER']
        self.assertEqual(getTokens(data2), expected)


        data3 = '''
            echo("Variable a is ", a);
            if (a==undef) {
                echo("Variable a is tested undefined");
            }
        '''
        expected = ['TOK_ECHO', '(', 'TOK_STRING', ',', 'TOK_ID', ')', ';', 'TOK_IF', '(', 'TOK_ID', 'EQ', 'TOK_UNDEF', ')',
                    '{', 'TOK_ECHO', '(', 'TOK_STRING', ')', ';', '}' ]
        self.assertEqual(getTokens(data3), expected)

if __name__ == '__main__':
    unittest.main()