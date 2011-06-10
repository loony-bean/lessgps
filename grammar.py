# -*- coding: utf-8 -*-

from pyparsing import *
import array

# parse actions
def to_latlon(s,l,toks):
    if toks:
        value = float(toks[0][:2]) + float(toks[0][2:])/60 # ddmm.mmmm
        if toks[1] == 'S' or toks[1] == 'W':
            value *= -1
        return value
    else:
        return 0

def to_utc(s,l,toks):
    return toks and toks[0] or '0'      # todo (Date also)

# elements grammar
class grammar_factory(dict):
    '''Store pyparsing grammar elements and create them by name'''
    def __init__(self):
        self.prefix = oneOf('$ !')
        self.talker = Word(alphas, exact=2)
        self.delimiter = Suppress(',')
        self.asterisk = Literal('*')
        self.checksum = Word(nums + 'ABCDEF')('CheckSum')

        self.real = Word('+-.' + nums)
        self.r = self.real
        self.ro = Optional(self.r)      # todo: define optionals in yaml

        self.du = oneOf('M')            # Distance units: Meter
        self.su = oneOf('N K')          # Speed units: Knot, Kph
        self.ns = oneOf('N S')          # Direction: North, South
        self.ew = oneOf('E W')          # Direction: East, West
        self.ewo = Optional(self.ew)
        self.mt = oneOf('M T')          # Variation: Magnetic, True
        self.mto = Optional(self.mt)

        self.gpsstat = oneOf('A V')     # A=Active, V=Void
        self.fixmode = oneOf('M A')     # M=Manual, A=Auto
        self.fixtype = oneOf('1 2 3')   # 1=NA, 2=2D Fix (<4 SV's used), 3=3D Fix (>3 SV's used)
        self.fixqual = oneOf('0 1 2')   # 0=NA/Invalid, 1=GPS, 2=DGPS

        self.lat = (self.r + self.delimiter + self.ns).setParseAction(to_latlon)
        self.lon = (self.r + self.delimiter + self.ew).setParseAction(to_latlon)
        self.utc = self.r.setParseAction(to_utc)

        # NMEA v2.3
        # A=autonomous, D=differential, E=Estimated, N=not valid, S=Simulator. 
        # Only the A and D values will correspond to an Active and reliable Sentence.
        # This mode character has been added to the RMC, RMB, VTG, and GLL sentences
        # and optionally some others including the BWC and XTE sentences.
        self.fixkind = oneOf('A D E N S')

    def get(self, name):
        return self.__getattribute__(name)

G = grammar_factory()

# sentence grammar helpers
def nmea(*params):
    '''Creates NMEA sentence with all headers and footers'''
    # todo: proprietary messages
    # todo: query messages
    # first is threated as header
    grammar = G.prefix + G.talker('Talker') + Literal(params[0])('Type')
    for elem in params[1:]:
        grammar += G.delimiter + elem
    grammar += G.asterisk + G.checksum
    return grammar

def group(*params):
    '''Creates named group of elements'''
    grammar = params[0]
    for elem in params[1:]:
        grammar += G.delimiter + elem
    return Group(grammar)
    
def optional(param):
    '''Optional element. Note that only single (not grouped) element can be optional'''
    return Optional(G.delimiter + param)

def checksum(s):
    '''Calculate NMEA sentence check sum'''
    bytes = array.array('b', s[1:-3])
    sum = bytes[0]
    for e in bytes[1:]:
        sum ^= e
    return "%02X" % sum

