# -*- coding: utf-8 -*-
import sys
import re

class Node(object):
    __num__ = -1
    def __init__(self):
        self.transition = {}
        self.suffixLink = None
        self.ids = set()
        self.id = Node.__num__
        Node.__num__ += 1

    def addTransition(self, node, start, end, ch):
        self.transition[ch] = (node, start, end)

    def isLeaf(self):
        if len(self.transition) > 0:
            return False
        else:
            return True

    def __str__(self):
        return "Node:({})".format(", ".join(self.transition.keys()))

class SuffixTree(object):
    def __init__(self):
        self.text = ""
        self.str_list = []
        self.seps = []
        self.bottom = Node()
        self.root = Node()
        self.root.suffixLink = self.bottom
        self.s = self.root
        self.k = 0
        self.i = -1
        self.terminal_gen = self._terminalSymbolsGenerator()
        self.index = -1

    def addString(self, text):
        ori_len = len(self.text)
        sep = self.terminal_gen.next()
        text += sep
        self.seps.append(sep)
        self.text += text
        self.str_list.append(text)
        self.index += 1
        s = self.s
        k = self.k
        i = self.i
        for j in range(ori_len, len(self.text)):
            self.bottom.addTransition(self.root, j, j, self.text[j])
        while i < len(self.text) - 1:
            i += 1
            up = self.update(s, k ,i)
            up = self.canonize(up[0], up[1], i)
            s = up[0]
            k = up[1]
        self.s = s
        self.k = k
        self.i = i

    def update(self, s, k , i):
        oldr = self.root
        endPoint, r = self.testAndSplit(s, k, i - 1, self.text[i])
        while not endPoint:
            r.addTransition(Node(), i, len(self.text) - 1, self.text[i])
            if oldr != self.root:
                oldr.suffixLink = r
            oldr = r
            s, k = self.canonize(s.suffixLink, k, i - 1)
            endPoint, r = self.testAndSplit(s, k, i - 1, self.text[i])
            if oldr != self.root:
                oldr.suffixLink = s
        return s, k

    def testAndSplit(self, s, k, p, t):
        if k <= p:
            s2, k2, p2 = s.transition[self.text[k]]
            if t == self.text[k2 + p - k + 1]:
                return True, s
            else:
                r = Node()
                s.addTransition(r, k2, k2 + p - k, self.text[k2])
                r.addTransition(s2, k2 + p - k + 1, p2, self.text[k2 + p - k + 1])
                return False, r
        else:
            if t in s.transition:
                return True, s
            else:
                return False, s

    def canonize(self, s, k, p):
        if p < k:
            return s, k
        else:
            s2, k2, p2 = s.transition[self.text[k]]
        while p2 - k2 <= p - k:
            k = k + p2 - k2 + 1
            s = s2
            if k <= p:
                s2, k2, p2 = s.transition[self.text[k]]
        return s, k

    def _terminalSymbolsGenerator(self):
        """Generator of unique terminal symbols used for building the Generalized Suffix Tree.
        Unicode Private Use Area U+E000..U+F8FF is used to ensure that terminal symbols
        are not part of the input string.
        """
        py2 = sys.version[0] < '3'
        #UPPAs = list(list(range(0xE000,0xF8FF+1)) + list(range(0xF0000,0xFFFFD+1)) + list(range(0x100000, 0x10FFFD+1)))
        UPPAs = map(lambda x : ord(x), ["$","#","%"])
        for i in UPPAs:
            if py2:
                yield(unichr(i))
            else:
                yield(chr(i))
        raise ValueError("To many input strings.")
    
    def dot_str(self):
        dot = 'digraph G{{label="{}";\n'.format(self.text)
        nodes = [self.root]
        while len(nodes) > 0:
            node = nodes.pop(0)
            if node.isLeaf():
                pass
            else:
                for ch in node.transition.keys():
                    n, start, end = node.transition[ch]
                    label = self.text[start:end+1]
                    dot += '{}->{}[label="{}"];\n'.format(node.id, n.id, label)
                    sl = n.suffixLink
                    if sl:
                        dot += '{}->{}[style=dotted,constraint=false,arrowhead=vee,arrowsize=0.7];\n'.format(n.id, sl.id)
                    nodes.append(n)
        dot += "}\n"
        return dot

stree = SuffixTree()
# stree.addString("abcabxabcd")
stree.addString("abcabxabcd")
# stree.addString("abcx")
# stree.addString("abca")
print stree.dot_str()
