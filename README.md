# DataAnalysisGui
Interface for quick and easy data processing for Photoluminescence Data

The main python file is gui-build.py

Run this from a terminal or Ipython terminal and it will start the program.

The user interface is pretty straightforward. First the user must select the folder where
the data is located. The data must be named filename_sig.txt and filename_sig_dark.txt (for
the dark spectrum).

Once the folder is selected, the data that has been preprocessed (this involves subtracting the 
dark spectra and reformatting data into numpy arrays and then saving the arrays),  will be listed
in the "Processed Files" list. If the files of interest are not there, the data can be processed
using the "Process" button.

Any of the data that has been imported into numpy arrays can be previewed, by selecting it in the
"Processed Files" box and clicking the preview button. This will plot the 10th and the 20th spectrum
in the array. The preview plot is interactive and can be used to determine the desired integration
bounds.

Once the integration bounds are determined, the values can be typed into the bound input boxes and the
values can be checked using the checked bounds button, which will display vertical lines for the locations
of the upper and lower bounds.

If the data is ready to be integrated, the desired integration bounds can be entered into the boxes (unless the
default is prefered) and the checkboxes can be selected if desired. The "Integrate All" check box performs integration
on all the preprocessed files in the folder instead of the one(s) currently selected in the "Processed Files" list. The
"Remove Space" checkbox removes any dead time in the run, for example any time the laser was shuttered. The "Make and 
Save Plots" will plot the integrated traces and save them in the same folder. If desired a plot title can be added when
this is checked.

Once all of these inputs are decided, the "Integrate Data" button can be clicked and the program will find the area under the
curve of all the spectra in the arrays between the two bounds and will save that with the corresponding time data. The integrated
data will be saved as a numpy array with the name "filename+Int<upperbound>to<lowerbound>.npy".
