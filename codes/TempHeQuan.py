import yt
import glob
import re

#yt.enable_parallelism()


from yt.units import km
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.pyplot as plt 
#matplotlib inline
import numpy as np
#from yt.config import ytcfg
from yt import derived_field

@derived_field(name="velocity",units="auto", dimensions="velocity" )
def _velocity(field,data):
 return np.sqrt(data["velx"]**2+data["vely"]**2)

@derived_field(name="he4_Density",units="g/cm**3", force_override=True)
def _he4_rho(field,data):
   return data['density'] * data['he4 '] + yt.YTArray(np.ones(data['he4 '].shape)*10**-30,'g/cm**3')

@derived_field(name="he4_cell_mass",units="g", force_override=True)
def _he4_cell_mass(field,data):
   return data['density'] * data['he4 ']*data['cell_volume'] + yt.YTArray(np.ones(data['he4 '].shape)*10**-30,'g')


#yt.add_field(('gas','he4rho') , function=he4_rho , units="g/cm**3",force_override=True)

#he4_mass = np.sum(data['cell_volume']*data['he4_Density'])
#print("Total helium mass is = ", he4_mass)

filepath = '/scratch/06984/tg862835/PAPER_RUNS/17km/'
list = glob.glob(filepath + "super3d_hdf5_plt_cnt_*")
list.sort()
slice = list[246:-1:1]


plotvar="ye  "
plotvar2 = "density"
plotvar3 = "temperature"
plotvar4 = "velocity"
plotvar5 = "rpv1"
plotvar6 = "phfa"
plotvar7 = "he4_Density"

lowdens = 1e7 
yecon = 0.5 
he4lowden = 10
HeliumAmountArray = [] #np.array([])
MaxTempArray = [] #np.array([])
Time = []

filename = 'He4_MaxT_KE_RotKE_17kmAll.dat' 

for file in slice:
    print ("Analyzing file ... ", file)
    ds = yt.load(file)
    dat = ds.all_data()
    He4Mass = np.sum(dat['cell_volume'] * dat['he4_Density'])
    total_KE = np.sum(dat['cell_volume'] * dat['kinetic_energy'])
    
    velX = dat['velocity_x']
    velY = dat['velocity_y']
    velZ = dat['velocity_z']
    
    x = dat['x']
    y = dat['y']
    z = dat['z']
    
    r = np.sqrt(x**2 + y**2)
    
    cosphi = x/r
    sinphi = y/r
    
    vel_phi = (velY * cosphi) - (velX * sinphi)
    
    rot_E_kinetic = np.sum(0.5 * dat['density'] * vel_phi**2 * dat['cell_volume'])
    
    E_kinetic = total_KE - rot_E_kinetic

    #total_mass = np.sum(dat['cell_volume']*dat['density'])
    #print("Total mass is = ", total_mass.in_units('Msun'))

    MaxTemp = np.max(dat['temp'])
    time = ds.current_time

    He4MaxTemp = np.array([time,    He4Mass.in_units('Msun'),     MaxTemp.in_units('K'), total_KE.in_units('erg'), rot_E_kinetic.in_units('erg'), E_kinetic.in_units('erg')])
    
    print("Time is = ", time)
    print("Total helium mass is = ", He4Mass.in_units('Msun'))
    print("Maximum Temperature is = ", MaxTemp)
    print("KE is = ", total_KE)
    print("rot_E_kinetic is = ", rot_E_kinetic)

   
    with open(filename, 'a') as f:
         f.write('\n{}'.format(He4MaxTemp))



