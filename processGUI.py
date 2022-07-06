# Semi-Bulk Processing
# by Nicole Quist (2/20/2019)
# 
# This script process all the signal files from Spectrasuite in a given
# directory. It finds all the *_sig.txt files that don't have corresponding
# *_pros.npy and *_time.npy files (or .txt files if you choose that format)
# and imports them, reshapes them, removes the background (found in the 
# corresponding *_dark.txt file) and saves the data to binary files 
# called *_pros.npy and *_time.npy or .txt files if so desired.

import numpy as np
import glob
import os
import re


def run_data():
    # Collect lists of sig, dark and pros files in the dir and then trim the ending
    txt_files = False
    fls = glob.glob("*_sig.txt")
    fls_trimmed = [re.sub('\_sig\.txt$', '', file) for file in fls]
    
    # Due to non-standard naming, some of the files are named file_sig_dark and some
    # are named file_dark. This makes the code robust to process both without changing
    # the code.
    dkfls = glob.glob("*_dark.txt")
    dksigfls = glob.glob("*_sig_dark.txt")
    dk_with_sig = False
    
    if len(dksigfls) == 0:
        dkfls_trimmed = [re.sub('\_dark\.txt$', '', file) for file in dkfls]
    else:
        dkfls_trimmed = [re.sub('\_sig\_dark\.txt$', '', file) for file in dksigfls]
        dk_with_sig = True
    
    
    # Allows to switch between .npy files and .txt files
    if txt_files == True:
        prsfls = glob.glob("*_pros.txt")
        timefls = glob.glob("*_time.txt")
        prsfls_trimmed = [re.sub('\_pros\.txt$', '', file) for file in prsfls]
        timefls_trimmed = [re.sub('\_time\.txt$', '', file) for file in timefls]
    else:
        prsfls = glob.glob("*_pros.npy")
        timefls = glob.glob("*_time.npy")
        prsfls_trimmed = [re.sub('\_pros\.npy$', '', file) for file in prsfls]
        timefls_trimmed = [re.sub('\_time\.npy$', '', file) for file in timefls]
    
    print(fls_trimmed)
    print(dkfls_trimmed)
    print(prsfls_trimmed)
    print(timefls_trimmed)
    
    # Remove already processed data (data with both pros and time files)
    # from the list to process.
    fully_processed = set(prsfls_trimmed).intersection(timefls_trimmed)
    unpros_fls = set(fls_trimmed)-fully_processed
    
    # Remove any sig files that don't have a dark file as well
    unpros_fls_withdk = list(unpros_fls.intersection(dkfls_trimmed))
    print(unpros_fls_withdk)
    
    # Import data, format it to be 2048 by the length, remove the background (dark),
    # and save it as file_pros.txt and file_time.txt
    for i in range(len(unpros_fls_withdk)):
        file_name = str(unpros_fls_withdk[i])
        print("Running file " + file_name)
        
        # Import data from file_dark and file_sig
        if dk_with_sig == False:
            dark_spec = np.genfromtxt(file_name+'_dark.txt', delimiter='\t', 
                                  skip_header = 17, skip_footer=1)
        else:
            dark_spec = np.genfromtxt(file_name+'_sig_dark.txt', delimiter='\t', 
                                  skip_header = 17, skip_footer=1)
        spec = np.genfromtxt(file_name+'_sig.txt', delimiter='\t', skip_header = 1)
        time = np.genfromtxt(file_name+'_sig.txt', delimiter='\t', max_rows = 1)
        
        # Extract time values, convert from miliseconds to seconds and save as 
        # binary numpy array file called file_time.npy
        time = time[1:(len(time)-1)]/1000
        np.save(file_name+'_time.npy', time) 
        
        # Create new array to hold spec without the background.
        spec_wo_bkg = 0*spec
        spec_wo_bkg[:,0] = spec[:,0]
        
        # Subtract the background noise and then save the processed data to file_pros.txt
        for j in range(1, len(spec[1])):
            spec_wo_bkg[:,j] = spec[:,j] - dark_spec[:,1]
        np.save(file_name+'_pros.npy', spec_wo_bkg)
        
        # Save as txt files if needed
        if txt_files == True:
            np.savetxt(file_name+'_time.txt', time, delimiter='\t')
            np.savetxt(file_name+'_pros.txt', spec_wo_bkg, delimiter='\t')
            
    print('Completed')