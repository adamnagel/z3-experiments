#!/usr/bin/python
import networkx as nx
from z3 import *


class Wifi_Security(object):
    NONE = 0
    WEP = 1
    WPA = 2
    WPA2 = 3

    def __init__(self,
                 name,
                 include=None,
                 exclude=None):
        self.name = name
        if include:
            self.supports = include
        else:
            self.supports = [
                self.NONE,
                self.WEP,
                self.WPA,
                self.WPA2
            ]
            if exclude:
                for excl in exclude:
                    self.supports.remove(self.supports.index(excl))

    def z3(self):
        variable = Int(self.name)
        constraints = Or([variable == i for i in self.supports])

        return variable, constraints


class Wifi_Frequency(object):
    GHZ_2_4 = 2
    GHZ_5 = 5

    def __init__(self,
                 name,
                 include=None,
                 exclude=None):
        self.name = name

        if include:
            self.supports = include
        else:
            self.supports = [
                self.GHZ_2_4,
                self.GHZ_5
            ]
            if exclude:
                for excl in exclude:
                    self.supports.remove(excl)

    def z3(self):
        variable = Int(self.name)
        constraints = Or([variable == i for i in self.supports])

        return variable, constraints


class Wifi(object):
    def __init__(self,
                 name,
                 security_includes=None,
                 security_excludes=None,
                 frequency_includes=None,
                 frequency_excludes=None):
        self.frequency = Wifi_Frequency('%s_freq' % name,
                                        include=frequency_includes,
                                        exclude=frequency_excludes)

        self.security = Wifi_Security('%s_security' % name,
                                      include=security_includes,
                                      exclude=security_excludes)

    def z3(self):
        var_freq, constr_freq = self.frequency.z3()
        var_sec, constr_sec = self.security.z3()

        return var_sec, var_freq, And(constr_freq, constr_sec)


WIFI_FREQ_24 = 2
WIFI_FREQ_5 = 5

s = Solver()

# Create RBP
rbp_wifi_sec, rbp_wifi_freq, constr = Wifi(name='rbp',
                                           security_excludes=[Wifi_Security.WPA2],
                                           frequency_excludes=[Wifi_Frequency.GHZ_5]).z3()
s.add(constr)

# Create WRT
wrt_wifi_sec, wrt_wifi_freq, constr2 = Wifi(name='wrt').z3()
s.add(constr2)


# Constrain WiFi technology choices
s.add(rbp_wifi_sec == wrt_wifi_sec)
s.add(rbp_wifi_freq == wrt_wifi_freq)

# Solve
print('')
print('Is there a satisfying solution?')
print(s.check())

print('What is it?')
while s.check() == sat:
    print(s.model())
    s.add(Or(rbp_wifi_sec != s.model()[rbp_wifi_sec],
             wrt_wifi_sec != s.model()[wrt_wifi_sec]))

import unittest


class TestNothing(unittest.TestCase):
    def test_nothing(self):
        pass
