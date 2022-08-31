#!/usr/bin/env python
import os
import sys
import matplotlib
import yfinance
import numpy
import scipy
import sklearn
import pandas
import backtrader as bt
import indicators

import enular

class BTBBase(enular.IndicatorOperation):

    def b_standardise(self,stand_data):

        if stand_data >= 1.0:
            stand_data = 1.0
        elif stand_data <= -1.0:
            stand_data = -1.0
        else:
            stand_data = 0.0

        return stand_data

    def next_logic(self):
        pass

    def next(self):

        self.lines.temp0[0] = self.b_standardise(self.data0[0])
        self.lines.temp1[0] = self.b_standardise(self.data1[0])

        self.next_logic()

class BTBAnd(BTBBase):

    lines = ('btband','temp0','temp1',)

    def next_logic(self):

        operation = (self.lines.temp0[0] + self.lines.temp1[0])/2
        self.lines.btband[0] = self.b_standardise(operation)

class BTBOr(BTBBase):

    lines = ('btbor','temp0','temp1',)

    def next_logic(self):

        operation = self.lines.temp0[0] + self.lines.temp1[0]
        self.lines.btbor[0] = self.b_standardise(operation)

class BTBSo(BTBBase):

    lines = ('btbso','temp0','temp1',)

    def next_logic(self):

        operation = self.lines.temp0[0]
        self.lines.btbso[0] = self.b_standardise(operation)

class BTBNot(BTBBase):

    lines = ('btbnot','temp0','temp1',)

    def next_logic(self):

        operation = self.lines.temp0[0] * -1
        self.lines.btbnot[0] = self.b_standardise(operation)

class BTBXor(BTBBase):

    lines = ('btbxor','temp0','temp1',)

    def next_logic(self):

        if self.lines.temp0[0] >= 1 and self.lines.temp1[0] == 0:
            operation = 1
        elif self.lines.temp0[0] == 0 and self.lines.temp1[0] >= 1:
            operation = 1
        if self.lines.temp0[0] <= -1 and self.lines.temp1[0] == 0:
            operation = -1
        elif self.lines.temp0[0] == 0 and self.lines.temp1[0] <= -1:
            operation = -1
        else:
            operation = 0

        self.lines.btbxor[0] = self.b_standardise(operation)

class BTBXnor(BTBBase):

    lines = ('btbxnor','temp0','temp1',)

    def next_logic(self):

        if self.lines.temp0[0] >= 1 and self.lines.temp1[0] >= 1:
            operation = 1
        elif self.lines.temp0[0] == 0 and self.lines.temp1[0] == 0:
            operation = 1
        elif self.lines.temp0[0] <= -1 and self.lines.temp1[0] <= -1:
            operation = -1
        else:
            operation = 0

        self.lines.btbxnor[0] = self.b_standardise(operation)

class BTBNand(BTBBase):

    lines = ('btbnand','temp0','temp1',)

    def next_logic(self):

        if self.lines.temp0[0] >= 1 and self.lines.temp1[0] == 0:
            operation = 1
        elif self.lines.temp0[0] == 0 and self.lines.temp1[0] >= 1:
            operation = 1
        elif self.lines.temp0[0] <= 0 and self.lines.temp1[0] <= -1:
            operation = -1
        elif self.lines.temp0[0] == 0 and self.lines.temp1[0] == 0:
            operation = 1
        elif self.lines.temp0[0] <= -1 and self.lines.temp1[0] <= 0:
            operation = -1
        else:
            operation = 0

        self.lines.btbnand[0] = self.b_standardise(operation)

class BTBNor(BTBBase):

    lines = ('btbnor','temp0','temp1',)

    def next_logic(self):

        if self.lines.temp0[0] == 0 and self.lines.temp1[0] == 0:
            operation = 1
        else:
            operation = 0

        self.lines.btbnor[0] = self.b_standardise(operation)


class VTVCustom(enular.IndicatorOperation):

    lines = ('vtvcustom',)

    def init_logic(self):

        operation = self.data0 + self.data1
        self.lines.vtvcustom = operation


class VTBCrossover(enular.IndicatorOperation):

    lines = ('vtbcrossover',)

    def init_logic(self):

        upcross = indicators.CrossUp(self.data0, self.data1)
        downcross = indicators.CrossDown(self.data0, self.data1)
        operation = upcross - downcross
        self.lines.vtbcrossover = operation

class VTBCustom(BTBBase):

    lines = ('vtbcustom','temp0','temp1',)

    def next_logic(self):

        if self.lines.temp0[0] >= 0 and self.lines.temp1[0] >= 0:
            operation = 1
        else:
            operation = 0

        self.lines.vtbcustom[0] = self.b_standardise(operation)