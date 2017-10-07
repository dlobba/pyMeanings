import html2text as h2t
import collections
import re
import sys

import rst_helper as rh

from PyDictionary import PyDictionary

def find_word(text, blacklist):
    """Return all the words of a given file that aren't in the
    blacklist."""
    for word in re.split("[^\w]+", text):
        if not len(word):
            continue
        word = str.lower(word)
        if word not in blacklist:
            yield(word)

def collect_meanings(words):
    words_assign = {word:None for word in words}
    
    py_dict = PyDictionary()
    
    for word in words_assign.keys():
        words_assign[word] = py_dict.meaning(word)
        
    return words_assign
            
def main(file_path):

    html_handler = h2t.HTML2Text()
    blacklist = set()
    words = set()

    with open(file_path) as file_h:
        for line in file_h:
            text = html_handler.handle(line)
            for word in find_word(text, blacklist):
                words.add(word)

    meanings = collect_meanings(words)  
    rst = rh.Document("ciao.rst")
    rst.add_content(rh.DefinitionList(meanings))
    
    return rst
            
if __name__ == "__main__":
    main(sys.argv[1])
    
    
                
            