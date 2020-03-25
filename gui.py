import tkinter
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from main_program import main_func
import numpy as np


fig = Figure()
ax = fig.add_subplot(111)
x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
y = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
ax.set_title('Energy Loss Calculations',fontname='serif')
ax.set_xlabel('Strip Number',fontname='serif')
ax.set_ylabel('Energy Loss (MeV)',fontname='serif')
ax.grid()
ax.set_xlim(-1, 18)
ax.set_ylim(0, 3)
ax.scatter(x,y)


class App:
    def __init__(self, master):
        # Create a container
        frame = tkinter.Frame(master)
##################################################################################
#This button starts the magic! Go over to the draw function for more information
#about what this button acutally does. 

        self.compute_loss = tkinter.Button(master,text=" Compute Energy Loss ", command=self.draw)
        self.compute_loss.grid(row=2,column=0)


        self.reactionstrip_label = tkinter.Label(master,text='Reaction in Strip:')
        self.reactionstrip_label.grid(row=3,column=0)
        self.reactionstrip = StringVar()
        self.reactionstrip.set("SELECT STRIP")
        self.reactionstrip_entry = OptionMenu(master,self.reactionstrip, 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)
        self.reactionstrip_entry.grid(row = 4, column = 0)

##################################################################################
#Entries for m1 Particle (this is the beam)

        self.m1_name_label = tkinter.Label(master,text='m1 Name')
        self.m1_name_label.grid(row=2,column=1)
        self.m1_name_entry = tkinter.Entry(master,text='m1 Name',width=3)
        self.m1_name_entry.grid(row=2,column=2)

        self.m1_E_label = tkinter.Label(master,text='m1 E')
        self.m1_E_label.grid(row=3,column=1)
        self.m1_E_entry = tkinter.Entry(master,text='m1 E',width=3)
        self.m1_E_entry.grid(row=3,column=2)

        self.m1_A_label = tkinter.Label(master,text='m1 A')
        self.m1_A_label.grid(row=4,column=1)
        self.m1_A_entry = tkinter.Entry(master,text="m1 A",width=3)
        self.m1_A_entry.grid(row=4,column=2)

        self.m1_Z_label = tkinter.Label(master,text='m1 Z')
        self.m1_Z_label.grid(row=5,column=1)
        self.m1_Z_entry = tkinter.Entry(master,text='m1 Z',width=3)
        self.m1_Z_entry.grid(row=5,column=2)

        self.m1_mass_label = tkinter.Label(master,text='m1 Mass')
        self.m1_mass_label.grid(row=6,column=1)
        self.m1_mass_entry = tkinter.Entry(master,text='m1 Mass',width=3)
        self.m1_mass_entry.grid(row=6,column=2)

##################################################################################
#Entries for m3 Particle (this is the heavy recoil)
        
        self.m3_name_label = tkinter.Label(master,text='m3 Name')
        self.m3_name_label.grid(row=2,column=3)
        self.m3_name_entry = tkinter.Entry(master,text='m3 Name',width=3)
        self.m3_name_entry.grid(row=2,column=4)

#        self.m3_E_label = tkinter.Label(master,text='m3 E')
#        self.m3_E_label.grid(row=3,column=3)
#        self.m3_E_entry = tkinter.Entry(master,text='m3 E',width=3)
#        self.m3_E_entry.grid(row=3,column=4)

        self.m3_A_label = tkinter.Label(master,text='m3 A')
        self.m3_A_label.grid(row=4,column=3)
        self.m3_A_entry = tkinter.Entry(master,text="m3 A",width=3)
        self.m3_A_entry.grid(row=4,column=4)

        self.m3_Z_label = tkinter.Label(master,text='m3 Z')
        self.m3_Z_label.grid(row=5,column=3)
        self.m3_Z_entry = tkinter.Entry(master,text='m3 Z',width=3)
        self.m3_Z_entry.grid(row=5,column=4)
        
        self.m3_mass_label = tkinter.Label(master,text='m3 Mass')
        self.m3_mass_label.grid(row=6,column=3)
        self.m3_mass_entry = tkinter.Entry(master,text='m3 Mass',width=3)
        self.m3_mass_entry.grid(row=6,column=4)

##################################################################################
#Gas property entries
        
        self.gaspressure_label = tkinter.Label(master,text='Gas Pressure (Torr)')
        self.gaspressure_label.grid(row=2,column=5)
        self.gaspressure_entry = tkinter.Entry(master,text='Gas Pressure (Torr)',width=6)
        self.gaspressure_entry.grid(row=2,column=6)

        self.gastype_label = tkinter.Label(master,text='Gas Type')
        self.gastype_label.grid(row=3,column=5)
        self.variable = StringVar()
        self.variable.set("SELECT GAS")
        self.gastype_entry = OptionMenu(master,self.variable, 'METHANE','P10','HELIUM')
        self.gastype_entry.grid(row = 3, column = 6)


##################################################################################
#Window Properties 
        
        self.windowthick_label = tkinter.Label(master,text='Mylar Window Thickness (ug/cm^2)')
        self.windowthick_label.grid(row=4,column=5)
        self.windowthick_entry = tkinter.Entry(master,text='Mylar Window Thickness (ug/cm^2)',width=6)
        self.windowthick_entry.grid(row=4,column=6)
        
