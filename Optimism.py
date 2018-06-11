#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from Class_Gear import *

def x_distribute(g1,g2,gp,index):
    # distribution of xn_sigma, and optimization
    # g1, g2, gp should be class object
    
    if index==1:    # simplified, to take golden ratio as initialization
        temp=gp.xn_sigma
        new_x_min=g1.x_min
        a=0
        b=0
            
        while 1:    
            # what if the check of quality does not meet the criteria, should need re-distribute the modification factor
        
            g1.xn=(temp-new_x_min)*0.3819660113+new_x_min
        
            if gp.i=="e":
                g2.xn=temp-g1.xn
            else:
                g2.xn=temp+g1.xn
            
            g1.para_calc()  # calculate other parameters related to delta_y_n of gear1 (tip / root diameter)
            g2.para_calc()  # calculate other parameters related to delta_y_n of gear2 (tip / root diameter)
            g1.gear_quality_check()
            g2.gear_quality_check()
            gp.engage_quality_check()
                
            if g1.undercut<>"" or g2.undercut<>"":
                new_x_min=g1.xn
                continue
            else:
                a=1
        
            if g1.sharpen<>"" or g2.sharpen<>"":
                temp=new_x_min
                new_x_min=g1.xn
                continue
            else:
                b=1
        
            jump=a+b
            
            if jump==2:
                break
        
    elif index==2:  # equal slip ratio methods
        # more complex
        return 2