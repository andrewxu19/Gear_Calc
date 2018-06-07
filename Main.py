#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from Class_Gear import *
from Optimism import *
from math import sin,cos,tan,acos

gp=Gear_Pair()  # initializate the gear pair
gp.name=input("please input gear pair number:")

# mn,z,z_mate,alpha_n,ha_n,c_n,beta,b,xn,xn_mate,i="e",hand="LH",a_modified=0
L=[2.5,19,31,20,1,0.25,18,40,0.1,0.2,"e","LH",0]
# L[10],indicate whether external / internal engagement

mn=L[0]
z1=L[1]
z2=L[2]

if z2<z1:   # 确保z1为小齿轮，z2为大齿轮
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

# 对后续使用的参数进行初始化 parameter initialization for following usage
a=0             # 中心距 cender distance
i1=""           # 小齿轮是否为外齿、内齿，"e"为外齿，"i"为内齿
i2=""           # 大齿轮是否为外齿、内齿，"e"为外齿，"i"为内齿
at_modified=0   # 啮合角 engagement angle

if gp.i=="e":   # 内、外齿，旋向区分
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

g1=Helix_Gear(mn, z1, z2, alpha_n, ha_n, c_n, beta, b, xn1, xn2, i1, hand1)  # 小齿轮初始化
g2=Helix_Gear(mn, z2, z1, alpha_n, ha_n, c_n, beta, b, xn2, xn1, i2, hand2)  # 大齿轮初始化

if a_modified==0:    # 已经xn1,xn2，求变位后中心距 xn1,xn2 already known, to calculate a_modified
    if gp.i=="e":  # 如为外啮合 external engagement
        gp.at_modified=ainv(2*(xn2+xn1)*tan(alpha_n)/(z2+z1)+inv(g1.alpha_t))
        gp.yt=(z2+z1)*(cos(g1.alpha_t)/cos(gp.at_modified)-1)/2
        gp.yn=gp.yt/cos(beta)
        gp.a_modified=mn*((z2+z1)/2+gp.yt)/cos(beta)
        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=xn2+xn1-gp.yn   # 中心距变动系数，并保持统一
    else:   # 如为内啮合 internal engagement
        gp.at_modified=ainv(2*(xn2-xn1)*tan(alpha_n)/(z2-z1)+inv(g1.alpha_t))
        gp.yt=(z2-z1)*(cos(g1.alpha_t)/cos(gp.at_modified)-1)/2
        gp.yn=gp.yt/cos(beta)
        gp.a_modified=mn*((z2-z1)/2+gp.yt)/cos(beta)  # 变位后中心距
        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=xn2-xn1-gp.yn   # 中心距变动系数，并保持统一     
else:    # 已知变位后中心距，求变位系数 a_modified already known, to calculate xn_sigma
    gp.a_modified=a_modified    # 变位后中心距存入对象
    if gp.i=="e":   # 如为外啮合 external engagement
        gp.a=mn*(z1+z2)/2/cos(beta)
        gp.yt=(a_modified-a)/g1.mt
        gp.yn=(a_modified-a)/mn
        gp.at_modified=acos(a*cos(g1.alpha_t)/a_modified) # 啮合角 engagement angle
        gp.xn_sigma=(z2+z1)*(inv(gp.at_modified)-inv(g1.alpha_t))/2/tan(alpha_n)   # 总变位系数
        
        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=gp.xn_sigma-gp.yn  # 中心距变动系数，并保持统一
        
        # 变位系数的分配及校核
        # 注意，只有分配后，才能进行单个齿轮的详细计算
        x=x_distribute()
        
        g1.xn=g2.xn_mate=x[0]
        g2.xn=g1.xn_mate=x[1]
        
        
        
        
    else:   # 如为内啮合 internal engagement
        gp.a=mn*(z2-z1)/2/cos(beta)
        gp.yt=(a_modified-a)/g1.mt
        gp.yn=(a_modified-a)/mn
        gp.at_modified=acos(a*cos(g1.alpha_t)/a_modified) # 啮合角 engagement angle
        gp.xn_sigma=(z2-z1)*(inv(gp.at_modified)-inv(g1.alpha_t))/2/tan(alpha_n) # 总变位系数

        gp.delta_y_n=g1.delta_y_n=g2.delta_y_n=xn_sigma-yn  # 中心距变动系数，并保持统一

        # 变位系数的分配及校核
        # 注意，只有分配后，才能进行单个齿轮的详细计算
        x=x_distribute()
        
        g1.xn=g2.xn_mate=x[0]
        g2.xn=g1.xn_mate=x[1]  
        

g1.para_calc()  # 计算小齿轮与中心距变位系数相关的齿轮参数，如齿顶圆、齿根圆等与中心距变位系数相关的齿轮参数，如齿顶圆、齿根圆等 calculate other parameters related to delta_y_n of gear1
g2.para_calc()  # 计算大齿轮与中心距变位系数相关的齿轮参数，如齿顶圆、齿根圆等 calculate other parameters related to delta_y_n of gear2

if gp.i=="e":   # 外啮合
    gp.d1_modified=2*a_modified*z1/(z2+z1) # 小齿轮节圆直径 pitch diameter of gear1
    gp.d2_modified=2*a_modified*z2/(z2+z1) # 大齿轮节圆直径 pitch diameter of gear2
    gp.Epix_a=(z1*(tan(g1.alpha_at)-tan(gp.at_modified))+z2*(tan(g2.alpha_at)-tan(g2.alpha_t)))/2/pi # 端面重合度 face overlap ratio
else:   # 内啮合
    gp.d1_modified=2*a_modified*z1/(z2-z1) # 小齿轮节圆直径 pitch diameter of gear1
    gp.d2_modified=2*a_modified*z2/(z2-z1) # 大齿轮节圆直径 pitch diameter of gear2
    gp.Epix_a=(z1*(tan(g1.alpha_at)-tan(gp.at_modified))-z2*(tan(g2.alpha_at)-tan(g2.alpha_t)))/2/pi # 端面重合度 face overlap ratio  

gp.Epix_b=b*sin(beta)/mn/pi    # 轴向重合度 axial overlap ratio
gp.Epix_gama=gp.Epix_a+gp.Epix_b     # 总重合度 total overlap ratio    

# the following will check the engagement quality

