import yt
import glob

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

@derived_field(name="he4_density",units="g/cm**3", force_override=True)
def _he4_rho(field,data):
   return data['density'] * data['he4 '] + yt.YTArray(np.ones(data['he4 '].shape)*10**-30,'g/cm**3')

@derived_field(name="ti44_density",units="g/cm**3", force_override=True)
def _he4_rho(field,data):
   return data['density'] * data['ti44'] + yt.YTArray(np.ones(data['ti44'].shape)*10**-30,'g/cm**3')



@derived_field(name="he4_cell_mass",units="g", force_override=True)
def _he4_cell_mass(field,data):
   return data['density'] * data['he4 ']*data['cell_volume'] + yt.YTArray(np.ones(data['he4 '].shape)*10**-30,'g')


#yt.add_field(('gas','he4rho') , function=he4_rho , units="g/cm**3",force_override=True)

#he4_mass = np.sum(data['cell_volume']*data['he4_density'])
#print("Total helium mass is = ", he4_mass)

list = glob.glob("super3d_hdf5_chk_*")
list.sort()
slice = list[5:6:1]



plotvar="ye  "
plotvar2 = "density"
plotvar3 = "temperature"
plotvar4 = "velocity"
plotvar5 = "rpv1"
plotvar6 = "phfa"
plotvar7 = "he4_density"
plotvar8 = "ti44_density"

lowdens = 1e7
yecon = 0.5
he4lowden = 10

#colormaps = ['viridis', 'inferno']
axis = [0, 1, 2]

for j in axis:
    for file in slice:
        print ("Analyzing file ... ", file)
        ds = yt.load(file)
        axis = j
        center = ("max", "dens")
    
    #    plot1 = yt.SlicePlot(ds,axis, plotvar7, origin='native')#, center = center)
    #    #plot1.set_colorbar_label((plotvar7),' ')
    #    plot1.set_colorbar_label((plotvar7),'He density (g cm$^{-3}$)')
    #    plot1.set_font_size(30)
    #    plot1.set_cmap(plotvar7, cmap='viridis')
    #    plot1.set_zlim(plotvar7,10,2e5)
    #    plot1.annotate_timestamp()
    #    plot1.zoom(15)
    #    plot1.save('plots/helium_den/') 
        
        plot2 = yt.SlicePlot(ds,axis, plotvar3, origin='native', center = center)
        plot2.set_colorbar_label((plotvar3),' ')
        #plot2.set_colorbar_label((plotvar3),'Temperature (K) ')
        plot2.set_font_size(30)
        plot2.set_cmap(plotvar3, cmap='magma')
        plot2.annotate_contour('pres',ncont=5,clim=(5e20,5e24), plot_args={"colors": "lime", "linewidths": 2})
        plot2.annotate_contour('density',ncont=5,clim=(5e3,5e5), plot_args={"colors": "white", "linewidths": 2}) 
        plot2.set_zlim(plotvar3,8e7,3e9)
        plot2.annotate_timestamp()
        plot2.zoom(20)
        plot2.save('plots/temperature/contours/')



 