##################################################################################
      
        self.tree_label = tkinter.Label(master,text=' m1 Energy Loss Table')
        self.tree_label.grid(row=0,column=8)
        self.tree = ttk.Treeview(master)
        self.tree["columns"]=("Element","Energy")
        self.tree.column("#0", width=0, minwidth=0, stretch=tkinter.NO)
        self.tree.column("Element", width=100, minwidth=10, stretch=tkinter.NO)
        self.tree.column("Energy", width=80, minwidth=10, stretch=tkinter.NO)
        self.tree.heading("Element",text="Element",anchor=tkinter.W)
        self.tree.heading("Energy", text="Energy (MeV)",anchor=tkinter.W)
        self.tree.grid(row=0,column=8,rowspan=4,sticky=E,padx=0)
        self.tree.configure(height=20)

        self.tree2_label = tkinter.Label(master,text=' m4 Energy Loss Table')
        self.tree2_label.grid(row=0,column=9)
        self.tree2 = ttk.Treeview(master)
        self.tree2["columns"]=("Element","Energy")
        self.tree2.column("#0", width=0, minwidth=0, stretch=tkinter.NO)
        self.tree2.column("Element", width=100, minwidth=10, stretch=tkinter.NO)
        self.tree2.column("Energy", width=80, minwidth=10, stretch=tkinter.NO)
        self.tree2.heading("Element",text="Element",anchor=tkinter.W)
        self.tree2.heading("Energy", text="Energy (MeV)",anchor=tkinter.W)
        self.tree2.grid(row=0,column=9,rowspan=4,sticky=E,padx=10)
        self.tree2.configure(height=20)  
##################################################################################
#This sets up an empty plot before the magic happens when the program is first
#started up.
        
        
        self.plot1 = ax.scatter(x,y)
        self.canvas = FigureCanvasTkAgg(fig,master=master)
        self.canvas.get_tk_widget().grid(row=1,column=0,columnspan=8)
        self.canvas.draw()

         
##################################################################################
##################################################################################
##################################################################################
#This is where the magic happens! Get all the useful values from the entries
#and pass them along to the energy loss calculation algorithm. Onces the values
#are calculated the values are plotted.
        
    def draw(self):
        m1_energy = float(self.m1_E_entry.get())
        m1_name = str(self.m1_name_entry.get())
        m1_mass = float(self.m1_mass_entry.get())
        m1_Z = float(self.m1_Z_entry.get())
        m1_A = float(self.m1_A_entry.get())

        m4_name = str(self.m3_name_entry.get())
        m4_mass = float(self.m3_mass_entry.get())
        m4_Z = float(self.m3_Z_entry.get())
        m4_A = float(self.m3_A_entry.get())

        gastype = str(self.variable.get())
        gaspressure = float(self.gaspressure_entry.get())
        windowthick = 0
        reactionstrip = int(self.reactionstrip.get())
        
        window_eloss, dead_eloss, m1strip, m4strip = main_func(m1_name,m1_mass,m1_energy,m1_Z,m1_A,m4_name,m4_mass,m4_Z,m4_A,gastype,gaspressure,windowthick,reactionstrip)





        self.tree.delete(*self.tree.get_children())
        self.tree2.delete(*self.tree2.get_children())
        
        self.tree.insert('',1, text="Window", values=("Window",window_eloss))
        self.tree.insert('',2, text="Dead Region", values=("Dead Region",dead_eloss))
        for i in range(0,17):
            self.tree.insert('',i+2, text="Dead Region", values=("Strip " +str(i),m1strip[i]))

        self.tree2.insert('',1, text="Window", values=("Window","No Reaction"))
        self.tree2.insert('',2, text="Dead Region", values=("Dead Region","No Reaction"))
        for i in range(0,17):
            if(i < reactionstrip):
                self.tree2.insert('',i+2, text="Dead Region", values=("Strip " +str(i),"No Reaction"))
            else:
                self.tree2.insert('',i+2, text="Dead Region", values=("Strip " +str(i),m4strip[i]))                
    
        self.tree.insert('',19, text="Dead Region", values=(("Total Eloss "),sum(m1strip)+window_eloss+dead_eloss))
        self.tree.insert('',20, text="Dead Region", values=(("Remaing E "),m1_energy-(sum(m1strip)+window_eloss+dead_eloss)))        
            
        ax.clear()
        ax.set_title('Energy Loss Calculations',fontname='serif')
        ax.set_xlabel('Strip Number',fontname='serif')
        ax.set_ylabel('Energy Loss (MeV)',fontname='serif')
        ax.grid()
        ax.set_xlim(-1, 18)
        ax.set_ylim(0, np.amax(m4strip)+1)
        self.plot1 = ax.scatter(x,m1strip,color = 'r',label=m1_name)
        self.plot1 = ax.scatter(x,m4strip,color = 'b',label=m4_name)     
        self.plot1 = ax.plot(x,m1strip,color = 'r')
        self.plot1 = ax.plot(x,m4strip,color='b')
        ax.legend(loc=1)
        self.canvas.draw()

##################################################################################
##################################################################################
##################################################################################





root = tkinter.Tk()
app = App(root)
root.title("Athena Energy Loss Calculator")
root.mainloop()
