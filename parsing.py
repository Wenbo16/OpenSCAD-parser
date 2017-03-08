import numpy as np

# Description of our algorithm


RULE_VARIABLE = 0
RULE_STRINGS = 1
DOT_LOCATION = 2
#            = 3
BACK_POINTER = 4

def creatEmptyChart(tokenList):
    chartTable = []
    for i in range (len(tokenList)+1):
        chartTable.append([])
    return chartTable


def memoSet (tokenList):
    setList = []
    for i in range (len(tokenList)+1):
       setList.append(set())
    return setList

# cell[STATUS_VALUE] == FLAGGED

def Earley_Parser(grammar, tokenizedCode):


    # initialize the chart table to store data
    chart = creatEmptyChart(tokenizedCode)
    chartSet = memoSet(tokenizedCode)
    startPoint = grammar["start"]
    startRule = grammar["rules"][startPoint]
    chart[0].append(( grammar["start"], startRule, 0, 0, ()))


    chartWidth = len(tokenizedCode)+1
    for k in range (0, chartWidth):
        index = 0
        for state in chart[k]:
            if not finished(state):
                nextElement = state[RULE_STRINGS].split(" ")[state[DOT_LOCATION]]
                if nextElement in grammar["nonterminals"]:
                    predictor(state, k, grammar, chart, chartSet[k], index)
                else:
                    if k <  len(tokenizedCode):
                        scanner(state, k, tokenizedCode, chart)
            else:
                completer(state, k, chart,  index)
            index += 1

    chart = np.array(chart)
    return chart


def finished(state):
    length = len(state[RULE_STRINGS].split(" "))
    return state[DOT_LOCATION] == length


def predictor(state, k, grammar, chart, stateSet, index):
    dot = state[DOT_LOCATION]
    nonterminal = state[RULE_STRINGS].split(" ")[dot]
    subindex = 0
    for production in grammar["rules"][nonterminal]:
        newState = (nonterminal, production, 0, k, ())
        if newState not in stateSet:
            chart[k].append( newState )
            stateSet.add( newState )
            subindex +=1
        if production == "":                 # bug solved
            jumpState = (state[RULE_VARIABLE], state[RULE_STRINGS], state[DOT_LOCATION]+1, state[3], state[BACK_POINTER])
            jumpState = addBackPointer(jumpState, (k, index+subindex))
            if jumpState not in stateSet:
                chart[k].append(jumpState)
                stateSet.add( jumpState )



def scanner(state, k, words, chart):
    dot = state[DOT_LOCATION]
    terminal = state[RULE_STRINGS].split(" ")[dot]
    if terminal == words[k]:
        chart[k+1].append((state[RULE_VARIABLE], state[RULE_STRINGS], state[DOT_LOCATION] + 1, state[3], state[BACK_POINTER]))



def completer(state, k ,chart, index):
    for i in chart[state[3]]:
        if not finished(i):
            if i[RULE_STRINGS].split(" ")[i[DOT_LOCATION]] == state[RULE_VARIABLE]:
                completeState = (i[RULE_VARIABLE], i[RULE_STRINGS], i[DOT_LOCATION]+1, i[3], i[BACK_POINTER])
                completeState = addBackPointer(completeState, (k, index))
                chart[k].append(completeState)



def addBackPointer( state , ptr ):  # ptr = (1,2)
    (a,b,c,d,e) = state
    e = e + (ptr,)
    state = (a,b,c,d,e)
    return  state



def findRoot(chart, tokenList, grammar):
    target = (grammar["start"], grammar["rules"][grammar["start"]], 1, 0)
    for state in chart[len(tokenList)]:
        (a,b,c,d,e) = state
        s = (a,b,c,d)
        if s == target:
            return state


