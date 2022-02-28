import collections

string = """
good afternoon class. this is a substitution of test. good luck in decoding it. look for two letter words, three letter words and phrases.
good luck. 
tim
"""

class node:
    def __init__(self, freq, symbol, left=None, right=None):
        # frequency of symbol
        self.freq = freq
  
        # symbol name (character)
        self.symbol = symbol
  
        # node left of current node
        self.left = left
  
        # node right of current node
        self.right = right
  
        # tree direction (0/1)
        self.huff = ''  
  
def printNodes(node, val=''):
    val += str(node.huff)

    if(node.left):
        printNodes(node.left, val)
    if(node.right):
        printNodes(node.right, val)

    if(not node.left and not node.right):
        print(f"{node.symbol} -> {val}")
  
  
# characters for huffman tree
characters = ['a', 'b', 'c', 'd', 'e', 'f']
  
# frequency of characters
frequences = [ 5, 9, 12, 13, 16, 45]
  
# list containing unused nodes
nodes = []
  
# converting characters and frequencies
# into huffman tree nodes
for  in enumerate(characters):
    nodes.append(node(freq[x], chars[x]))
  
while len(nodes) > 1:
    # sort all the nodes in ascending order
    # based on theri frequency
    nodes = sorted(nodes, key=lambda x: x.freq)
  
    # pick 2 smallest nodes
    left = nodes[0]
    right = nodes[1]
  
    # assign directional value to these nodes
    left.huff = 0
    right.huff = 1
  
    # combine the 2 smallest nodes to create
    # new node as their parent
    newNode = node(left.freq+right.freq, left.symbol+right.symbol, left, right)
  
    # remove the 2 nodes and add their
    # parent as new node among others
    nodes.remove(left)
    nodes.remove(right)
    nodes.append(newNode)
  
# Huffman Tree is ready!
printNodes(nodes[0])


if __name__ == "__main__":
    print(collections.Counter(string))