#!/usr/bin/env python3
#-*- coding:utf-8 -*-

class Helix_Gear(object):

# module and gear number    
    def __init__(self,mn,z):
        self.mn=mn          # section gear modules
        self.z=z            # tooth number
        self.alphan=20      # section pressure angle at reference diameter, units in deg
        self.ha=1           # tip height coefficient
        self.c=0.25         # tip gap coefficient
        self.beta=0         # helix angle, units in deg
        self.rho_fp=0.38    # root radius coeffient
        self.b=0            # gear width
        self.xn=0           # section profile shift coefficient
        
        # Process information
        self.mat="20MnCr5"          # gear material
        self.HT="Carbonitriding"    # Heat Treatment
        self.hardness="50~56HRC"    # hardness of the gear


# basic parameter calculate

    def para_calc(self):
        self.d=self.mn*self.z                           # reference diameter
        self.tip_height=self.ha*self.mn                 # tip height
        self.root_height=self.c*self.mn                 # root height
        self.height=self.tip_height+self.root_height    # full tooth height

# test        
    def test(self):
        print('hello, these are %s eee' % "dd")

g1=Helix_Gear(2.5,35)
g1.para_calc()
g1.test()
