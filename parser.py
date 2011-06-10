# -*- coding: utf-8 -*-

from pyparsing import ParseResults, ParseException
from grammar import G, group, nmea, optional, checksum
from pprint import pprint
import yaml

# helpers
gramkey = lambda d: d.keys()[0]     # [_k_]
gramval = lambda d: d.items()[0][1] # [(k, _v_)]
isgroup = lambda d: not isinstance(d[gramkey(d)], (str, unicode)) # [{k, _[...]_}]
isoptional = lambda d: gramkey(d)[-1] == '?'
optname = lambda name: name.replace('?', '')

class Parser():
    def __init__(self, filename):
        '''Initialize and load grammar from yaml file'''
        self.grammar = self.__load(filename)

    def __walk(self, data):
        '''Transform pyparsing ParseResults into native types'''
        def number(s):
            try: return int(s)
            except ValueError: return float(s)
        def dump(res):
            if isinstance(res, (str, unicode)):
                try: res = number(res)
                except: pass
            if isinstance(res, ParseResults):
                group = dict()
                for k, v in res.items():
                    group[k] = dump(v)
                res = group
            return res
        for k in data:
            if k != 'CheckSum':
                data[k] = dump(data[k])
        return data

    def __gram(self, d):
        '''Recursively create pyparsing grammar statements from yaml elements'''
        if isgroup(d):
            groupname = gramkey(d)
            items = [self.__gram(x) for x in gramval(d)]
            return group(*items)(optname(groupname))
        else:
            name, elem = d.items()[0]
            return G.get(elem)(optname(name))

    def __load(self, filename):
        '''Load yaml file and make pyparsing grammar from its data'''
        data = yaml.load(open(filename, 'r').read())
        grammar = None
        for nmea_id in data:
            sentence = data[nmea_id]
            params = [nmea_id]
            required = True
            for elem in sentence:
                if isoptional(elem):
                    required = False
                if required: # [req, req, ..., req + opt + opt + ... + opt]
                    params.append(self.__gram(elem))
                else:
                    params[-1] += optional(self.__gram(elem))
            if not grammar: # g = a | b | c
                grammar = nmea(*params)
            else:
                grammar |= nmea(*params)
        return grammar

    def parse(self, s):
        '''Parse NMEA string into dictionary of values and check control sum'''
        raw = self.grammar.parseString(s).asDict()
        data = self.__walk(raw)
        data['CheckOK'] = int(str(data['CheckSum']) == checksum(s))
        return data

if __name__ == '__main__':
    parser = Parser('data/nmea.yaml')
    # example 1
    from testdata import strings as test_strings
    for sentence in test_strings:
        print sentence
        pprint(parser.parse(sentence))
    '''
    # example 2
    dump = open('data/gps.dump').readlines()
    for line in dump:
        pair = line.split(':')
        if len(pair) == 2:
            sentence = pair[1].strip()
            print sentence
            try:
                pprint(parser.parse(sentence))
            except ParseException as e:
                print 'Error: malformed sentence, %s' % e
    '''

