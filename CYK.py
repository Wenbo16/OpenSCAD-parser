import numpy as np

# Input: A string s = s[0], ... , s[len(s) - 1] and CFG G in CNF form
# Output: A Boolean value indicating if s is in L(G)



grammer2= {
    "variables" : [ "NP", "Nom", "AP", "A", "Det", "AdvD" ],
    "terminals" : [ "a", "very", "heavy","book", "orange"],
    "start" : "NP",
    "rules" : {
                "NP" : ["Det Nom"],
                "Nom" : ["book", "orange", "AP Nom"],
                "AP" : ["heavy", "orange", "AdvD A"],
                "A" : ["heavy", "orange"],
                "Det" : ["a"],
                "AdvD" : ["very"]
              }
}


def findRule (G, result):
    ruleSet = set()
    for v in G["variables"]:
        for symbol in  G["rules"][v]:
            if symbol == result:
                ruleSet.add(v)
    return ruleSet


def createTable(s):
    Table = []
    for i in range (len(s)):
        Table.append([])
        for j in range (len(s)+1):
            Table[i].append(set())
    return Table



def findSubString(G, cell1, cell2):
    cell = set()
    if (cell1 == set([]) or cell2 == set([]) ):
        return cell
    for symbol1 in cell1:
        for symbol2 in cell2:
            print symbol1 + " " + symbol2
            rule = findRule(G, symbol1 + " " + symbol2)
            print rule
            cell = cell | rule
    return cell


def CYK(s,G):
    MemoTable = createTable(s);

    for j in range(1, len(s)+1):  # column j
        print "j= ", j
        MemoTable[j-1][j] = findRule (G, s[j-1])
        if  MemoTable[j-1][j] == set([]):
            print  s, "is not in the bottom"
            return False

        for i in range(j-2,-1,-1): # fill row i in column j
            for k in range(i+1, j):     # loop over cell below cell[i][j]
                cell = findSubString(G, MemoTable[i][k], MemoTable[k][j])
                MemoTable[i][j]  = MemoTable[i][j] | cell

    MemoTable = np.array(MemoTable)
    print MemoTable

    if G["start"] in MemoTable[0][len(s)]:
        print "true"
        return True
    else:
        print "false"
        return False



s = ["a", "very", "heavy", "orange", "book"]

CYK(s, grammer2)