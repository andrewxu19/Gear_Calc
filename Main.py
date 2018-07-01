#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# test, for internal engagement, not finished

from Class_Gear import *
from math import sin,cos,tan,acos,sqrt
import sys


input1=sys.open("") # 从文件读取参数
test=0

# mn,z,z_mate,alpha_n,ha_n,c_n,beta,b,xn,xn_mate,i="e",hand="LH",a_modified=0
L=[2.5,19,31,20,1,0.25,18,40,0,0,"e","LH",66.4]
# L[10],indicate whether external / internal engagement

gp=Gear_Pair()  # gear pair initialization
# gp.name=input("please input gear pair number:")
gp.mn=mn=L[0]
gp.z1=z1=L[1]
gp.z2=z2=L[2]

if z2<z1:   # to check whether z2 must be greater than z1
    print("Z2 should be greater than Z1, please change the parameter.")
    exit(None)

gp.alpha_n=alpha_n=radians(L[3])
gp.ha_n=ha_n=L[4]
gp.c_n=c_n=L[5]
gp.beta=beta=radians(L[6])
gp.b=b=L[7]
gp.xn1=xn1=L[8]
gp.xn2=xn2=L[9]

if xn1<0:
    print("the modification factor of gear1 should be equal or greater than 0, please change the parameter.")
    exit(None)

gp.i=L[10]        # indication of external / internal gear
hand1=L[11]
gp.a_modified=a_modified=L[12]

# parameter initialization for following usage
a=0             # cender distance
i1=""           # external / internal gear, "e" for external, "i" for internal
i2=""           # external / internal gear, "e" for external, "i" for internal
at_modified=0   # engagement angle

if gp.i=="e":   # external engagement
    i1="e"      # gear1 is an external gear
    i2="e"      # gear2 is an external gear
    if hand1=="LH": # helix angle of gear1 is left hand
        hand2="RH"  # helix angle of gear2 is right hand
    else:
        hand2="LH"
else:
    i1="e"      # gear1 is an external gear
    i2="i"      # gear2 is an internal gear
    if hand1=="LH":
        hand2="LH"
    else:
        hand2="RH"

gp.para_calc() # calculate basic parameter of gp

g1=Helix_Gear(mn, z1, z2, alpha_n, ha_n, c_n, beta, b, xn1, xn2, gp.delta_y_n,i1, hand1)  # gear1 initialization
g2=Helix_Gear(mn, z2, z1, alpha_n, ha_n, c_n, beta, b, xn2, xn1, gp.delta_y_n,i2, hand2)  # gear2 initialization

if gp.xn1!=0 or gp.xn2!=0:  #the modificaiton factor already been distributed
    g1.para_calc()
    g2.para_calc()
    
    g1.gear_quality_check()
    g2.gear_quality_check()
    if g1.undercut!="":
        print(g1.undercut)
        exit(0)
    elif g1.sharpen!="":
        print(g1.sharpen)
        exit(0)
else:
    gp.x_distribute(g1, g2, 1) # 变位系数分配 modification factor distribution

gp.advance_calc(g1,g2)  # 节圆及重合度计算

gp.slip_ratio(g1,g2)    # 最大滑动率计算

write2file(gp, g1, g2)  # write the result to a file

print("test sucess",gp.eta1,gp.eta2)

# the following will check whether there have interference between tip circle of gear2 and root transit curve of gear1






