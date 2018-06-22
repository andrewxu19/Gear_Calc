#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from math import sin,cos,tan,degrees,radians,pow,sqrt,pi,acos,asin,atan,sqrt

class Helix_Gear(object):
    # should download ISO1122 or DIN3960 for the English terms of all the parameter name
    
    def __init__(self,mn,z,z_mate,alpha_n,ha_n,c_n,beta,b,xn,xn_mate,i="e",hand="LH",delta_y_n=0):
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
        
        self.mt=self.mn/cos(self.beta)		                 	# 端面模数 face module 
        self.alpha_t=atan(tan(self.alpha_n)/cos(self.beta))	    # 端面分度圆压力角 face pressure angle at reference circle  
        self.xt=self.xn*cos(self.beta)                          # 端面变位系数 face profile shift coefficient
        self.ha_t=self.ha_n*cos(self.beta)                      # 端面齿顶高系数 face tip height coefficient
        self.c_t=self.c_n*cos(self.beta)                        # 端面顶隙系数 face tip gap coefficient
        
        self.d=self.mt*self.z                        	        # 分度圆直径 reference diameter 
        
        self.db=self.d*cos(self.alpha_t)			# 基圆直径 base circle diameter
        self.beta_b=atan(self.db*tan(self.beta)/self.d)         # 基圆螺旋角 helix angle at base circle   
        
        self.x_min=self.ha_n-self.z*sin(self.alpha_n)^2     # minimum modificatin factor for the gear
        
        self.undercut=""
        self.tipcut=""
        self.sharpen=""
        
    # Process information
        self.mat="20MnCr5"          # 齿轮材料 gear material 
        self.HT="Carbonitriding"    # 热处理 Heat Treatment 
        self.hardness="50~56HRC"    # 硬度 hardness of the gear 
        
    def para_calc(self):
        # basic parameter calculate
       
        if self.i== "e":    # 外齿 external gear
            self.tip_height=(self.ha_n+self.xn-self.delta_y_n)*self.mn   # 外齿 齿顶高tip height for external gear
            self.root_height=(self.ha_n+self.c_n-self.xn)*self.mn  	# 外齿 齿根高 root height for external gear
            self.da=self.d+2*self.tip_height			# 外齿 齿顶圆直径 tip diameter for external gear 
            self.df=self.d-2*self.root_height			# 外齿 齿根圆直径 root diameter for external gear 
        else:   # 内齿 internal gear
            self.tip_height=(self.ha_n-self.xn+self.delta_y_n)*self.mn   # 内齿 齿顶高 tip height for internal gear
            self.root_height=(self.ha_n+self.c_n+self.xn)*self.mn  	# 内齿 齿根高 root height for internal gear
            self.da=self.d-2*self.tip_height			# 内齿 齿顶圆直径 tip diameter for internal gear 
            self.df=self.d+2*self.root_height			# 内齿 齿根圆直径 root diameter for internal gear 
       
        self.height=self.tip_height+self.root_height    	# 全齿高full tooth height 
        
        self.alpha_at=acos(self.db/self.da)			# 齿顶圆压力角 tip circle pressure angle 
        self.beta_a=atan(self.da*tan(self.beta)/self.d)         # 齿顶圆螺旋角，任意圆螺旋角需更換齿顶圆直径参数 helix angle at tip circle, for helix angle at any diameter should replace the parameter self.da
        
        return 0

    def advance_calc(self):
    # advanced calculation for parameters not frequently used
        self.tooth_pitch=self.mt*pi                     # 齿距 tooth pitch
        self.st=pi*self.mt/2                            # 分度圆齿厚 tooth thickness at reference circle
        #self.st_a=                                      # 齿顶圆齿厚 tooth thickness at tip circle
        
        self.z_v=self.z/(cos(self.beta_b)^2*cos(self.beta)) # 当量齿数Zv, equivalent tooth number

    def gear_quality_check(self):
        # check the gear quality, eg. undercut, tip sharpen, sliding rate, root pressure ratio
        
        # undercut check        
        z_min=2*self.ha/sin(self.alpha_n)^2
        if self.z<z_min:
            self.undercut="too less tooth number, please check and re-enter the parameter"
        
        # tip cut check
        
        self.tipcut=""
        # tip sharpen check
        
        self.sharpen=""

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
    
        # calculate the common normal length
        temp=self.z*inv(self.alpha_t)/inv(self.alpha_n)
        self.k=round(temp/pi*(sqrt((1+2*self.xn/temp)^2-cos(self.alpha_n)^2)/cos(self.alpha_n)-2*self.xn*tan(
            self.alpha_n)/temp-inv(self.alpha_n))+0.5) # number of teeth when measuring
        
        self.w_asterisk=cos(self.alpha_n)*(pi*(self.k-0.5)+temp*inv(self.alpha_n))
        self.w_delta=2*self.xn*sin(self.alpha_n)
        
        self.w_n=(self.w_asterisk+self.w_delta)*self.mn  # common normal length
        
        

