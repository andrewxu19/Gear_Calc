#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from Class_Gear import *
from Optimism import *
from math import sin,cos,tan,acos,sqrt

gp=Gear_Pair()  # gear pair initialization
gp.name=input("please input gear pair number:")

# mn,z,z_mate,alpha_n,ha_n,c_n,beta,b,xn,xn_mate,i="e",hand="LH",a_modified=0
L=[2.5,19,31,20,1,0.25,18,40,0.1,0.2,"e","LH",0]
# L[10],indicate whether external / internal engagement

mn=L[0]
z1=L[1]
z2=L[2]

if z2<z1:   # to check whether z2 must be greater than z1
    print("Z2 should be greater than Z1, please change the parameter.")
    exit(None)

alpha_n=L[3]
ha_n=L[4]
c_n=L[5]
beta=L[6]
b=L[7]
xn1=L[8]
xn2=L[9]

if xn1<0:
    print("the modification factor of gear1 should be greater than 0, please change the parameter.")
    exit(None)

gp.i=L[10]        # indication of external / internal gear
hand1=L[11]
a_modified=L[12]

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

g1=Helix_Gear(mn, z1, z2, alpha_n, ha_n, c_n, beta, b, xn1, xn2, i1, hand1)  # gear1 initialization
g2=Helix_Gear(mn, z2, z1, alpha_n, ha_n, c_n, beta, b, xn2, xn1, i2, hand2)  # gear2 initialization

if a_modified==0:    # if xn1,xn2 already known, to calculate a_modified
    if gp.i=="e":  # if external engagement
        gp.at_modified=ainv(2*(xn2+xn1)*tan(alpha_n)/(z2+z1)+inv(g1.alpha_t))
        gp.yt=(z2+z1)*(cos(g1.alpha_t)/cos(gp.at_modified)-1)/2
        gp.yn=gp.yt/cos(beta)
        gp.a_modified=mn*((z2+z1)/2+gp.yt)/cos(beta)
        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=xn2+xn1-gp.yn   # center distance modification factor
    else:   # if internal engagement
        gp.at_modified=ainv(2*(xn2-xn1)*tan(alpha_n)/(z2-z1)+inv(g1.alpha_t))
        gp.yt=(z2-z1)*(cos(g1.alpha_t)/cos(gp.at_modified)-1)/2
        gp.yn=gp.yt/cos(beta)
        gp.a_modified=mn*((z2-z1)/2+gp.yt)/cos(beta)  # center distance modified
        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=xn2-xn1-gp.yn   # center distance modification factor     
else:    # if a_modified (center distance modified) already known, to calculate xn_sigma and distribute xn between gears
    gp.a_modified=a_modified    # gear pair property assignment
    if gp.i=="e":   # if external engagement
        gp.a=mn*(z1+z2)/2/cos(beta)
        gp.yt=(a_modified-a)/g1.mt
        gp.yn=(a_modified-a)/mn
        gp.at_modified=acos(a*cos(g1.alpha_t)/a_modified) # engagement angle
        gp.xn_sigma=(z2+z1)*(inv(gp.at_modified)-inv(g1.alpha_t))/2/tan(alpha_n)   # total modification coefficiency

        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=gp.xn_sigma-gp.yn  # center distance modification factor

        x_distribute(g1,g2,gp,index)  # xn1, xn2 distribution, the parameter should be a class object
        
    else:   # if internal engagement
        gp.a=mn*(z2-z1)/2/cos(beta)
        gp.yt=(a_modified-a)/g1.mt
        gp.yn=(a_modified-a)/mn
        gp.at_modified=acos(a*cos(g1.alpha_t)/a_modified) # engagement angle
        gp.xn_sigma=(z2-z1)*(inv(gp.at_modified)-inv(g1.alpha_t))/2/tan(alpha_n) # total modification coefficiency

        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=xn_sigma-yn  # center distance modification factor
            
        x_distribute(g1,g2,gp,index)  # xn1, xn2 distribution, the parameter should be a class object
       

            
        



if gp.i=="e":   # if external engagement
    gp.d1_modified=2*a_modified*z1/(z2+z1) # pitch diameter of gear1
    gp.d2_modified=2*a_modified*z2/(z2+z1) # pitch diameter of gear2
    gp.Epix_a=(z1*(tan(g1.alpha_at)-tan(gp.at_modified))+z2*(tan(g2.alpha_at)-tan(g2.alpha_t)))/2/pi    # face overlap ratio
else:   # if internal engagement
    gp.d1_modified=2*a_modified*z1/(z2-z1) # pitch diameter of gear1
    gp.d2_modified=2*a_modified*z2/(z2-z1) # pitch diameter of gear2
    gp.Epix_a=(z1*(tan(g1.alpha_at)-tan(gp.at_modified))-z2*(tan(g2.alpha_at)-tan(g2.alpha_t)))/2/pi    # face overlap ratio  

gp.Epix_b=b*sin(beta)/mn/pi    # axial overlap ratio
gp.Epix_gama=gp.Epix_a+gp.Epix_b     # total overlap ratio    

# the following will check whether there have interference between tip circle of gear2 and root transit curve of gear1
if gp.i=="e":
    gp.rho=g1.mt*(z1*sin(g1.alpha_t)/2-(g1.ha_t-g1.xt)/sin(g1.alpha_t))
    if g2.da<sqrt(g2.db^2+(2*a_modified*sin(gp.at_modified)+2*gp.rho)^2):
        gp.transit_curve="interferenced, please check the parameter and reselect the xn1"
        exit()
    else:
        gp.transit_curve="no interference with tip circle of gear2 at transit curve of gear1"
else:
    print("test")





