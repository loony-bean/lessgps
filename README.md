LessGPS
=======

This is a Python library for parsing [NNEA][1] (GPS currently) sentences. It was inspired 
by Tim Savage [Python NMEA Tolkit][2] but made more friendly and easily configurable by using
[Pyparsing][3] library and [YAML][4] description files for NMEA sentences.

Introduction
------------

NMEA format is widely used in navigational software, chart plotters, GPS drivers, etc.
In the past this was a job for embedded systems hosting mostly ANSI C programs because
of hardware limitations and productivity expectations. But now more and more navigation
is made using general purpose laptops, pads and smartphones. Hardware is not an issue 
any more, and we can use more advanced languages and technologies for navigation tasks.

LessGPS utilizes a fact that NMEA sentences have really simple structure,
thus it is possible to define sentence structure in human understandable
format and once having core parsing engine add new definitions without
actually modifying the code.

Usage
-----

### Grammar ###

There is a ton of NMEA sentences, many of them are proprietary, but there is a limited
set of elements, like *lat*, *lon*, *utc*, that form every single message. This is a
core of LessGPS grammar, and it is defined in internal *grammar_factory* class of
*grammar.py*. Then, for convenience, it is possible to make named groups of grammar
elements and give names to particular elements.

### Configuration ###

Before the parser can start working, you should provide it with grammar YAML file.
The basic grammar is provided in *lessgps/data/nmea.yaml*. You should populate it 
with any sentences you need, and than pass the file path to Parser constructor.
Everything in the YAML file is very staightforward, for example lets see the
definition of GLL:

    GLL:
      - Lat: lat
      - Lon: lon
      - UTC: utc
      - GPSStat: gpsstat
      - FixKind?: fixkind

This defines GLL sentense that consists from *lat*, *lon*, *utc*, *gpsstat* grammar elements
and optional *fixkind* (added in 2.3 version of NMEA protocol). After parsing this GLL
string will be translated into python dictionary with keys 'Lat', 'Lon', 'UTC',
'GPSStat' and 'FixKind' accordingly.

### Example ###

    # -*- coding: utf-8 -*-
    import lessgps
    from pprint import pprint

    gga = '$GPGGA,084037,2727.9487,S,15305.3408,E,1,07,02.0,-00000.9,M,039.4,M,,*77'
    gsa = '$GPGSA,A,3,07,08,11,13,17,27,28,,,,,,05.3,02.0,04.8*0E'
    gsv = '$GPGSV,2,1,08,01,40,083,46,02,17,308,41,12,07,344,39,14,22,228,45*75'
    rmc = '$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A'
    vtg = '$GPVTG,054.7,T,034.4,M,005.5,N,010.2,K*48'
    gll = '$GPGLL,4916.45,N,12311.12,W,225444,A*31'

    strings = [gga, gsa, gsv, rmc, vtg, gll]

    if __name__ == "__main__":
        parser = lessgps.Parser('lessgps/data/nmea.yaml')
        for sentence in strings:
            print sentence
            pprint(parser.parse(sentence))

[1]: http://en.wikipedia.org/wiki/NMEA_0183     "NMEA Protocol"
[2]: http://code.google.com/p/python-gpsd       "Python NMEA Tolkit"
[3]: http://pyparsing.wikispaces.com            "PyParsing"
[4]: http://www.yaml.org                        "YAML"

