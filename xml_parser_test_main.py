#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: mkrishan
"""


import sys
from lxml import etree
from itertools import groupby
import numpy as np
from xml.dom import minidom
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, tostring
from xml.dom.minidom import parseString
import dicttoxml
import pandas as pd
import cluster_matrices
###############################################################################################
class XML2Dict():
    """ Converts an XML object to Python Dictionary
   """
    def __init__(self):
        self.merge_keys = ["action" ]
 
    def __dappend(self, dictionary, key, item):
        """Append item to dictionary at key."""
 
        if key == "#attributes":
            for k,v in item.items():
                dictionary.setdefault(k, v)
            return
 
        if key in dictionary.keys():
            if key not in dictionary.keys():
                dictionary[key] = []
            if not isinstance(dictionary[key], list):
                lst=[]
                lst.append(dictionary[key])
                lst.append(item)
                dictionary[key]=lst
            else:
                dictionary[key].append(item)
        else:
            dictionary.setdefault(key, item)
 
    def __node_attributes(self, node):
        """Return an attribute dictionary """
        if node.hasAttributes():
            return dict([(str(attr), str(node.attributes[attr].value)) for attr in node.attributes.keys()])
        else:
            return None
 
    def __attr_str(self, node):
        return "%s-attrs" % str(node.nodeName)
 
    def __hasAttributes(self, node):
        if node.nodeType == node.ELEMENT_NODE:
            if node.hasAttributes():
                return True
        return False
 
    def __with_attributes(self, node, values):
        if self.__hasAttributes(node):
            if isinstance(values, dict):
                self.__dappend(values, '#attributes', self.__node_attributes(node))
                return { str(node.nodeName): values }
            elif isinstance(values, str):
                return { str(node.nodeName): values,
                         self.__attr_str(node): self.__node_attributes(node)}
        else:
            return { str(node.nodeName): values }
 
    def xml2dict(self, node):
        """Given an xml dom node tree,
       return a python dictionary corresponding to the tree structure of the XML. 
       """
        if not node.hasChildNodes():
            if node.nodeType == node.TEXT_NODE:
                if node.data.strip() != '':
                    return str(node.data.strip())
                else:
                    return None
            else:
                ret =  self.__with_attributes(node, None)
                return ret
        else:
            #recursively create the list of child nodes
            childlist = []
            for child in node.childNodes:
                xc = self.xml2dict(child)
                if xc != None and child.nodeType != child.COMMENT_NODE:
                    childlist.append(xc)
            if len(childlist)==1 and isinstance(childlist[0], str):
                return self.__with_attributes(node, childlist[0])
            else:
                #if False not in [isinstance(child, dict) for child in childlist]:
                new_dict={}
                for child in childlist:
                    if isinstance(child, dict):
                        for k in child:
                            self.__dappend(new_dict, k, child[k])
                    elif isinstance(child, str):
                        self.__dappend(new_dict, '#text', child)
                    else:
                        print ("ERROR")
                ret =  self.__with_attributes(node, new_dict)
 
                
                if len(ret) == 1 and isinstance(list(ret.values())[0], dict):
                    k,v = list(ret.items())[0]
                    if isinstance(v, dict):
                        k1,v1 = list(v.items())[0]
                        if isinstance(v1, list) and k1 in self.merge_keys and k1 + "s" == node.nodeName:
                            ret = { str(node.nodeName): v1 }
                return ret



P = cluster_matrices.R
m,n = P.shape
variabledict = {}
for k in range(int(n)):
    datavalloop = P[:][0:,k]
    l = [num for num in datavalloop if num]
    ni = ["{}_{}".format("value",i)  for i, e in enumerate(datavalloop) if e != 0]
    
    cluster_entries = dict(zip(ni,l))
    more_deep = 
    variabledict["{}_{}".format("e:Cluster", k)] = cluster_entries
print(variabledict)   


xml_data = xml_writer.dicttoxml(variabledict, attr_type=False,root=True)
dom = parseString(xml_data)
print(dom.toprettyxml())
open("bounds.xml", "w").write(dom.toprettyxml())
##########################################################
