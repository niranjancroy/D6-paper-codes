import numpy as np 
import matplotlib.pyplot as plt

data = np.loadtxt("He4MaxTemp136kmAll.dat")

Time = data[:,0]
He4Mass = data[:,1]
MaxTemp = data[:,2]

fig, (ax1, ax2) = plt.subplots(2,1, figsize = (6,8), dpi= 100)


ax1.plot(Time, He4Mass, 'g')
#ax1.set_xlabel('Time (s)', fontsize = 18)
ax1.set_ylabel('He4 mass (Msun)', fontsize = 18)



ax2.plot(Time, MaxTemp)
ax2.set_xlabel('Time (s)', fontsize = 18)
ax2.set_ylabel('T_max (K)', fontsize = 18)

plt.tight_layout()
plt.savefig("EvolutionHe4MaxTemp.png")

print('Figure saved....')
