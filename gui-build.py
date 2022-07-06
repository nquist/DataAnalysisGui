import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import os
import processGUI as pG
import IntegrateAllGUI as IntAll
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCan

window = tk.Tk()

window.title("Nicole is a super powerful python wizard")
window.geometry('920x690')

intAll = tk.BooleanVar()
rmSpc = tk.BooleanVar()
mkPlts = tk.BooleanVar()
list_fls = []

## Functions for buttons

def getDirect():
    direct =  filedialog.askdirectory(title='Select')
    os.chdir(direct)
    Directory.config(text=direct)
    btn_pross.config(state="normal")
    rdy_fls = IntAll.locate_files()
    #list_fls = 1*rdy_fls
    listbox.delete(0,'end')
    if len(rdy_fls) > 0:
        for item in rdy_fls:
            listbox.insert('end', item)
        listbox.update_idletasks()
        btn_prev.config(state='normal')
        btn_run.config(state='normal')
        btn_ck.config(state='normal')
    else: 
        btn_prev.config(state='disabled')
        btn_run.config(state='disabled')
        btn_ck.config(state='disabled')

def preProsess():
    Prosses.config(text="Processing....")
    pG.run_data()
    Prosses.config(text="Processing: Completed")
    rdy_fls = IntAll.locate_files()
    listbox.delete(0,'end')
    if len(rdy_fls) > 0:
        for item in rdy_fls:
            listbox.insert('end', item)
        listbox.update_idletasks()
        btn_prev.config(state='normal')
        btn_run.config(state='normal')
        btn_ck.config(state='normal')
    else: 
        btn_prev.config(state='disabled')
        btn_run.config(state='disabled')
        btn_ck.config(state='disabled')
 
def callback():#(id, tex):
    flz = filedialog.askopenfilenames(parent=window, title='Choose a file')
    filez_path = window.tk.splitlist(flz)
#    if len(filez_path) != 0:
#        filez = np.array((1,len(filez_path)))
#        for i in range(0, len(filez_path)):
#            filez[0,i] = os.path.basename(filez_path[i])
#            tex.insert(window.END, filez[0,i])
#            tex.see(tk.END)
    return(filez_path)
    
def prevGraph():
    val = listbox.curselection()
    if len(val) == 1:
        flname = IntAll.locate_files()[val[0]]
        if len(ttle.get()) > 0:
            title = ttle.get()
        else:
            title = str(flname)
        fle1 = flname+"_pros.npy"
        dta1 = np.load(fle1)
        plt.rc('font', family='serif')
        plt.rc('xtick', labelsize='medium')
        plt.rc('ytick', labelsize='medium')
        ax.clear()
        l = ax.plot(dta1[:,0],dta1[:,10], dta1[:,0],dta1[:,20])
        ax.set_xlim((500,850))
        yu =1.1* max(max(dta1[:,10]),max(dta1[:,20]))
        ax.set_ylim((-1,yu))
        ax.set_xlabel('Wavelength (nm)', fontsize=14)
        ax.set_ylabel('Count', fontsize=14)
        ax.set_title(title, fontsize=18)
        canvas.draw()
        
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        
def ckBnds():
    val = listbox.curselection()
    if len(val) == 1:
        flname = IntAll.locate_files()[val[0]]
        if len(ttle.get()) > 0:
            title = ttle.get()
        else:
            title = str(flname)
        fle1 = flname+"_pros.npy"
        dta1 = np.load(fle1)
        plt.rc('font', family='serif')
        plt.rc('xtick', labelsize='medium')
        plt.rc('ytick', labelsize='medium')
        ax.clear()
        l = ax.plot(dta1[:,0],dta1[:,10], dta1[:,0],dta1[:,20])
        ax.set_xlim((500,850))
        yu =1.1* max(max(dta1[:,10]),max(dta1[:,20]))
        print(int(E_low.get()), int(E_high.get()))
        ax.axvline(x=int(E_low.get()))
        ax.axvline(x=int(E_high.get()))
        ax.set_ylim((-1,yu))
        ax.set_xlabel('Wavelength (nm)', fontsize=14)
        ax.set_ylabel('Count', fontsize=14)
        ax.set_title(title, fontsize=18)
        canvas.draw()
        
        cid = fig.canvas.mpl_connect('button_press_event', onclick)


def onclick(event):
    if event.inaxes is not None:
        wvleng.config(text="Wavelength of click: " + str(int(round(event.xdata,0))))
    else:
        wvleng.config(text="Wavelength of click: n/a")
        
def runInt():
    Int_complete.config(text=" ")
    if E_high.get() == '' or E_low.get() == '':
        low = 615
        high = 732
    else:
        low = E_low.get()
        high = E_high.get()
    if intAll.get() == True:
        for i in range(0, len(IntAll.locate_files())):
            print(IntAll.locate_files()[i])
            tst = IntAll.Integrator(IntAll.locate_files()[i], \
                              int(low), int(high), rmSpc.get(), mkPlts.get(), ttle.get())
            print("done " + str(i+1))
    else:
        for j in range(0, len(listbox.curselection())):
            val = listbox.curselection()[j]
            print(IntAll.locate_files()[val])
            tst = IntAll.Integrator(IntAll.locate_files()[val], \
                              int(low), int(high), rmSpc.get(), mkPlts.get(), ttle.get())
            print("done " + str(j+1))
    Int_complete.config(text="Complete")    
    
