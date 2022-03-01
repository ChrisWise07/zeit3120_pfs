import collections
import huffman

string = """
good afternoon class. this is a substitution of test. good luck in decoding it. look for two letter words, three letter words and phrases.
good luck. 
tim
"""

print(huffman.codebook(collections.Counter(string).items()))