def inv(alpha):
    # 渐开线函数，参数弧度 involute function, alpha should be in radians
    return tan(alpha)-alpha

def ainv(value):
    # 渐开线反函数，输出弧度 function to calculate the angle corresponding to involute spline, units in radians
    R1=0                                # 起始角度0deg/rad
    R2=radians(90)                      # 直接转换为弧度
    mate=(R2-R1)*0.6180339887498+R1     # 黄金分割法寻优 
    THRESHOLD=1E-9                      # 精度阈值
    
    while 1:
        eva1=inv(mate)-value
    
        if eva1 > THRESHOLD:
            R2=mate
            mate=(R2-R1)*0.389660112502+R1
        elif eva1<0:
            R1=mate
            mate=(R2-R1)*0.6180339887498+R1
        else:
            return mate
                   
    return 0

class Gear_Pair(object):
    # 齿轮对的参数存放于此类中 gear pair class to store gear pair information, including quality information
    
    def __init__(self):
        self.name=""        # gear pair name
        self.overlap=""     #
        self.i=""           # external / internal engagement
        self.d1_modified=0  # pitch diameter of gear1
        self.d2_modified=0  # pitch diameter of gear2
        self.Epix_a=0       # face overlap ratio
        self.Epix_b=0       # axial overlap ratio
        self.Epix_gama=0    # total overlap ratio
        self.a=0            # theoretical center distance
        self.a_modified=0   # modified center distance (actual center distance) 
        self.at_modified=0  # engagement angle
        self.xn_sigma=0 # total modification factor
        self.yn=0
        self.yt=0
        self.delta_y_n=0
        self.rho=0
        self.eta1=0     # slip ratio of gear1
        self.eta2=0     # slip ratio of gear2
        
        self.transit_curve=""   # store the status of the transit curve of gear1
        
    def x_distribute(self,g1,g2,index):
            # distribution of xn_sigma, and optimization
            # g1, g2, gp should be class object
            
        if index==1:    # simplified, to take golden ratio as initialization
            temp=self.xn_sigma
            new_x_min=g1.x_min
            a=0
            b=0
                    
            while 1:    
                # what if the check of quality does not meet the criteria, should need re-distribute the modification factor
                
                g1.xn=(temp-new_x_min)*0.3819660113+new_x_min
                
                if self.i=="e":
                    g2.xn=temp-g1.xn
                else:
                    g2.xn=temp+g1.xn
                    
                g1.para_calc()  # calculate other parameters related to delta_y_n of gear1 (tip / root diameter)
                g2.para_calc()  # calculate other parameters related to delta_y_n of gear2 (tip / root diameter)
                g1.gear_quality_check()
                g2.gear_quality_check()
                self.engage_quality_check()
                        
                if g1.undercut<>"" or g2.undercut<>"":  # check whether gears have undercut
                    new_x_min=g1.xn
                    continue
                else:
                    a=1
                
                if g1.sharpen<>"" or g2.sharpen<>"":    # check whether gear tip have been sharpened
                    temp=new_x_min
                    new_x_min=g1.xn
                    continue
                else:
                    b=1
                
                jump=a+b
                    
                if jump==2: # jump=2 means no undercut and no sharpen happened
                    break
                
        elif index==2:   # equal slip ratio methods
            # more complex
            return 2
        elif index==3:  # flushing point of gear methods
            # more complex
            return 3
        else:
            return 0
                
    
    def engage_quality_check(self):
        
        return 0
    
    def slip_ratio(self):
        # to calculate the slip ratio of the gear pair
        
        return 0
    
    
# the following are for testing of this file    
gear=Helix_Gear(2.5,19,31,20,1,0.25,18,30,0,0)
print(gear.mn,gear.z,gear.beta,gear.d,gear.mat,gear.HT,gear.hardness)