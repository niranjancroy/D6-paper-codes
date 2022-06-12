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


@derived_field(name="he4_density",units="g/cm**3", force_override=True)
def _he4_rho(field,data):
   return data['density'] * data['he4 '] + yt.YTArray(np.ones(data['he4 '].shape)*10**-30,'g/cm**3')

@derived_field(name="ti44_density",units="g/cm**3", force_override=True)
def _he4_rho(field,data):
   return data['density'] * data['ti44'] + yt.YTArray(np.ones(data['ti44'].shape)*10**-30,'g/cm**3')

@derived_field(name="c12_density",units="g/cm**3", force_override=True)
def _he4_rho(field,data):
   return data['density'] * data['c12 '] + yt.YTArray(np.ones(data['c12 '].shape)*10**-30,'g/cm**3')

#@derived_field(name="o16_density",units="g/cm**3", force_override=True)
#def _he4_rho(field,data):
#   return data['density'] * data['o16 '] + yt.YTArray(np.ones(data['o16 '].shape)*10**-30,'g/cm**3')


@derived_field(name="he4_cell_mass",units="g", force_override=True)
def _he4_cell_mass(field,data):
   return data['density'] * data['he4 ']*data['cell_volume'] + yt.YTArray(np.ones(data['he4 '].shape)*10**-30,'g')

@derived_field(name="c12_cell_mass",units="g", force_override=True)
def _he4_cell_mass(field,data):
   return data['density'] * data['c12 ']*data['cell_volume'] + yt.YTArray(np.ones(data['c12 '].shape)*10**-30,'g')

@derived_field(name="mass",units="g", force_override=True)
def _he4_cell_mass(field,data):
   return data['density'] *data['cell_volume'] + yt.YTArray(np.ones(data['density'].shape)*10**-30,'g')

#yt.add_field(('gas','he4rho') , function=he4_rho , units="g/cm**3",force_override=True)

#he4_mass = np.sum(data['cell_volume']*data['he4_density'])
#print("Total helium mass is = ", he4_mass)

filepath = '/scratch/06984/tg862835/PAPER_RUNS/17km/'
list = glob.glob(filepath + "super3d_hdf5_chk_*")
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
dir = '/work2/06984/tg862835/stampede2/D6_Paper/plots' #don't add / at end

#colormaps = ['viridis', 'inferno']

for file in slice:
    print ("Analyzing file ... ", file)
    ds = yt.load(file)
    axis = 2
    zoom = 10
    #center = [0 0 0]#("max", "temp")

    dat = ds.all_data()
    he4_mass = np.sum(dat['cell_volume']*dat['he4_density'])
    c12_mass = np.sum(dat['cell_volume']*dat['c12_density'])
    total_mass = np.sum(dat['cell_volume']*dat['density'])
    
    he4_frac = he4_mass / total_mass 
    c12_frac = c12_mass / total_mass
    print('He4, O16, and C12 fractions are = {},{}, and {} respectively.'.format(he4_frac,1-he4_frac-c12_frac, c12_frac))
   # #print("Total mass is = ", total_mass.in_units('Msun'))
    print("Total helium mass is = ", he4_mass.in_units('Msun'))
    sp = ds.sphere("max", (1.5e4, "km"))
    total_he4_in_sphere = sp.quantities.total_quantity(["he4_cell_mass"])
    total_c12_in_sphere = sp.quantities.total_quantity(["c12_cell_mass"])
    total_mass_in_sphere = sp.quantities.total_quantity(["mass"])
    he4_frac_sphr = total_he4_in_sphere / total_mass_in_sphere
    c12_frac_sphr = total_c12_in_sphere / total_mass_in_sphere

    print('Helium inside primary = {}'.format(total_he4_in_sphere.in_units('Msun')))
    #print('He4, O16, and C12 fractions in primary are = {}, {}, {} respectively.'.format(he4_frac_sphr, 1-he4_frac_sphr-c12_frac_sphr, c12_frac_sphr))
   # print("Total helium in primary WD = ",total_he4_in_sphere.in_units('Msun'))

   # dat = ds.all_data()
   # he4_mass = np.sum(dat['cell_volume']*dat['he4_density'])
   # #total_mass = np.sum(dat['cell_volume']*dat['density'])
   # #print("Total mass is = ", total_mass.in_units('Msun'))
   # print("Total helium mass is = ", he4_mass.in_units('Msun'))
   # sp = ds.sphere("max", (1.5e4, "km"))
   # total_he4_in_sphere = sp.quantities.total_quantity(["he4_cell_mass"])
   # print("Total helium in primary WD = ",total_he4_in_sphere.in_units('Msun'))

    plot1 = yt.SlicePlot(ds,axis, plotvar7, origin='native')#, center = center)
    #plot1.set_colorbar_label((plotvar7),' ')
    plot1.set_colorbar_label((plotvar7),'He density (g cm$^{-3}$)')
    plot1.set_font_size(30)
    plot1.set_cmap(plotvar7, cmap='viridis')
    plot1.set_zlim(plotvar7,10,2e5)
    plot1.annotate_timestamp()
    plot1.zoom(zoom)
    plot1.save(dir+'/helium_den/') 
    
    plot2 = yt.SlicePlot(ds,axis, plotvar3, origin='native')#, center = center)
    #plot2.set_colorbar_label((plotvar3),' ')
    plot2.set_colorbar_label((plotvar3),'Temperature (K) ')
    plot2.set_font_size(30)
    plot2.set_cmap(plotvar3, cmap='inferno')
    #plot2.set_zlim(plotvar3,8e7,3e9)
    plot2.annotate_timestamp()
    #plot2.annotate_grids()
    plot2.zoom(zoom)
    plot2.save(dir+'/temperature/') 

    plot3 = yt.SlicePlot(ds,axis, plotvar8, origin='native')#, center = center)
    plot3.set_colorbar_label((plotvar8),'Ti44 density (g cm$^{-3}$)')
    #plot3.set_colorbar_label((plotvar8),' ')
    plot3.set_font_size(30)
    plot3.set_cmap(plotvar8, cmap='cividis')
    plot3.set_zlim(plotvar8,1e-3,1.2e2)
    plot3.annotate_timestamp()
    #plot2.annotate_grids()
    plot3.zoom(zoom)
    plot3.save(dir+'/titanium_dens/') 

    plot4 = yt.SlicePlot(ds,axis, plotvar2, origin='native')#, center = center)
    #plot4.set_colorbar_label((plotvar2),' ')
    plot4.set_font_size(30)
    plot4.set_colorbar_label(plotvar2,"Density (g cm$^{-3}$)")
    plot4.set_cmap(plotvar2, cmap='magma')
    plot4.set_zlim(plotvar2,10,5e7)
    plot4.annotate_timestamp()
    #plot4.annotate_grids()
    plot4.zoom(zoom)
    plot4.save(dir+'/density/') 



