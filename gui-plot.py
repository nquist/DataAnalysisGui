import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import os
import plotInfo as pltI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCan

window = tk.Tk()

window.title("Plotting Town")
window.geometry('830x500')

intAll = tk.BooleanVar()
scl1 = tk.BooleanVar()
sclnum = tk.BooleanVar()
list_fls = []

## Functions for buttons

def getDirect():
    direct =  filedialog.askdirectory(title='Select')
    os.chdir(direct)
    Directory.config(text=direct)
    rdy_fls = pltI.locate_files()
    listbox.delete(0,'end')
    if len(rdy_fls) > 0:
        for item in rdy_fls:
            listbox.insert('end', item)
        listbox.update_idletasks()
        btn_run.config(state='normal')
        btn_save.config(state='normal')
    else: 
        btn_run.config(state='disabled')
        btn_save.config(state='disabled')
    
def prevGraph():
    ax.clear()
    val, pt_titles = get_lists()
    mx = 0
    if len(val) >= 1:
        for i in range(0,len(val)):
            print(i, val[i])
            dta1 = pltI.get_data(val[i], scl1.get(), sclnum.get(), scl_val.get())
            ax.plot(dta1[0,:],dta1[1,:])    
            if np.max(dta1[1,:]) > mx:
                mx = np.max(dta1[1,:])
        yu =1.1*mx
        ax.set_ylim((0,yu))
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(pt_titles[2])
        ax.set_title(pt_titles[1])
        canvas.draw()
        
def SavePlot():
    if len(fle_ttle.get()) > 0:
        val, pt_titles = get_lists()
        pltI.plot_sv(val, pt_titles, scl1.get(), sclnum.get(), scl_val.get())
        
        
def get_lists():
    if intAll.get():
        files = pltI.locate_files()
    else:
        files = []
        idx = listbox.curselection()
        for j in range(len(idx)):
            files.append(pltI.locate_files()[idx[j]])
    
    plt_titles = []
    if len(fle_ttle.get()) > 0:
        plt_titles.append(fle_ttle.get())
    else:
        plt_titles.append(' ')
    if len(ttle.get()) > 0:
        plt_titles.append(ttle.get())
    else:
        plt_titles.append(' ')
    if len(y_ttle.get()) > 0:
        plt_titles.append(y_ttle.get())
    else:
        plt_titles.append('Integrated Counts (counts*nm)')
        
    return files, plt_titles
    
      
## Set up GUI

# first frame - select working directory (must contain data files)
flder = tk.LabelFrame(window, text="Folder Location", padx=5, pady=5)
flder.grid(column=1, row=1, sticky="nsew")

Direct_lab = tk.Label(flder, text="Select working directory (must contain data and will be where plots are saved): \t")
Direct_lab.grid(column = 1, row = 1, columnspan = 5)
Directory = tk.Label(flder, text="Dir: <Not yet chosen>")
Directory.grid(column=1, row=2, columnspan = 4)

btn_fldr_select = tk.Button(flder, text="Select Folder", command=getDirect)
btn_fldr_select.grid(column=20, row=2, sticky= 'e')

# Second frame. This is where most of the processing will happen. Data can be previewed,
# Integration bounds are chosen and files are run and saved. 
IntView = tk.LabelFrame(window, text="Preview and Integration", padx=5, pady=5)
IntView.grid(column=1, row=3, sticky="nsew")

Pros_fls = tk.Label(IntView, text="Processed Files")
Pros_fls.grid(column=1, row=1, columnspan=3)

wvleng = tk.Label(IntView, text="Plot Preview")
wvleng.grid(column=6, row=1, columnspan=5)

int_all = tk.Checkbutton(IntView, text="Plot All", variable=intAll, onvalue=True, offvalue=False)
int_all.grid(column=1, row=6, sticky='w')
remove_space = tk.Checkbutton(IntView, text="Scale to 1", variable=scl1, onvalue=True, offvalue=False)
remove_space.grid(column=1, row=7, sticky='w')
plts = tk.Checkbutton(IntView, text="Scale plots by", variable=sclnum, onvalue=True, offvalue=False)
plts.grid(column=1, row=8, sticky='w')


scrollbar_y = tk.Scrollbar(IntView, orient="vertical")
listbox = tk.Listbox(IntView, selectmode="extended", width=35, height = 5,\
                     yscrollcommand=scrollbar_y.set) #, xscrollcommand=scrollbar_x.set)
scrollbar_y.config(command=listbox.yview)
scrollbar_y.grid(column=4, row=2, rowspan=2, sticky="ns")
listbox.grid(column=1, row=2, rowspan=2, columnspan=3)

#Create Matplotlib figure
fig = plt.figure(figsize=(7,4))
ax = fig.add_subplot(111)
ax.set_xlim((0,800))
ax.set_xlabel('Time (s)')
ax.set_ylabel('Integrated Count')

#Create Tkinter canvas to hold mpl figure
plotFrame = tk.LabelFrame(IntView)
plotFrame.grid(row=2,column=6,columnspan=5, rowspan = 11, padx=12)
canvas = FigCan(fig,master=plotFrame)
#self.canvas.show()
canvas.get_tk_widget().grid(row=0,column=0)

scl_val = tk.Entry(IntView, bd =5)
scl_val.grid(column=3, row=8, columnspan=2, sticky='w')

gt_ttle = tk.Label(IntView, text="Plot Title")
gt_ttle.grid(column=1, row=9, columnspan=2, sticky='w')
ttle = tk.Entry(IntView, bd =5)
ttle.grid(column=1, row=10, columnspan=3, sticky='w')

gt_y_ttle = tk.Label(IntView, text="Y-axis Label")
gt_y_ttle.grid(column=1, row=11, columnspan=2, sticky='w')
y_ttle = tk.Entry(IntView, bd =5)
y_ttle.grid(column=1, row=12, columnspan=3, sticky='w')

gt_fle_ttle = tk.Label(IntView, text="File name to save plot")
gt_fle_ttle.grid(column=1, row=13, columnspan=2, sticky='w')
fle_ttle = tk.Entry(IntView, bd =5)
fle_ttle.grid(column=1, row=14, columnspan=2, sticky='w')

btn_run = tk.Button(IntView, text="Plot", state='disabled', command=prevGraph)
btn_run.grid(column=3, row=11, columnspan=1)

Int_complete = tk.Label(IntView, text=" ")
Int_complete.grid(column=3, row=12, columnspan=2, sticky='w')

btn_save = tk.Button(IntView, text="Save Plot", state='disabled', command=SavePlot)
btn_save.grid(column=3, row=14, columnspan=1)

plt.close()
window.mainloop()
