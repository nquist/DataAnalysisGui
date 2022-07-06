# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:05:12 2019

@author: Hypatia
"""

import numpy as np
import glob
import os
import re
import matplotlib.pyplot as plt

def locate_files():
    fls = glob.glob("*_pros.npy")
    pros_fls = [re.sub('.npy$', '', file) for file in fls]
    fls = glob.glob("*_time.npy")    
    time_fls = [re.sub('.npy$', '', file) for file in fls]
    fls = glob.glob("*.npy")    
    np_fls = [re.sub('.npy$', '', file) for file in fls]
    
    int_fls = (set(np_fls)-set(pros_fls))-set(time_fls)

    if len(int_fls) == 0:
        return []
    else:
        return sorted(int_fls)
  

def plot_sv(fls, titles, sc1, scnum, numb):
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='Large')
    plt.rc('ytick', labelsize='Large') 
    
    mx = 0
    num = len(fls)
    for i in range(num):
        tmp = get_data(fls[i], sc1, scnum, numb)
        plt.plot(tmp[0,:], tmp[1,:])
        if np.max(tmp[1,:]) > mx:
            mx = np.max(tmp[1,:])
    if len(titles[2]) > 0:
        ttle = titles[2]
    else:
        ttle = 'Integrated PL (counts*nm)'
        
    plt.ylim(-0.5, 1.05*mx)
    plt.ylabel(ttle, fontsize=14)
    plt.xlabel('Time (s)', fontsize=14)
    plt.title(titles[1], fontsize=18)
    plt.savefig(titles[0]+'.png', bbox_inches="tight", dpi=1200)
    plt.close()
    
def get_data(file_name, sc1, scnum, num):
    dta = np.load(file_name+'.npy')
    
    if sc1:
        dta[1,:] = dta[1,:]/np.max(dta[1,:])
    elif scnum and len(num) > 0:
        dta[1,:] = dta[1,:]/float(num)
    
    return dta