from parsing import Earley_Parser, findRoot

# Get the token map from the lexer.  This is required.

grammar= {
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

s = 'the large can can hold the water'
s2 = '2 + 3 * 4'
input = s.split(" ")
print Earley_Parser(grammar, input)

chart = Earley_Parser(grammar, input)
root = findRoot(chart, input, grammar)
print "root: ", root


def printTree(state):
    print state[0], ' -> ', state[1]
    if state[4] == ():
        pass
    else:
        for ptr in state[4]:
            printTree(chart[ptr[0]][ptr[1]])


def printSideways(state):
    print state[1],
    if state[4] != ():
        n = len(state[4])
        for i in range(n-1, -1, -1 ):
            printSideways(chart[state[4][i][0]][state[4][i][1]])

printTree(root)