# 3c397########################################### 

#plotting velocity

# ds = yt.load(file)
# plot4 = yt.SlicePlot(ds,'theta', plotvar4, origin='native')
# plot4.set_font_size(35)
# plot4.set_log(plotvar4,False)
# plot4.set_cmap(plotvar4, cmap='viridis')
# #plot4.set_zlim(plotvar4,3e3,7e8)
# plot4.annotate_timestamp()
# plot4.zoom(20)
# #plot3.annotate_grids()
# plot4.set_center((-0.5,-0.0))
# plot4.pan_rel((0.5, 0.0))
# plot4.annotate_velocity(plot_args={"headwidth": 10})
# plot4.annotate_contour('dens',ncont=1, clim=(lowdens,lowdens),plot_args={"colors": "black", "linewidths": 2}) 
# #plot3.annotate_contour('ye  ',ncont=1, clim=(yecon,yecon),plot_args={"colors": "blue", "linewidths": 3})
# plot4.save('velocity/17Aug20/')

################ PLOTTING Y_e#########################

# plot = yt.SlicePlot(ds,'theta', plotvar, origin='native')
# plot.set_font_size(35)
# plot.set_log(plotvar,False)
# plot.set_cmap(plotvar, cmap='Spectral')
# plot.set_zlim(plotvar,0.46e0,0.5e0)
# plot.annotate_timestamp()
# plot.zoom(10)
# plot.annotate_grids()
# plot.set_center((-0.5,-0.0))
# plot.pan_rel((0.5, 0.0))
# plot.annotate_contour('dens',ncont=1, clim=(lowdens,lowdens),plot_args={"colors": "black", "linewidths": 3})
 #plot.annotate_contour('ye  ',ncont=1, clim=(yecon,yecon),plot_args={"colors": "blue", "linewidths": 3})
# plot.save('y_e/13may20/')


####################3 PLOTTING DENSITY ################
# plot2 = yt.SlicePlot(ds,'theta', plotvar2, origin='native')
# plot2.set_font_size(35)
# plot2.set_log(plotvar2,False)
# plot2.set_cmap(plotvar2, cmap='jet')
# plot2.set_zlim(plotvar2,1e-3,2.2e9)
# plot2.annotate_timestamp()
# plot2.zoom(15)
# plot2.set_center((-0.5,-0.0))
# plot2.pan_rel((0.5, 0.0))
# plot2.annotate_contour('dens',ncont=1, clim=(lowdens,lowdens),plot_args={"colors": "black", "linewidths": 2})
# plot2.annotate_velocity()
# plot2.save('density/4sep20/')


################## phfa #############################

# plot6 = yt.SlicePlot(ds,'theta', plotvar6, origin='native')
# plot6.set_font_size(35)
# plot6.set_log(plotvar6,False)
# plot6.set_cmap(plotvar6, cmap='Spectral')
## plot5.set_zlim(plotvar5,1e-3,2.2e9)
# plot6.annotate_timestamp()
# plot6.zoom(50)
# plot6.set_center((-0.5,-0.0))
# plot6.pan_rel((0.5, 0.0))
# plot6.annotate_contour('dens',ncont=1, clim=(lowdens,lowdens),plot_args={"colors": "black", "linewidths": 2}) 
## plot5.annotate_velocity()
# plot6.save('phfa/4sep20/')