## Set up GUI

# first frame - select working directory (must contain data files)
flder = tk.LabelFrame(window, text="Folder Location", padx=5, pady=5)
flder.grid(column=1, row=1, sticky="nsew")

Direct_lab = tk.Label(flder, text="Select working directory (must contain data and will be where plots are saved):")
Direct_lab.grid(column = 1, row = 1, columnspan = 5)
Directory = tk.Label(flder, text="Dir: <Not yet chosen>")
Directory.grid(column=1, row=2, columnspan = 4)

btn_fldr_select = tk.Button(flder, text="Select Folder", command=getDirect)
btn_fldr_select.grid(column=20, row=2, sticky= 'e')


# Second frame that will do preprocessing.
prePros = tk.LabelFrame(window, text="Preprocess Data", padx=5, pady=5)
prePros.grid(column=1, row=3, sticky="nsew")

Prosses = tk.Label(prePros, text="Processing: Not Completed")
Prosses.grid(column=1, row=1, columnspan = 4)

btn_pross = tk.Button(prePros, text="Process", state='disabled', command=preProsess)
btn_pross.grid(column=20, row=1, sticky='e')


# Third frame. This is where most of the processing will happen. Data can be previewed,
# Integration bounds are chosen and files are run and saved. 
IntView = tk.LabelFrame(window, text="Preview and Integration", padx=5, pady=5)
IntView.grid(column=1, row=5, sticky="nsew")

Pros_fls = tk.Label(IntView, text="Processed Files")
Pros_fls.grid(column=1, row=1, columnspan=3)

btn_prev =  tk.Button(IntView, text=u"Preview\n \u27a1", state='disabled', command=prevGraph)
btn_prev.grid(column = 5, row=2, columnspan = 1, padx=5, pady=5)

wvleng = tk.Label(IntView, text="Wavelength of click: n/a")
wvleng.grid(column=6, row=1, columnspan=5)

int_all = tk.Checkbutton(IntView, text="Integrate All", variable=intAll, onvalue=True, offvalue=False)
int_all.grid(column=1, row=6, sticky='w')
remove_space = tk.Checkbutton(IntView, text="Remove Space", variable=rmSpc, onvalue=True, offvalue=False)
remove_space.grid(column=1, row=7, sticky='w')
plts = tk.Checkbutton(IntView, text="Make and Save Plots", variable=mkPlts, onvalue=True, offvalue=False)
plts.grid(column=1, row=8, sticky='w')


scrollbar_y = tk.Scrollbar(IntView, orient="vertical")
#scrollbar_x = tk.Scrollbar(IntView, orient="horizontal")
#scrollbar_x.config(command=listbox.xview)
#scrollbar_x.grid(column=1, row=5, sticky="we")
listbox = tk.Listbox(IntView, selectmode="extended", width=35, height = 5,\
                     yscrollcommand=scrollbar_y.set) #, xscrollcommand=scrollbar_x.set)
scrollbar_y.config(command=listbox.yview)
scrollbar_y.grid(column=4, row=2, rowspan=2, sticky="ns")
listbox.grid(column=1, row=2, rowspan=2, columnspan=3)

#Create Matplotlib figure
fig = plt.figure(figsize=(6,4))
plt.rc('font', family='serif')
plt.rc('xtick', labelsize='medium')
plt.rc('ytick', labelsize='medium')
ax = fig.add_subplot(111)
ax.set_xlim((600,850))
ax.set_xlabel('Wavelength (nm)', fontsize=14)
ax.set_ylabel('Count', fontsize=14)

#Create Tkinter canvas to hold mpl figure
plotFrame = tk.LabelFrame(IntView)
plotFrame.grid(row=2,column=6,columnspan=5, rowspan = 11)
canvas = FigCan(fig,master=plotFrame)
#self.canvas.show()
canvas.get_tk_widget().grid(row=0,column=0)

#Look for click events
cid = fig.canvas.mpl_connect('button_press_event', onclick)

ttle_lab = tk.Label(IntView, text="Plot Title")
ttle_lab.grid(column=1, row=9, columnspan=2, sticky='w')
ttle = tk.Entry(IntView, bd =5)
ttle.grid(column=1, row=10, columnspan=2, sticky='w')
    
L_low = tk.Label(IntView, text="Lower Bound (default 615)")
L_low.grid(column=1, row=11, columnspan=2, sticky='w')
E_low = tk.Entry(IntView, bd =5)
E_low.grid(column=1, row=12, columnspan=2, sticky='w')

L_high = tk.Label(IntView, text="Upper Bound (default 732)")
L_high.grid(column=1, row=13, columnspan=2, sticky='w')
E_high = tk.Entry(IntView, bd =5)
E_high.grid(column=1, row=14, columnspan=2, sticky='w')

btn_ck = tk.Button(IntView, text="Check Bounds\n \u27a1", state='disabled', command=ckBnds)
btn_ck.grid(column=3, row=11, columnspan=3, rowspan=2)

btn_run = tk.Button(IntView, text="Integrate Data", state='disabled', command=runInt)
btn_run.grid(column=2, row=15, columnspan=3)

Int_complete = tk.Label(IntView, text=" ")
Int_complete.grid(column=2, row=16, columnspan=3, sticky='w')

plt.close()
window.mainloop()
