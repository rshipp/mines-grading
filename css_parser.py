#!/usr/bin/env python

import re
import sys

cssfile = open(sys.argv[2], 'r')

def cssHas(cssStruct, element, attribute, value):
    for sel in cssStruct:
        if element in sel:
            if attribute in cssStruct[sel].attribs:
                if cssStruct[sel].attribs[attribute] == value:
                    return True
#            else:
#                print(attribute + " was not in " + str(cssStruct[sel].attribs))
    return False

def cssGet(cssStruct, element, attribute):
    for sel in cssStruct:
        if element in sel:
            if attribute in cssStruct[sel].attribs:
                return cssStruct[sel].attribs[attribute]
    return ""

class CssSelector:
    attribs = {}
    sel = ""

    def __init__(self, selector, props):
        self.sel = selector
        self.attribs = props

    def addAttrib(self, attribute, value):
        self.attribs[attribute] = value

    def __repr__(self):
        ret = self.sel + " { "
        for k in self.attribs:
            ret += k + ": " + self.attribs[k] + "; "
        ret += "}"
        return ret

unlined = ""
for l in cssfile:
    unlined += l.strip()

tokens = re.findall("([a-z0-9A-Z, .#_]+)\s*({.*?})", unlined)

sels = {}
for t in tokens:
    props = re.findall("([a-zA-Z0-9\-_]+)\s*:\s*([_a-zA-Z0-9# \-)(,]+);?", t[1])
    pmap = {}
    for pairs in props:
        pmap[pairs[0]] = pairs[1].lower()
    if t[0] not in sels:
        sels[t[0]] = CssSelector(t[0], pmap)
    else:
        sels[t[0]].attribs.update(pmap)
        print("Updated %s, so it now has %s" % (t[0], str(sels[t[0]].attribs)))

#print("Tests pass? " + str(
#    cssHas(sels, "body", "color", "black")
#    and cssHas(sels, "h1", "float", "right")
#    and cssHas(sels, "h2", "float", "right")
#    ))

def propHasAttrs(sels, selector, attribs, values):
    has = False
    allVals = ""
    for a in attribs:
        for v in values:
            if cssHas(sels, selector, a, v):
                has = True
        else:
            allVals += cssGet(sels, selector, a)

    if not has:
        print("In %s, expected one of %s to have one of %s, but it had %s" % (selector, attribs, values, allVals))

