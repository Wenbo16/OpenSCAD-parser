from parsing import Earley_Parser, findRoot

grammar= {
    "nonterminals" : [ "Start", "S", "NP", "VP", "prep", "N", "Adj" ,"Aux", "V"],
    "terminals" : set([ "the", "large", 'bottle', "can","hold", "water"]),
    "start" : "Start",
    "rules" : {
                "Start" : ("S"),
                "S" : ("NP VP",),
                "NP" : ("prep Adj N", "prep N", "Adj N"),
                "VP" : ("Aux VP", "V NP"),
                "prep" : ("the",),
                "Adj" : ("large",),
                "N" : ("can", "water", "bottle"),
                "Aux" : ("can",),
                "V" : ("can", "hold", "water"),
              }
}



s1 = 'the large can can hold the water'
input1 = s1.split(" ")
# print Earley_Parser(grammar, input1)
chart1 = Earley_Parser(grammar, input1)
root1 = findRoot(chart1, input1, grammar)
# print "root1: ", root1

s2 = 'the bottle hold the water'
input2 = s2.split(" ")
chart2 = Earley_Parser(grammar, input2)
root2 = findRoot(chart2, input2, grammar)

def printTree(state):
    print state[0], ' -> ', state[1]
    if state[4] == ():
        pass
    else:
        for ptr in state[4]:
            printTree(chart1[ptr[0]][ptr[1]])


# printTree(root2)

import zss
# from simple_tree import Node
from zss import Node, simple_distance


def buildTree(state, node, chart):
    if state[4] == ():
        return
    else:
        for ptr in state[4]:
            child = Node(chart[ptr[0]][ptr[1]][0])
            node.addkid(child)
            buildTree(chart[ptr[0]][ptr[1]], child, chart)


rootNode1 = Node("Start",[])
buildTree(root1, rootNode1, chart1)

rootNode2 = Node("Start",[])
buildTree(root2, rootNode2, chart2)

print simple_distance(rootNode1, rootNode2)


# for child in rootNode1.get_children():
#     for chichild in child.get_children():
#         print "parent is: ", chichild.get_label()
#         for chichichild in chichild.get_children():
#             print chichichild.get_label()

for child in Node.get_children(rootNode1):
    print Node.get_label(child)