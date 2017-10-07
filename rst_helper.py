"""A very small module to help adding rst content to a file."""

import re
import os
import collections

class Title:

    def __init__(self, title=None, level=1):
        """Crete an rst Title for the given level.
        
        Level 1
          for the main titles
          
        Level 2
          for section/chapter titles
          
        Level 3
          for paragraph/subsection titles
        """
        self.title = re.sub("(\s+|\n)", "", title)
        self.level = level

    def __str__(self):
        str = self.title + "\n"
        length = len(self.title)
        
        if self.level == 1:
            level_string = "=" * length
        if self.level == 2:
            level_string = "-" * length
        if self.level == 3:
            level_string = "~" * length
        
        return str + level_string

class ListType:
    ENUMERATED = "e"
    UNORDERED = "*"
    
    TYPES = [ENUMERATED, UNORDERED]
    
    @classmethod
    def is_valid(cls, type):
        return type in cls.TYPES 
    
class List:

    def __init__(self, alist, type=ListType.UNORDERED, indent="\t", nested_level=0):
        self.alist = list()
        self.nested_level = nested_level
        self.indent = indent
        if not re.fullmatch("^(\ +|\t+)$", indent):
            self.indent = "\t"
        
        if ListType.is_valid(type):
            self.type = type
        
        for item in alist:
            if isinstance(item, str):
                self.alist.append(item)
            elif isinstance(item, dict):
                self.alist.append(DefinitionList(dict))
            elif isinstance(item, DefinitionList):
                self.alist.append(item)
            elif isinstance(item, list):
                self.alist.append()
    
    def __str__(self):
        indent = self.indent * self.nested_level
        alist = []
        
        list_symbol = self.type
        for item in self.alist:
            tmp = ""
            if isinstance(item, str):
                tmp += indent
            tmp += list_symbol + " " + str(item)
            alist.append(tmp)

        return str.join("\n\n", alist)
        
class DefinitionList:

    def __init__(self, definitions_dict, indent="\t", nested_level=0):
        """Create a DefinitionList given a Python
        dictionary containing name-definition pairs."""
        self.definitions = collections.OrderedDict()
        
        self.nested_level = nested_level
        self.indent = indent
        if not re.fullmatch("^(\ +|\t+)$", indent):
            self.indent = "\t"
        
        for definition, content in definitions_dict.items():
            # just skip the element
            if content is None:
                continue
            definition = str(definition)
            if isinstance(content, str):
                self.definitions[definition] = content
            elif isinstance(content, dict):
                self.definitions[definition] = DefinitionList(content, self.indent, self.nested_level + 1)
            elif isinstance(content, list):
                self.definitions[definition] = List(content, indent=self.indent, nested_level=self.nested_level + 1)
            else:
                self.definitions[definition] = str(content)

    def __str__(self):
        def_list = []
         
        indent = self.indent * self.nested_level
        list_indent = self.indent * (self.nested_level + 1)
        for definition, content in self.definitions.items():
            
            tmp = indent + "**" + definition + ":**\n"
            if isinstance(content, str):
                tmp += list_indent
            tmp += str(content)
            def_list.append(tmp)
            
        return str.join("\n\n", def_list)
        
class Document:

    EXTENSTION = ".rst"

    def __init__(self, title):
        self.__title = title
        self.content = []
    
    def add_content(self, content):
        self.content.append(content)
    
    def __str__(self):
        return str.join("\n\n", [str(content) for content in self.content])
    
    def to_file(self, path):
        with open(path + os.sep + self.__title + self.EXTENSTION, "w") as rst_file:
            rst_file.write(str(self))
    
    
   