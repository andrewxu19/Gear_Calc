#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from Class_Gear import *
from math import sin,cos,tan,acos

gp=Gear_Pair()  # initializate the gear pair
gp.name=input("please input gear pair number:")

# mn,z,z_mate,alpha_n,ha_n,c_n,beta,b,xn,xn_mate,i="e",hand="LH",a_modified=0
L=[2.5,19,31,20,1,0.25,18,40,0.1,0.2,"e","LH",0]
# L[10],indicate whether external / internal engagement

mn=L[0]
z1=L[1]
z2=L[2]

if z2<z1:   # ȷ��z1ΪС���֣�z2Ϊ�����
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

# �Ժ���ʹ�õĲ������г�ʼ�� parameter initialization for following usage
a=0             # ���ľ� cender distance
i1=""           # С�����Ƿ�Ϊ��ݡ��ڳݣ�"e"Ϊ��ݣ�"i"Ϊ�ڳ�
i2=""           # ������Ƿ�Ϊ��ݡ��ڳݣ�"e"Ϊ��ݣ�"i"Ϊ�ڳ�
at_modified=0   # ���Ͻ� engagement angle

if gp.i=="e":   # �ڡ���ݣ���������
    i1="e"
    i2="e"
    if hand1=="LH":
        hand2="RH"
    else:
        hand2="LH"
else:
    i1="e"
    i2="i"
    if hand1=="LH":
        hand2="LH"
    else:
        hand2="RH"

g1=Helix_Gear(mn, z1, z2, alpha_n, ha_n, c_n, beta, b, xn1, xn2, i1, hand1)  # С���ֳ�ʼ��
g2=Helix_Gear(mn, z2, z1, alpha_n, ha_n, c_n, beta, b, xn2, xn1, i2, hand2)  # ����ֳ�ʼ��

if a_modified==0:    # �Ѿ�xn1,xn2�����λ�����ľ� xn1,xn2 already known, to calculate a_modified
    if gp.i=="e":  # ��Ϊ������ external engagement
        gp.at_modified=ainv(2*(xn2+xn1)*tan(alpha_n)/(z2+z1)+inv(g1.alpha_t))
        gp.yt=(z2+z1)*(cos(g1.alpha_t)/cos(gp.at_modified)-1)/2
        gp.yn=gp.yt/cos(beta)
        gp.a_modified=mn*((z2+z1)/2+gp.yt)/cos(beta)
        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=xn2+xn1-gp.yn   # ���ľ�䶯ϵ����������ͳһ
    else:   # ��Ϊ������ internal engagement
        gp.at_modified=ainv(2*(xn2-xn1)*tan(alpha_n)/(z2-z1)+inv(g1.alpha_t))
        gp.yt=(z2-z1)*(cos(g1.alpha_t)/cos(gp.at_modified)-1)/2
        gp.yn=gp.yt/cos(beta)
        gp.a_modified=mn*((z2-z1)/2+gp.yt)/cos(beta)  # ��λ�����ľ�
        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=xn2-xn1-gp.yn   # ���ľ�䶯ϵ����������ͳһ     
else:    # ��֪��λ�����ľ࣬���λϵ�� a_modified already known, to calculate xn_sigma
    gp.a_modified=a_modified    # ��λ�����ľ�������
    if gp.i=="e":   # ��Ϊ������ external engagement
        gp.a=mn*(z1+z2)/2/cos(beta)
        gp.yt=(a_modified-a)/g1.mt
        gp.yn=(a_modified-a)/mn
        gp.at_modified=acos(a*cos(g1.alpha_t)/a_modified) # ���Ͻ� engagement angle
        gp.xn_sigma=(z2+z1)*(inv(gp.at_modified)-inv(g1.alpha_t))/2/tan(alpha_n)   # �ܱ�λϵ��

        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=gp.xn_sigma-gp.yn  # ���ľ�䶯ϵ����������ͳһ
        
    else:   # ��Ϊ������ internal engagement
        gp.a=mn*(z2-z1)/2/cos(beta)
        gp.yt=(a_modified-a)/g1.mt
        gp.yn=(a_modified-a)/mn
        gp.at_modified=acos(a*cos(g1.alpha_t)/a_modified) # ���Ͻ� engagement angle
        gp.xn_sigma=(z2-z1)*(inv(gp.at_modified)-inv(g1.alpha_t))/2/tan(alpha_n) # �ܱ�λϵ��

        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=xn_sigma-yn  # ���ľ�䶯ϵ����������ͳһ

g1.para_calc()  # ����С���������ľ��λϵ����صĳ��ֲ�������ݶ�Բ���ݸ�Բ�������ľ��λϵ����صĳ��ֲ�������ݶ�Բ���ݸ�Բ�� calculate other parameters related to delta_y_n of gear1
g2.para_calc()  # �������������ľ��λϵ����صĳ��ֲ�������ݶ�Բ���ݸ�Բ�� calculate other parameters related to delta_y_n of gear2

if gp.i=="e":   # ������
    gp.d1_modified=2*a_modified*z1/(z2+z1) # С���ֽ�Բֱ�� pitch diameter of gear1
    gp.d2_modified=2*a_modified*z2/(z2+z1) # ����ֽ�Բֱ�� pitch diameter of gear2
    gp.Epix_a=(z1*(tan(g1.alpha_at)-tan(gp.at_modified))+z2*(tan(g2.alpha_at)-tan(g2.alpha_t)))/2/pi # �����غ϶� face overlap ratio
else:   # ������
    gp.d1_modified=2*a_modified*z1/(z2-z1) # pitch diameter of gear1
    gp.d2_modified=2*a_modified*z2/(z2-z1) # pitch diameter of gear2
    gp.Epix_a=(z1*(tan(g1.alpha_at)-tan(gp.at_modified))-z2*(tan(g2.alpha_at)-tan(g2.alpha_t)))/2/pi # �����غ϶� face overlap ratio  

gp.Epix_b=b*sin(beta)/mn/pi    # �����غ϶� axial overlap ratio
gp.Epix_gama=gp.Epix_a+gp.Epix_b     # ���غ϶� total overlap ratio    

# the following will check the engagement quality 

