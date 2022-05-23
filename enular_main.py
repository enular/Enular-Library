#!/usr/bin/env python
import os
import sys

from import_test import *

if __name__ == '__main__':
    print ('Do not run this file.')

#Make sure that file and dependencies are imported and functioning
class Test:
    
    a = 1

    def __init__(self):
        self.a = 2
    
    def test_the_test(self):
        print(self.a)
        test_function()

#Evaluation class placeholder, including visualisation
#Takes in strategy in as a parameter
class Evaluate:

    a = 1

    def __init__(self, strategy):
        self.a = 2
        self.evaluate(strategy)

    def evaluate(self, strategy):
        self.a = strategy

    def print_results(self):
        print(self.a)

    def print_graph(self):
        print(self.a)
        
#Strategy class placeholder
class Strategy:

    a = 1

    def __init__(self):
        self.a = 2

#Streamer class placeholder
class Streamer:
    
    a = 1

    def __init__(self):
        self.a = 2

#Indicator base class placeholder
class Indicator:
    
    a = 1

    def __init__(self):
        self.a = 2