import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

'''
IR Spektren in Wässriger Lösung und der Gasphase der cis und trans Geometrie
'''

IR_cis = pd.read_csv('opt_sb_cis.out.ir.dat', sep='\\s+', header=None)
IR_cis_CPCM =  pd.read_csv('opt_cis_IS.out.ir.dat', sep='\\s+', header=None)
IR_trans = pd.read_csv('opt_sb_trans.out.ir.dat', sep='\\s+', header=None)
IR_trans_CPCM = pd.read_csv('opt_trans_IS.out.ir.dat', sep='\\s+', header=None)

fig, ax = plt.subplots(1, 2, figsize=(12, 5), layout="constrained")
fig.suptitle('Berechnete IR-Spektren der cis und trans Geometrie')

# Gasphase
ax[0].plot(IR_cis[0], IR_cis[1] /10, linewidth = 1, label = 'cis') #cis
ax[0].plot(IR_trans[0], IR_trans[1] /10, linewidth = 1, label = 'trans') #trans
ax[0].set_title("Gasphase")
ax[0].set_xlabel(r"$\tilde{\nu} \: [\mathrm{cm}^{-1}]$")
ax[0].invert_xaxis()
ax[0].set_ylabel(r"$T \:[\%]$")
ax[0].set_xlim(4000, 300)
ax[0].legend()


# CPCM(wasser)
ax[1].plot(IR_cis_CPCM[0], IR_cis_CPCM[1] , linewidth = 1, label = 'cis') #cis
ax[1].plot(IR_trans_CPCM[0], IR_trans_CPCM[1] , linewidth = 1, label = 'trans') #trans
ax[1].set_title("CPCM(Wasser)")
ax[1].set_xlabel(r"$\tilde{\nu} \: [\mathrm{cm}^{-1}]$")
ax[1].invert_xaxis()
ax[1].set_xlim(4000, 300)
ax[1].set_ylabel(r"$T \:[\%]$")
ax[1].legend()

plt.savefig('IR_cis_trans.pdf', format='pdf', bbox_inches='tight', dpi=600)

'''
UV/VIS Spektren der cis und trans Geometrie in der Gasphase und in Wässrigen Lösungen
'''

def wavenumber_to_eV(wavenumber):
    return wavenumber / 8065.54

def eV_to_wavenumber(energy):
    return energy * 8065.54

UVVIS_cis = pd.read_csv('TDDFT_cis.out.abs.dat', sep='\\s+', header=None)
UVVIS_cis_CPCM =  pd.read_csv('TDDFT_cis_IS.out.ABS.dat', sep='\\s+', header=None)
UVVIS_trans = pd.read_csv('TDDFT_trans.out.abs.dat', sep='\\s+', header=None)
UVVIS_trans_CPCM = pd.read_csv('TDDFT_trans_IS.out.ABS.dat', sep='\\s+', header=None)

fig, ax = plt.subplots(1, 2, figsize=(12, 5), sharey=True, layout="constrained")
fig.suptitle('Konvolutierte UV-VIS Spektren der cis und trans Geometrie')

# Gasphase
ax[0].plot(wavenumber_to_eV(UVVIS_cis[0]), UVVIS_cis[1], linewidth = 1, label = 'cis') #cis
ax[0].plot(wavenumber_to_eV(UVVIS_trans[0]), UVVIS_trans[1], linewidth = 1, label = 'trans') #trans
ax[0].set_title("Gasphase")
ax[0].set_xlabel(r"$E \: [\mathrm{eV}]$")
ax[0].set_ylabel(r"$I \:[\mathrm{a.u.}]$")
ax[0].set_xlim(wavenumber_to_eV(40000), wavenumber_to_eV(60000))
ax[0].legend()

secax0 = ax[0].secondary_xaxis(
    'top',
    functions=(eV_to_wavenumber, wavenumber_to_eV)
)
secax0.set_xlabel(r'$\tilde{\nu} \, [\mathrm{cm}^{-1}]$')

# CPCM(wasser)
ax[1].plot(wavenumber_to_eV(UVVIS_cis_CPCM[0]), UVVIS_cis_CPCM[1], linewidth = 1, label = 'cis') #cis
ax[1].plot(wavenumber_to_eV(UVVIS_trans_CPCM[0]), UVVIS_trans_CPCM[1], linewidth = 1, label = 'trans') #trans
ax[1].set_title("CPCM(Wasser)")
ax[1].set_xlabel(r"$E \: [\mathrm{eV}]$")
ax[1].set_ylabel(r"")
ax[1].set_xlim(wavenumber_to_eV(40000), wavenumber_to_eV(60000))
ax[1].legend()

secax1 = ax[1].secondary_xaxis(
    'top',
    functions=(eV_to_wavenumber, wavenumber_to_eV)
)
secax1.set_xlabel(r'$\tilde{\nu} \ [\mathrm{cm}^{-1}]$')

