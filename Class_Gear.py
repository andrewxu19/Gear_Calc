#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from math import sin,cos,tan,degrees,radians,pow,sqrt,pi,acos,asin,atan,sqrt

class Helix_Gear(object):
    # should download ISO1122 or DIN3960 for the English terms of all the parameter name
    
    def __init__(self,mn,z,z_mate,alpha_n,ha_n,c_n,beta,b,xn,xn_mate,delta_y_n,i="e",hand="LH",):
        # basic parameter of gear, i represents internal or external gear of the gear pair. the alpha_n and beta should be in radians 	
        self.mn=mn                    # 法向模数 section gear modules 
        self.z=z                      # 齿数 tooth number 
        self.z_mate=z_mate            # tooth number of mated gear
        self.i=i	              # 内齿"i"或外齿"e" internal or external gear 
        self.hand=hand	              # 旋向，LH左旋，RH右旋 helix direction 
        self.alpha_n=alpha_n          # 法向分度圆压力角，转換为弧度 section pressure angle at reference diameter, units in deg 
        self.ha_n=ha_n                # 法向齿顶高系数 tip height coefficient 
        self.c_n=c_n                  # 法向顶隙系数 tip gap coefficient 
        self.beta=beta                # 螺旋角，转換为弧度 helix angle, units in deg， and has been transformed to radians
        self.rho_fp=0.38              # 齿根过渡圆角系数 root radius coeffient 
        self.b=b                      # 齿宽 gear width 
        self.xn=xn                    # 法向变位系数 section profile shift coefficient 
        self.xn_mate=xn_mate          # 配对齿轮法向变位系数 section profile shift coefficient of mated gear
        self.delta_y_n=delta_y_n      # 中心距变动系数 modification factor of center distance 
        
        self.mt=self.mn/cos(self.beta)		                # 端面模数 face module 
        self.alpha_t=atan(tan(self.alpha_n)/cos(self.beta))	# 端面分度圆压力角 face pressure angle at reference circle  
        self.xt=self.xn*cos(self.beta)                          # 端面变位系数 face profile shift coefficient
        self.ha_t=self.ha_n*cos(self.beta)                      # 端面齿顶高系数 face tip height coefficient
        self.c_t=self.c_n*cos(self.beta)                        # 端面顶隙系数 face tip gap coefficient
        
        self.d=self.mt*self.z                        	        # 分度圆直径 reference diameter 
        
        self.db=self.d*cos(self.alpha_t)			# 基圆直径 base circle diameter
        self.beta_b=atan(self.db*tan(self.beta)/self.d)         # 基圆螺旋角 helix angle at base circle   
        
        self.x_min=self.ha_n-self.z*sin(self.alpha_n)**2     # 齿轮最小的修形系数 minimum modificatin factor for the gear
        
        self.undercut=""    # 根切状态 gear root cut status
        self.sharpen=""     # 齿顶变尖状态 gear tip sharpened status
        
        # Process information
        test=0
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


        self.tooth_pitch=self.mt*pi    # 齿距 tooth pitch
        self.st=pi*self.mt/2           # 分度圆齿厚 tooth thickness at reference circle
        self.sa=self.da*(pi/2/self.z+2*self.xn*tan(self.alpha_n)/self.z+inv(self.alpha_n)-inv(self.alpha_at))   # 齿顶圆齿厚 tooth thickness at tip circle
        
        self.z_v=self.z/(cos(self.beta_b)**2*cos(self.beta)) # 当量齿数Zv, equivalent tooth number
        
        return 0

    def gear_quality_check(self):
        # 检查齿轮质量，如根切，齿顶变尖
        # check the gear quality, eg. undercut, tip sharpen
        
        # 根切检查 undercut check        
        z_min=2*self.ha_n/sin(self.alpha_n)**2
        if self.z<z_min:
            self.undercut="too less tooth number, please check and re-enter the parameter"
        
        # 齿顶变尖检查 tip sharpen check
        if self.sa<0.4*self.mn:
            self.sharpen="tip thickness too small (less than 0.4mn)"

    def bend_strength_calc(self):
    # check the bending strength
        test=0
        return 0

    def contact_strength_calc(self):
    #check contact strength
        test=0
        return 0

    def pitting_calc(self):
    # check pitting
        test=0
        return 0

    def tolerance_calc(self):
    # 计算齿轮的精度公差
    # calculate tolerance of the gear
    
        # 公法线长度及跨齿数 calculate the common normal length
        temp=self.z*inv(self.alpha_t)/inv(self.alpha_n)
        self.k=round(temp/pi*(sqrt((1+2*self.xn/temp)**2-cos(self.alpha_n)**2)/cos(self.alpha_n)-2*self.xn*tan(
            self.alpha_n)/temp-inv(self.alpha_n))+0.5) # 跨齿数 number of teeth when measuring
        
        self.w_asterisk=cos(self.alpha_n)*(pi*(self.k-0.5)+temp*inv(self.alpha_n))
        self.w_delta=2*self.xn*sin(self.alpha_n)
        
        self.w_n=(self.w_asterisk+self.w_delta)*self.mn  # 公法线长度 common normal length
                
        test=0 # 斜齿轮不能测量条件

        # 分度圆弦齿厚
        if self.i="e":
            self.h_bar=self.ha_n+self.mn*self.z_v*(1-cos(pi/2/self.z_v+2*self.xn*tan(self.alpha_n)/self.z_v)) # 分度圆弦齿高
            self.s_bar=self.mn*self.z_v*sin(pi/2/self.z_v+2*self.xn*tan(self.alpha_n)/self.z_v) # 分度圆弦齿厚
        else:
            self.delta_a2= # test 公式模糊，看不清，暂停编辑
            self.h2_delta=self.da/2*(1-cos(self.delta_a2))

            self.s_bar=self.mn*self.z_v*sin(pi/2/self.z_v-2*self.xn*tan(self.alpha_n)/self.z_v) # 分度圆弦齿厚

        # test 固定弦齿厚

        # 跨棒距
        self.dp=1.65*self.mn
        # test 公式太模糊，

 



        return 0

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
        self.z1=0           # teeth number of gear1
        self.z2=0           # teeth number of gear2
        self.b=0            # gear width
        self.beta=0         # gear helix angle
        self.mn=0           # module of gear
        self.alpha_n=0      # 法向压力角
        self.ha_n=0         # 法向齿顶高系数
        self.c_n=0          # 法向顶隙系数
        self.xn1=0          # 小齿轮法向变位系数
        self.xn2=0          # 大齿轮法向变位系灵敏
        
        self.i=""           # 内/外啮合 external / internal engagement
        self.d1_modified=0  # 小齿轮节圆直径 pitch diameter of gear1
        self.d2_modified=0  # 大齿轮节圆直径 pitch diameter of gear2
        self.Epix_a=0       # 端面重合度 face overlap ratio
        self.Epix_b=0       # 轴向重合度 axial overlap ratio
        self.Epix_gama=0    # 总重合度 total overlap ratio
        self.a=0            # 理论中心距 theoretical center distance
        self.a_modified=0   # 实际中心距 modified center distance (actual center distance) 
        self.at_modified=0  # 啮合角 engagement angle
        self.xn_sigma=0 # 总变位系数 total modification factor
        self.yn=0           # 法向中心距变动系数
        self.yt=0
        self.delta_y_n=0
        self.rho=0          # 干涉检查用参数
        self.eta1=0     # 小齿轮最大滑动率 slip ratio of gear1
        self.eta2=0     # 大齿轮最大滑动率 slip ratio of gear2
        
        self.transit_curve=""   # store the status of the transit curve of gear1
        
    def para_calc(self):
        # basic parameter calcu
        self.alpha_t=atan(tan(self.alpha_n)/cos(self.beta))	    # 端面分度圆压力角 face pressure angle at reference circle  
        self.mt=self.mn/cos(self.beta)		                 	# 端面模数 face module 
        self.a=self.mn*(self.z1+self.z2)/2/cos(self.beta)           # theoretical center distance
        
        if self.a_modified==0:    #  变位系数已知，计算实际中心距等参数 if xn1,xn2 already known, to calculate a_modified
            if self.i=="e":  # if external engagement
                self.xn_sigma=self.xn2+self.xn1
                self.at_modified=ainv(2*(self.xn2+self.xn1)*tan(self.alpha_n)/(self.z2+self.z1)+inv(self.alpha_t))
                self.yt=(self.z2+self.z1)*(cos(self.alpha_t)/cos(self.at_modified)-1)/2
                self.yn=self.yt/cos(self.beta)
                self.a_modified=self.mn*((self.z2+self.z1)/2+self.yt)/cos(self.beta)
                self.delta_y_n=self.xn2+self.xn1-self.yn   # center distance modification factor
            else:   # if internal engagement
                self.xn_sigma=self.xn2-self.xn1
                self.at_modified=ainv(2*(self.xn2-self.xn1)*tan(self.alpha_n)/(self.z2-self.z1)+inv(self.alpha_t))
                self.yt=(self.z2-self.z1)*(cos(self.alpha_t)/cos(self.at_modified)-1)/2
                self.yn=self.yt/cos(self.beta)
                self.a_modified=self.mn*((self.z2-self.z1)/2+self.yt)/cos(self.beta)  # center distance modified
                self.delta_y_n=self.xn2-self.xn1-self.yn   # center distance modification factor     
        else:    # 已知实际中心距，计算总充数位系数 if a_modified (center distance modified) already known, to calculate xn_sigma and distribute xn between gears
            if self.i=="e":   # if external engagement
                self.a=self.mn*(self.z1+self.z2)/2/cos(self.beta)
                self.yt=(self.a_modified-self.a)/self.mt
                self.yn=(self.a_modified-self.a)/self.mn
                self.at_modified=acos(self.a*cos(self.alpha_t)/self.a_modified) # engagement angle
                self.xn_sigma=(self.z2+self.z1)*(inv(self.at_modified)-inv(self.alpha_t))/2/tan(self.alpha_n)   # total modification coefficiency
        
                self.delta_y_n=self.xn_sigma-self.yn  # center distance modification factor
               
            else:   # if internal engagement        
                self.a=self.mn*(self.z2-self.z1)/2/cos(self.beta)
                self.yt=(self.a_modified-self.a)/self.mt
                self.yn=(self.a_modified-self.a)/self.mn
                self.at_modified=acos(self.a*cos(self.alpha_t)/self.a_modified) # engagement angle
                self.xn_sigma=(self.z2-self.z1)*(inv(self.at_modified)-inv(self.alpha_t))/2/tan(self.alpha_n) # total modification coefficiency
        
                self.delta_y_n=self.xn_sigma-self.yn  # center distance modification factor
                    
    def advance_calc(self,g1,g2):
     
        if self.i=="e":   # if external engagement
            self.d1_modified=2*self.a_modified*self.z1/(self.z2+self.z1) # 小齿轮节圆直径 pitch diameter of gear1
            self.d2_modified=2*self.a_modified*self.z2/(self.z2+self.z1) # 大齿轮节圆直径 pitch diameter of gear2
            self.Epix_a=(self.z1*(tan(g1.alpha_at)-tan(self.at_modified))+self.z2*(tan(g2.alpha_at)-tan(g2.alpha_t)))/2/pi    # face overlap ratio
        else:   # if internal engagement
            self.d1_modified=2*a_modified*self.z1/(self.z2-self.z1) # 小齿轮节圆直径 pitch diameter of gear1
            self.d2_modified=2*a_modified*self.z2/(self.z2-self.z1) # 大齿轮节圆直径 pitch diameter of gear2
            self.Epix_a=(self.z1*(tan(g1.alpha_at)-tan(self.at_modified))-self.z2*(tan(g2.alpha_at)-tan(g2.alpha_t)))/2/pi    # face overlap ratio  
        
        self.Epix_b=self.b*sin(self.beta)/self.mn/pi    # 轴向重合度 axial overlap ratio
        self.Epix_gama=self.Epix_a+self.Epix_b     # 总重合度 total overlap ratio    
        
        
    def x_distribute(self,g1,g2,index):
    # 变位系数分配优化，g1,g2为齿轮类对象，index为方法类别，1为黄金分割法，2为
    # distribution of xn_sigma, and optimization
    # g1, g2, self should be class object
            
        if index==1:    # simplified, to take golden ratio as initialization
            temp=self.xn_sigma
            if g1.x_min<0:
                new_x_min=0
            else:
                new_x_min=g1.x_min
                    
            while 1:    
                # what if the check of quality does not meet the criteria, should need re-distribute the modification factor
                
                g1.xn=(temp-new_x_min)*0.6180339887498+new_x_min
                
                if self.i=="e":
                    g2.xn=self.xn_sigma-g1.xn
                else:
                    g2.xn=self.xn_sigma+g1.xn

                g1.para_calc()  # calculate other parameters related to delta_y_n of gear1 (tip / root diameter)
                g2.para_calc()  # calculate other parameters related to delta_y_n of gear2 (tip / root diameter)
                g1.gear_quality_check()
                g2.gear_quality_check()
                self.interference_check(g1,g2)
                        
                if g1.sharpen!="" or g2.sharpen!="" or self.transit_curve!="":    # check whether gear tip have been sharpened or have transit curve interference
                    temp=g1.xn
                    continue
                else:   # no undercut, no sharpen and no transit curve interference happened
                    break
            return 1    
        elif index==2:   # equal slip ratio methods
            # more complex
            return 2
        elif index==3:  # flushing point of gear methods
            # more complex
            return 3
        else:
            return 0
                
    
    def interference_check(self,g1,g2):
        if self.i=="i":
            self.rho=g1.mt*(self.z1*sin(g1.alpha_t)/2-(g1.ha_t-g1.xt)/sin(g1.alpha_t))
            if g2.da<sqrt(g2.db**2+(2*self.a_modified*sin(self.at_modified)+2*self.rho)**2):
                self.transit_curve="interferenced, please check the parameter and reselect the xn1"
        return 0
    
    def slip_ratio(self,g1,g2):
        # to calculate the slip ratio of the gear pair
        self.eta1=(self.z1+self.z2)*(tan(g2.alpha_at)-tan(self.at_modified))/((self.z1+self.z2)*tan(self.at_modified)-self.z2*tan(g2.alpha_at))
        self.eta2=(self.z1+self.z2)*(tan(g1.alpha_at)-tan(self.at_modified))/((self.z1+self.z2)*tan(self.at_modified)-self.z1*tan(g1.alpha_at))
      
        return 0
    
    
# the following are for testing of this file    
# gear=Helix_Gear(2.5,19,31,20,1,0.25,18,30,0,0)
# print(gear.mn,gear.z,gear.beta,gear.d,gear.mat,gear.HT,gear.hardness)

def write2file(gp,g1,g2):
# 计算结果按特定格式输出至文件    
# write all result to a file with certain format
    f=open("result.txt","w")
    f.write("齿轮对：",gp.name)
    f.write("齿轮对参数")
    f.write("模数，齿数1，齿数2，压力角，螺旋角，变位1，变位2")
    f.write(gp.mn, gp.z1, gp.z2, gp.alpha_n, gp.beta, gp.xn1, gp.xn2)
    # 单个齿轮的参数
    f.write("小齿轮")
    
    print("test")
    return 0