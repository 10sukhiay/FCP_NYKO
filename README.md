# Simulating the airborne transmission of coronavirus for a network of rooms


### Authors

- Oscar Bond

- Kaelan Melville

- Yazad Sukhia

- Nathan Wooster


### Description

This code creates a COVID-19 simulation. The code simulates both the transmission of the virus within a room, and the effect of individuals 
travelling between rooms across a network. The simulation is carried on a network level for individual days, 
and at a room level for a number of iterations every day.


### Dependencies

These common python libraries need to be installed. They are imported at the beginning of the scripts:

- argparse

- numpy

- pandas

- random

- math

- matplotlib

- networkx

- seaborn


### Installing
**The main script to be downloaded is:**

simulation_NYKO.py

**The modules that also must be downloaded that it calls are:**

Person_Class.py

animate.py

area.py

Heat_Mapping.py

other_functions.py

update.py


### Executing Program

The script can be used to:

1. Show an amination of the simulation on screen
2. Create a simulation over a number of days
3. Show a plot of the network
4. Show a plot of the status of people

This is all run from the simulation_NYKO.py file. 

The file can be run from the command line thanks to the command line 
interface. This allows parameters to be changes without editing the code. e.g.:

    $ python simulator.py               # run simulation with default settings
    $ python simulator.py --number=50    # have 50 people in the room network
    $ python simulator.py --help        # show all command line options

 
### Acknowledgments

We would like to acknowledge Perla Jazmin Mayo Diaz de Leon for her help and guidance with this unit.
