import tkinter
from tkinter import *
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
        self.compute_loss.grid(row=1,column=0)

##################################################################################
#Entries for m1 Particle (this is the beam)

        self.m1_name_label = tkinter.Label(master,text='m1 Name')
        self.m1_name_label.grid(row=1,column=1)
        self.m1_name_entry = tkinter.Entry(master,text='m1 Name',width=3)
        self.m1_name_entry.grid(row=1,column=2)

        self.m1_E_label = tkinter.Label(master,text='m1 E')
        self.m1_E_label.grid(row=2,column=1)
        self.m1_E_entry = tkinter.Entry(master,text='m1 E',width=3)
        self.m1_E_entry.grid(row=2,column=2)

        self.m1_A_label = tkinter.Label(master,text='m1 A')
        self.m1_A_label.grid(row=3,column=1)
        self.m1_A_entry = tkinter.Entry(master,text="m1 A",width=3)
        self.m1_A_entry.grid(row=3,column=2)

        self.m1_Z_label = tkinter.Label(master,text='m1 Z')
        self.m1_Z_label.grid(row=4,column=1)
        self.m1_Z_entry = tkinter.Entry(master,text='m1 Z',width=3)
        self.m1_Z_entry.grid(row=4,column=2)

        self.m1_mass_label = tkinter.Label(master,text='m1 Mass')
        self.m1_mass_label.grid(row=5,column=1)
        self.m1_mass_entry = tkinter.Entry(master,text='m1 Mass',width=3)
        self.m1_mass_entry.grid(row=5,column=2)

##################################################################################
#Entries for m3 Particle (this is the heavy recoil)
        
        self.m3_name_label = tkinter.Label(master,text='m3 Name')
        self.m3_name_label.grid(row=1,column=3)
        self.m3_name_entry = tkinter.Entry(master,text='m3 Name',width=3)
        self.m3_name_entry.grid(row=1,column=4)

        self.m3_E_label = tkinter.Label(master,text='m3 E')
        self.m3_E_label.grid(row=2,column=3)
        self.m3_E_entry = tkinter.Entry(master,text='m3 E',width=3)
        self.m3_E_entry.grid(row=2,column=4)

        self.m3_A_label = tkinter.Label(master,text='m3 A')
        self.m3_A_label.grid(row=3,column=3)
        self.m3_A_entry = tkinter.Entry(master,text="m3 A",width=3)
        self.m3_A_entry.grid(row=3,column=4)

        self.m3_Z_label = tkinter.Label(master,text='m3 Z')
        self.m3_Z_label.grid(row=4,column=3)
        self.m3_Z_entry = tkinter.Entry(master,text='m3 Z',width=3)
        self.m3_Z_entry.grid(row=4,column=4)

        self.m3_mass_label = tkinter.Label(master,text='m3 Mass')
        self.m3_mass_label.grid(row=5,column=3)
        self.m3_mass_entry = tkinter.Entry(master,text='m3 Mass',width=3)
        self.m3_mass_entry.grid(row=5,column=4)

##################################################################################
#Gas property entries
        
        self.gaspressure_label = tkinter.Label(master,text='Gas Pressure (Torr)')
        self.gaspressure_label.grid(row=1,column=5)
        self.gaspressure_entry = tkinter.Entry(master,text='Gas Pressure (Torr)',width=6)
        self.gaspressure_entry.grid(row=1,column=6)

        self.gastype_label = tkinter.Label(master,text='Gas Type')
        self.gastype_label.grid(row=2,column=5)
        self.variable = StringVar()
        self.variable.set("SELECT GAS")
        self.gastype_entry = OptionMenu(master,self.variable, 'METHANE','P10','HELIUM')
        self.gastype_entry.grid(row = 2, column = 6)


##################################################################################
#Window Properties 
        
        self.windowthick_label = tkinter.Label(master,text='Mylar Window Thickness (ug/cm^2)')
        self.windowthick_label.grid(row=3,column=5)
        self.windowthick_entry = tkinter.Entry(master,text='Mylar Window Thickness (ug/cm^2)',width=6)
        self.windowthick_entry.grid(row=3,column=6)
##################################################################################
      
#        height = 18
#        width = 2
#        for i in range(height): #Rows
#            for j in range(width): #Columns
#                self.b = tkinter.Label(master, text="XXX")
#                self.b.grid(row=i, column=j+8)

##################################################################################
#This sets up an empty plot before the magic happens when the program is first
#started up.
        
        
        self.plot1 = ax.scatter(x,y)
        self.canvas = FigureCanvasTkAgg(fig,master=master)
        self.canvas.get_tk_widget().grid(row=0,column=0,columnspan=8)
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
        
        m1strip,m4strip = main_func(m1_name,m1_mass,m1_energy,m1_Z,m1_A,m4_name,m4_mass,m4_Z,m4_A,gastype,gaspressure)

        ax.clear()
        ax.set_title('Energy Loss Calculations',fontname='serif')
        ax.set_xlabel('Strip Number',fontname='serif')
        ax.set_ylabel('Energy Loss (MeV)',fontname='serif')
        ax.grid()
        ax.set_xlim(-1, 18)
        ax.set_ylim(0, 3)
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
