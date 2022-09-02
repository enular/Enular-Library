'''
Author: B. Bradford

MIT License

Copyright (c) 2020 B. Bradford

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from backtrader.indicator import Indicator
from backtrader.functions import If, And

import copy



class ZigZag(Indicator):

    lines = ('zigzag',
             'zigzag_peak',
             'zigzag_valley')

    params = (('plotdistance', 0.03), )  # distance to plot arrows (alters high/low indicator lines but not zigzag line)

    plotinfo = dict(subplot=True, zigzag=dict(_name='zigzag',
                                              color='darkblue',
                                              ls='--',
                                              _skipnan=True))

    plotlines = dict(
        zigzag_peak=dict(marker='v', markersize=7.0, color='red', fillstyle='full', ls=''),
        zigzag_valley=dict(marker='^', markersize=7.0, color='red', fillstyle='full', ls=''),
        )

    def __init__(self):
        tmp = copy.copy(self.data)
        tmp = If(self.data(0) == self.data(-1), tmp(-1) + 0.000001, self.data(0))
        self.zigzag_peak = If(And(tmp(0)>tmp(-1), tmp(0)>tmp(1)), self.data(0), float('nan'))
        tmp = copy.copy(self.data)
        tmp = If(self.data(0) == self.data(-1), tmp(-1) - 0.000001, self.data(0))
        self.zigzag_valley = If(And(tmp(0) < tmp(-1), tmp(0) < tmp(1)), self.data(0), float('nan'))
        self.lines.zigzag = If(self.zigzag_peak, self.zigzag_peak, If(self.zigzag_valley, self.zigzag_valley, float('nan')))
        self.lines.zigzag_peak = self.zigzag_peak * (1 + self.p.plotdistance)
        self.lines.zigzag_valley = self.zigzag_valley * (1 - self.p.plotdistance)