for secax in [secax0, secax1]:
    secax.xaxis.set_major_locator(MultipleLocator(5000))

plt.savefig('UVVIS_cis_trans.pdf', format='pdf', bbox_inches='tight', dpi=600)

'''
NEB in Wässriger Lösund und der Gasphase (Energieprofil des C-C-C-N Dihedralwinkels)
'''

phi_CCCN = np.array([9.611, 48.241, 67.891, 81.791, 93.620, 95.124 , 102.766, 111.951, 122.789, 138.188, 179.954])
dG = np.array([0.00, 2.33, 5.44, 7.69, 8.83, 8.66, 8.77, 7.74, 5.52, 1.60, -4.56])

fig, ax = plt.subplots(figsize=(12, 5), layout="constrained")
fig.suptitle('NEB Pfad der Isomerisierung')

ax.scatter( phi_CCCN, dG, marker='x', linewidth=1, label='NEB Bilder', color='blue')
ax.plot( phi_CCCN, dG, linewidth=1, ls='--', color='blue')

ax.set_xlabel(r"$\phi(\mathrm{C=C-C=N}) \: [\mathrm{°}]$")
ax.set_ylabel(r"$\Delta G \: [\mathrm{kcal}\cdot\mathrm{mol^{-1}}]$")
ax.set_xlim(phi_CCCN.min() - 5, phi_CCCN.max() + 5)
ax.set_ylim(-5, 15)
ax.legend()

img_0 = mpimg.imread('NEB_0.png')
img_TS = mpimg.imread('NEB_TS.png')
img_9 = mpimg.imread('NEB_9.png')

images = [(img_0, 15.611, dG[0]+4.5), (img_TS, 95.124, dG[5]+3), (img_9,  172, dG[10]+4.5)]

for img, x, y in images:
    imagebox = OffsetImage(img, zoom=0.15)
    annotation = AnnotationBbox(imagebox, (x, y), frameon=False)
    ax.add_artist(annotation)

plt.savefig('NEB.pdf', format='pdf', bbox_inches='tight', dpi=600)
plt.show()

'''
Energieprofil der Isomerisierung (cis, trans und TS Geometrie) in der Wässrigen und Gasphase
'''

dG_gas = np.array([1, 1, 1]) # cis - TS - tans
phi_gas = np.array([9.611, 95.363, 179.954]) # cis - TS - tans

dG_CPCM = np.array([1, 1, 1]) # cis - TS - tans
phi_CPCM = np.array([6.940, 95.363, 179.795]) # cis - TS - trans

fig, ax = plt.subplots(figsize=(10, 4), layout="constrained")
fig.suptitle('Energieprofil der Isomerisierungsreaktion')

ax.scatter(phi_gas, dG_gas , marker = 'x', linewidth = 1, label = 'Gasphase', color = 'blue')
ax.plot(phi_gas, dG_gas , linewidth = 1, ls = '--', color = 'blue')

ax.scatter(phi_CPCM, dG_CPCM, marker = 'x', linewidth = 1, label = 'CPCM(Wasser)', color = 'red')


'''
Vergleich der C-C und C-N Bindungslängen in der cis und trans Geometrie sowie des TS
'''

structure = ('cis', 'TS', 'trans')

bondlength_gas = {
    r'C$_1$=C$_2$': (1.351, 1.337, 1.353),
    r'C$_2$-C$_3$': (1.442, 1.469, 1.430),
    r'C$_3$=N': (1.300, 1.287, 1.301)
}

bondlength_CPCM = {
    r'C$_1$=C$_2$': (1.347, 1.337, 1.348),
    r'C$_2$-C$_3$': (1.448, 1.469, 1.437),
    r'C$_3$=N': (1.292, 1.287, 1.293)
}

fig, ax = plt.subplots(1, 2, figsize=(12, 5), layout="constrained", sharey=True)
fig.suptitle('Bindungslängen über den verlauf der Isomerisierung')

res_gas = ax[0].grouped_bar(bondlength_gas, tick_labels=structure, group_spacing=1)

for container in res_gas.bar_containers:
    ax[0].bar_label(container, padding=3, fmt='%.3f')

ax[0].set_ylabel(r'Bond length ($\mathrm{\AA}$)')
ax[0].set_ylim(1.2, 1.525)
ax[0].set_title('Gas phase')
ax[0].legend(loc='upper left', ncol=3)

res_CPCM = ax[1].grouped_bar(
    bondlength_CPCM,
    tick_labels=structure,
    group_spacing=1
)

for container in res_CPCM.bar_containers:
    ax[1].bar_label(container, padding=3, fmt='%.3f')

ax[1].set_title('CPCM (water)')
ax[1].legend(loc='upper left', ncol=3)

plt.savefig('Bondlength.pdf', format='pdf', bbox_inches='tight', dpi=600)
