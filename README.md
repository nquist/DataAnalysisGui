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

Any of the data that has been imported into numpy arrays
