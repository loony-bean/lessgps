# -*- coding: utf-8 -*-

gga = '$GPGGA,084037,2727.9487,S,15305.3408,E,1,07,02.0,-00000.9,M,039.4,M,,*77'
gsa = '$GPGSA,A,3,07,08,11,13,17,27,28,,,,,,05.3,02.0,04.8*0E'
gsv = '$GPGSV,2,1,08,01,40,083,46,02,17,308,41,12,07,344,39,14,22,228,45*75'
rmc = '$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A'
vtg = '$GPVTG,054.7,T,034.4,M,005.5,N,010.2,K*48'
gll = '$GPGLL,4916.45,N,12311.12,W,225444,A*31'

strings = [gga, gsa, gsv, rmc, vtg, gll]
types = ('GGA', 'GSA', 'GSV', 'RMC', 'VTG', 'GLL')

testdata = zip(strings, types)
testdata += testdata * int(1000/len(testdata)) # ~1000 sents

