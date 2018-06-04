#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from math import sin,cos,tan,degrees,radians,pow,sqrt,pi,acos,asin,atan

class Helix_Gear(object):
# should download ISO1122 or DIN3960 for the English terms of all the parameter name
    
    def __init__(self,mn,z,i="e",hand="LH",alpha_n,ha_n,c_n,beta,b,xn,delta_y_n=0):
        # basic parameter of gear, i represents internal or external engagement of the gear pair.  	
        self.mn=mn                    # section gear modules 法向模数
        self.z=z                      # tooth number 齿数
        self.i=i	              # internal or external engagement 内啮合"i"或外啮合"e"
        self.hand=hand	              # helix direction 旋向，LH左旋，RH右旋
        self.alpha_n=radians(alpha_n)      # section pressure angle at reference diameter, units in deg 法向分度圆压力角
        self.ha_n=ha_n                   # tip height coefficient 法向齿顶高系数
        self.c_n=c_n                # tip gap coefficient 法向顶隙系数
        self.beta=radians(beta)         # helix angle, units in deg 螺旋角，单位角度
        self.rho_fp=0.38              # root radius coeffient 齿根过渡圆角系数
        self.b=b                      # gear width 齿宽
        self.xn=xn                     # section profile shift coefficient 法向变位系数
        self.delta_y_n=delta_y_n      # 

    # Process information
        self.mat="20MnCr5"          # gear material 齿轮材料
        self.HT="Carbonitriding"    # Heat Treatment 热处理
        self.hardness="50~56HRC"    # hardness of the gear 硬度

    def para_calc(self):
        # basic parameter calculate
        self.mt=self.mn/cos(self.beta)		        	# face module 端面模数
        self.alpha_t=atan(tan(self.alpha_n)/cos(self.beta))	# face pressure angle at reference circle  端面分度圆压力角
        self.xt=self.xn*cos(self.beta)                          # face profile shift coefficient端面变位系数
        self.ha_t=self.ha_n*cos(self.beta)                      # face tip height coefficient端面齿顶高系数
        self.c_t=self.c_n*cos(self.beta)                        # face tip gap coefficient端面顶隙系数
        
        self.d=self.mt*self.z                        	        # reference diameter 分度圆直径
        
        #self.tip_height=(self.ha+self.xn)*self.mn               # tip height 齿顶高
        #self.root_height=(self.ha+self.c-self.xn)*self.mn  	# root height 齿根高
        #self.height=self.tip_height+self.root_height    	# full tooth height 全齿高
        
        if self.i== "e":
            self.da=self.d+2*self.tip_height			# tip diameter for external engagement 外啮合 齿顶圆直径
            self.df=self.d-2*self.root_height			# root diameter for external engagement 外啮合 齿根圆直径
        elif self.i=="i":
            self.da=self.d-2*self.tip_height			# tip diameter for internal engagement 内啮合 齿顶圆直径
            self.df=self.d+2*self.root_height			# root diameter for internal engagement 内啮合 齿根圆直径
        else:
            print("engagement type not defined")

        self.alpha_at=acos(self.db/self.da)			# tip circle pressure angle 齿顶圆压力角
           
        self.db=self.d*cos(self.alpha_t)			# base diameter 基圆直径
        
        self.beta_a=atan(self.da*tan(self.beta)/self.d)         # helix angle at tip circle
        


    def advance_calc(self):
    # advanced calculation for parameters not frequently used
        self.tooth_pitch=self.mt*pi                     # tooth pitch
        self.st=pi*self.mt/2                            # tooth thickness at reference circle
      
      
        self.e_alpha=
        self.e_beta=
        self.e_gamma=self.e_alpha+self.e_beta		# total overlap ratio 总重合度

    def gear_quality_check(self):
    # check the engagement quality, eg. undercut, tip sharpen, sliding rate, root pressure ratio
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