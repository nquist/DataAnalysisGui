# -*- coding: utf-8 -*-

#Created on Mon Mar  4 18:23:48 2019
#
#@author: Nicole Quist
#
#This code takes all the *_pros.npy files in a directory, makes sure
#There is a coresponding *_time.npy file. Then it plots the first and
#second trace of the pros file and asks the user if it is a file that
#they want to integrate. It then prompts the user to enter the desired
#wavelengths of integration and checks to make sure the values are
#correct. It performs the integration removing dead time and saves the
#data with the corresponding time values to a new .npy file with the 
#integration bounds in the file name. If desired, a plot will also be
#generated and saved as a png.

import glob as glob
import numpy as np
import matplotlib.pyplot as plt
import os
import re

# Choose Working directory and then chooses file name and plotting
#direc = input("Choose the directory: ") #"Z:\\smfiles\\Data\\Bulk Photobleaching\\December 11 2018\\Pn-TIPS_F8"
#os.chdir(direc)
#All_files = True #Run through all files?
#ploting = True #Make and save plot of integrated spec?
#changeTitle = False #Use a different title?
#newTitle = "Pn-TIPS-F8 in PMMA recovery"

# Finds all the *_pros.npy and *_time.npy files and takes the intersection
def locate_files():
    fls = glob.glob("*_pros.npy")
    pros_fls = [re.sub('\_pros\.npy$', '', file) for file in fls]
    fls = glob.glob("*_time.npy")    
    time_fls = [re.sub('\_time\.npy$', '', file) for file in fls]

    pros_fls = list(set(pros_fls).intersection(time_fls))

    if len(pros_fls) == 0:
        return []
    else:
        return sorted(pros_fls)

# Plotting loop while pobing the user to select the desired data
#for i in range(len(pros_fls)):
#    curr = np.load(pros_fls[i]+"_pros.npy")
#    plt.plot(curr[:,0], curr[:,2], curr[:,0], curr[:,20])
#    plt.title(pros_fls[i])
#    plt.ylabel('Counts')
#    plt.xlabel('Wavelength (nm)')
#    plt.show()
#    add_list = input("Do you want to process this data (y/n)?")
#    if add_list == 'y':
#        fls2int.append(pros_fls[i])
#    elif add_list == 'n':
#        a = 1
#    else:
#        print('Incorrect Input')
#        break

# The integration loop which includes integration, trimming dead time
# saving data and plotting (if desired).

def Integrator(flname, lowerbnd, upperbnd, trim, ploting, title):
    curr = np.load(flname+"_pros.npy")
    currT = np.load(flname+"_time.npy")
    ttl = flname+' Int '+str(int(lowerbnd))+' to '+str(int(upperbnd))
    if len(title) > 0:
        pt_title = title
    else:
        pt_title = ttl
#    if changeTitle == True:
#        ttl = newTitle+str(j)+' Int '+str(int(lwr_bnd))+' to '+str(int(upr_bnd))
#    else:
#        ttl = fls2int[j]+' Int '+str(int(lwr_bnd))+' to '+str(int(upr_bnd))
    loc = np.where((curr[:,0] >= lowerbnd) & (curr[:,0] <= upperbnd))[0]
    intspec = np.zeros((2,len(curr[1,:])-1))
    intspec[0,:] = currT
    r = 0
    for k in range(1,len(curr[0,:])-1):
        tmp = np.trapz(curr[loc,k], curr[loc,0])
        if tmp > 0.2*np.max(intspec) and trim:
            intspec[1,r] = 1*tmp
            r+=1
#        else:
#            intspec[1,r] = 1*tmp
#            r+=1
    intspec = 1*intspec[:,0:r]
    np.save(ttl.replace(" ","")+'.npy', intspec)
    if ploting == True:
        plt.rc('font', family='serif')
        plt.rc('xtick', labelsize='Large')
        plt.rc('ytick', labelsize='Large') 
        
        plt.figure()
        plt.plot(intspec[0,:], intspec[1,:])
        #plt.ylim(-0.5, 1.05*max(intspec[1,:]))
        plt.ylabel('Integrated PL (counts*nm)', fontsize=14)
        plt.xlabel('Time (s)', fontsize=14)
        plt.title(pt_title, fontsize=18)
        plt.savefig(ttl.replace(" ","")+'.png', bbox_inches="tight", dpi=1200)
        plt.close()