#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from math import sin,cos,tan,degrees,radians,pow,sqrt,pi,acos,asin,atan

class Helix_Gear(object):
# should download ISO1122 or DIN3960 for the English terms of all the parameter name
    
    def __init__(self,mn,z,z_mate,i="e",hand="LH",alpha_n,ha_n,c_n,beta,b,xn,xn_mate,delta_y_n=0):
        # basic parameter of gear, i represents internal or external gear of the gear pair.  	
        self.mn=mn                    # 法向模数 section gear modules 
        self.z=z                      # 齿数 tooth number 
        self.z_mate=z_mate            # tooth number of mated gear
        self.i=i	              # 内齿"i"或外齿"e" internal or external gear 
        self.hand=hand	              # 旋向，LH左旋，RH右旋 helix direction 
        self.alpha_n=radians(alpha_n) # 法向分度圆压力角，转換为弧度 section pressure angle at reference diameter, units in deg 
        self.ha_n=ha_n                # 法向齿顶高系数 tip height coefficient 
        self.c_n=c_n                  # 法向顶隙系数 tip gap coefficient 
        self.beta=radians(beta)       # 螺旋角，转換为弧度 helix angle, units in deg， and has been transformed to radians
        self.rho_fp=0.38              # 齿根过渡圆角系数 root radius coeffient 
        self.b=b                      # 齿宽 gear width 
        self.xn=xn                    # 法向变位系数 section profile shift coefficient 
        self.xn_mate=xn_mate          # 配对齿轮法向变位系数 section profile shift coefficient of mated gear
        self.delta_y_n=delta_y_n      # 中心距变动系数 modification factor of center distance 

    # Process information
        self.mat="20MnCr5"          # 齿轮材料 gear material 
        self.HT="Carbonitriding"    # 热处理 Heat Treatment 
        self.hardness="50~56HRC"    # 硬度 hardness of the gear 

    def para_calc(self):
        # basic parameter calculate
        self.mt=self.mn/cos(self.beta)		        	# 端面模数 face module 
        self.alpha_t=atan(tan(self.alpha_n)/cos(self.beta))	# 端面分度圆压力角 face pressure angle at reference circle  
        self.xt=self.xn*cos(self.beta)                          # 端面变位系数 face profile shift coefficient
        self.ha_t=self.ha_n*cos(self.beta)                      # 端面齿顶高系数 face tip height coefficient
        self.c_t=self.c_n*cos(self.beta)                        # 端面顶隙系数 face tip gap coefficient
        
        self.d=self.mt*self.z                        	        # 分度圆直径 reference diameter 
        
        self.db=self.d*cos(self.alpha_t)			# 基圆直径 base circle diameter
        self.beta_b=atan(self.db*tan(self.beta)/self.d)         # helix angle at base circle        
        
        if self.i== "e":
            self.tip_height=(self.ha+self.xn-self.delta_y_n)*self.mn   # 外齿 齿顶高tip height for external gear
            self.root_height=(self.ha+self.c-self.xn)*self.mn  	# 外齿 齿根高 root height for external gear
            self.da=self.d+2*self.tip_height			# 外齿 齿顶圆直径 tip diameter for external gear 
            self.df=self.d-2*self.root_height			# 外齿 齿根圆直径 root diameter for external gear 
        elif self.i=="i":
            self.tip_height=(self.ha-self.xn+self.delta_y_n)*self.mn   # 内齿 齿顶高 tip height for internal gear
            self.root_height=(self.ha+self.c+self.xn)*self.mn  	# 内齿 齿根高 root height for internal gear
            self.da=self.d-2*self.tip_height			# 内齿 齿顶圆直径 tip diameter for internal gear 
            self.df=self.d+2*self.root_height			# 内齿 齿根圆直径 root diameter for internal gear 
        else:
            print("gear type not defined")
        
        self.height=self.tip_height+self.root_height    	# 全齿高full tooth height 
        
        self.alpha_at=acos(self.db/self.da)			# 齿顶圆压力角 tip circle pressure angle 
        self.beta_a=atan(self.da*tan(self.beta)/self.d)         # 齿顶圆螺旋角，任意圆螺旋角需更換齿顶圆直径参数 helix angle at tip circle, for helix angle at any diameter should replace the parameter self.da
        


    def advance_calc(self):
    # advanced calculation for parameters not frequently used
        self.tooth_pitch=self.mt*pi                     # 齿距 tooth pitch
        self.st=pi*self.mt/2                            # 分度圆齿厚 tooth thickness at reference circle
        self.st_a=                                      # 齿顶圆齿厚 tooth thickness at tip circle
        
        self.z_v=self.z/(cos(self.beta_b)^2*cos(self.beta)) # equivalent tooth number

    def gear_quality_check(self):
    # check the gear quality, eg. undercut, tip sharpen, sliding rate, root pressure ratio
        test=0

    def bend_strength_calc(self):
    # check the bending strength
        test=0

    def contact_strength_calc(self):
    #check contact strength
        test=0

    def pitting_calc(self):
    # check pitting
        test=0

    def tolerance_calc(self):
    # calculate tolerance of the gear
        test=0

def inv(alpha):
    # involute function, alpha should be in radians
    return tan(alpha)-alpha

def ainv(value):
    # function to calculate the angle in radians
    return 0