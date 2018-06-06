#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from Class_Gear import *
from math import sin,cos,tan,acos

gp=Gear_Pair()  # initializate the gear pair
gp.name=input("please input gear pair number")

# mn,z,z_mate,alpha_n,ha_n,c_n,beta,b,xn,xn_mate,i="e",hand="LH",a_modified=0
L=[2.5,19,31,20,1,0.25,18,40,0.1,0.2,"e","LH",0]
# L[10],indicate whether external / internal engagement

mn=L[0]
z1=L[1]
z2=L[2]

if z2>z1:
    print("Z2 should be greater than Z1")
    exit(None)

alpha_n=L[3]
ha_n=L[4]
c_n=L[5]
beta=L[6]
b=L[7]
xn1=L[8]
xn2=L[9]
gp.i=L[10]        # indication of external / internal gear
hand1=L[11]
a_modified=L[12]

# parameter initialization for following usage
a=0             # cender distance
i1=""
i2=""
at_modified=0   # engagement angle

if gp.i=="e":
    i1="e"
    i2="e"
    if hand1="LH":
        hand2="RH"
    else:
        hand2="LH"
else:
    i1="e"
    i2="i"
    if hand1="LH":
        hand2="LH"
    else:
        hand2="RH"

g1=Helix_Gear(mn, z1, z2, alpha_n, ha_n, c_n, beta, b, xn1, xn2, i1, hand1, delta_y_n)
g2=Helix_Gear(mn, z2, z1, alpha_n, ha_n, c_n, beta, b, xn2, xn1, i2, hand2, delta_y_n)

if a_modified==0:
    # xn1,xn2 already known, to calculate a_modified
    if gp.i=="e":  # external engagement
        at_modified=ainv(2*(xn2+xn1)*tan(alpha_n)/(z2+z1)+inv(g1.alpha_t))
        yt=(z2+z1)*(cos(g1.alpha_t)/cos(at_modified)-1)/2
        yn=yt/cos(beta)
        a_modified=mn*((z2+z1)/2+yt)/cos(beta)
        g1.delta_y_n=g2.delta_y_n=xn2+xn1-yn
    else:   #internal engagement
        at_modified=ainv(2*(xn2-xn1)*tan(alpha_n)/(z2-z1)+inv(g1.alpha_t))
        yt=(z2-z1)*(cos(g1.alpha_t)/cos(at_modified)-1)/2
        yn=yt/cos(beta)
        a_modified=mn*((z2-z1)/2+yt)/cos(beta)
        g1.delta_y_n=g2.delta_y_n=xn2-xn1-yn        
else:
    # a_modified already known, to calculate xn_sigma
    if gp.i=="e":   # external engagement
        gp.a=mn*(z1+z2)/2/cos(beta)
        gp.yt=(a_modified-a)/g1.mt
        gp.yn=(a_modified-a)/mn
        gp.at_modified=acos(a*cos(alpha_t)/a_modified) # engagement angle
        gp.xn_sigma=(z2+z1)*(inv(at_modified)-inv(g1.alpha_t))/2/tan(alpha_n)

        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=xn_sigma-yn
        
    else:   # internal engagement
        gp.a=mn*(z2-z1)/2/cos(beta)
        gp.yt=(a_modified-a)/g1.mt
        gp.yn=(a_modified-a)/mn
        gp.at_modified=acos(a*cos(alpha_t)/a_modified) # engagement angle
        gp.xn_sigma=(z2-z1)*(inv(at_modified)-inv(g1.alpha_t))/2/tan(alpha_n)

        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=xn_sigma-yn

g1.para_calc()  # calculate other parameters related to delta_y_n of gear1
g2.para_calc()  # calculate other parameters related to delta_y_n of gear2

if i="e":
    gp.d1_modified=2*a_modified*z1/(z2+z1) # pitch diameter of gear1
    gp.d2_modified=2*a_modified*z2/(z2+z1) # pitch diameter of gear2
    gp.Epix_a=(z1*(tan(g1.alpha_at)-tan(at_modified))+z2*(tan(g2.alpha_at)-tan(alpha_t)))/2/pi # face overlap ratio
else:
    gp.d1_modified=2*a_modified*z1/(z2-z1) # pitch diameter of gear1
    gp.d2_modified=2*a_modified*z2/(z2-z1) # pitch diameter of gear2
    gp.Epix_a=(z1*(tan(g1.alpha_at)-tan(at_modified))-z2*(tan(g2.alpha_at)-tan(alpha_t)))/2/pi # face overlap ratio  

gp.Epix_b=b*sin(beta)/mn/pi    # axial overlap ratio
gp.Epix_gama=Epix_a+Epix_b     # total overlap ratio    

# the following will check the engagement quality

