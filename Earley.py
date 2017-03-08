
import numpy as np

grammar= {
    "nonterminals" : [ "Start", "S", "NP", "VP", "prep", "N", "Adj" ,"Aux", "V"],
    "terminals" : [ "the", "large", "can","hold", "water"],
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



def init(list):
    Table = []     # DECLARE ARRAY S;
    for i in range (len(list)+1):
        Table.append([])
    return Table

def initSet (list):
    setList = []     # DECLARE ARRAY S;
    for i in range (len(list)+1):
       setList.append(set())
    return setList


def Earley_Parser(grammar, words):
    chart = init(words)
    chartSet = initSet(words)
    chart[0].append(( grammar["start"], grammar["rules"][grammar["start"]], 0 ,0))
    for k in range (0, len(words)+1):
        for state in chart[k]:
            if not finished(state):
                nextElement = state[1].split(" ")[state[2]]
                if nextElement in grammar["nonterminals"]:
                    predictor(state, k, grammar, chart, chartSet[k])
                else:
                    if k <  len(words):
                        scanner(state, k, words, chart)
            else:
                completer(state, k, chart)
    chart = np.array(chart)
    return chart




def finished(state):
    length = len(state[1].split(" "))
    return state[2] == length


def predictor(state, k, grammar, chart, stateSet):
    dot = state[2]
    nonterminal = state[1].split(" ")[dot]
    for production in grammar["rules"][nonterminal]:
        newState = (nonterminal, production, 0, k)
        if newState not in stateSet:
            chart[k].append( newState )
            stateSet.add( newState )




def scanner(state, k, words, chart):
    dot = state[2]
    terminal = state[1].split(" ")[dot]
    if terminal == words[k]:
        chart[k+1].append((state[0], state[1], state[2] + 1, state[3]))


def completer(state, k ,chart):
    for i in chart[state[3]]:
        if not finished(i):
            if i[1].split(" ")[i[2]] == state[0]:
                completState = (i[0], i[1], i[2]+1, i[3])
                chart[k].append(completState)

s = 'the large can can hold the water'
s2 = '2 + 3 * 4'
input = s2.split(" ")
print Earley_Parser(grammar2, input)
