# Athena Energy Loss Calculator

![Gui](/gui.png)

Energy loss simulation for ions in the Active Target High Efficiency Detector for Nuclear Astrophysics 

This package contains a python script that utilizes pysrim to calculate the energy loss of energetic nuclei through the target gas of ATHENA. 

Inputs include the projectile nulceus charge, mass, and energy as well as the target gas compisition and pressure. The output is a plot of the energy loss deposited in each strip of the detector. 


## Running 

Make sure you have the pysrim, matplotlib, numpy, and tkinter modules installed. 

SRIM must be installed on your computer either natively on windows or using WINE and some emulator on UNIX based operating systems. 

Before running, make sure in main_program.py you have entered the directory where SRIM.exe is installed as shown 

```
srim_executable_directory = r'C:\Users\drewblankstein\Documents\SRIM-2013'
```

Then run gui.py to start running the calculator. Input your energies and ion species properties and click Compute Energy Loss to make the magic happen! 
