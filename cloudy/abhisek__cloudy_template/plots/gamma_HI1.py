import astropy.table as t
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import glob
from matplotlib.ticker import ScalarFormatter
from astropy.cosmology import Planck15 as planck
import scipy.optimize as sciopt


# setting the figure
font = {'family': 'serif', 'weight': 'normal', 'size': 18}
plt.rc('font', **font)
mpl.rcParams['axes.linewidth'] = 1.5

figure_size = [10, 6]
fig, ax = plt.subplots(1, 1, figsize=(figure_size[0], figure_size[1]))

alpha=0.9
figname='Gamma_HI.pdf'


x=0.1
y=0.175e-12
l='Kollmeier et al. 2014'
#ax.scatter(x, y, label=l, marker='*', s=300, c='blue')

uvb_array= [14, 15, 16, 17, 18, 19, 20]

path_gamma_files  = '/home/abhisek/mega/thesis_plot/uvb/cgm_uvb/cgm_uvb/paper_plots/gamma_HI_files/'
al = 0.9
for Q in uvb_array:
  q_name = 'Q{}'.format(Q)
  label = 'KS19 ({})'.format(q_name)
  gamma_file = path_gamma_files + 'Gamma_HI_KS18_Q{}.fits'.format(Q)
  data = t.Table.read(gamma_file)
  if  Q == 18:
      ax.plot(data['z'], data['g']/1e-12,  label=label, linewidth=3, alpha= al)
  else:
      ax.plot(data['z'], data['g']/1e-12,  label=label, linewidth=2, alpha= al)

  #ax.plot(z, g, color='k', label=label, linestyle='-', dashes=(5, 4), linewidth=2, alpha= al)

uvb_model = 'FG20'
file_name  =  path_gamma_files + 'Gamma_HI_{}.fits'.format(uvb_model)
data =  t.Table.read(file_name)
ax.plot(data['z'], data['g']/1e-12,  label=uvb_model, linewidth=3, linestyle  = '--',alpha = alpha, c= 'cyan')

uvb_model = 'P19'
file_name  =  path_gamma_files + 'Gamma_HI_{}.fits'.format(uvb_model)
data =  t.Table.read(file_name)
ax.plot(data['z'], data['g']/1e-12,  label=uvb_model, linewidth=3, linestyle  = '-.',alpha = alpha, c= 'grey')



#ax.plot(z, g, color='k', label=r'Khaire & Srianand 2018 ', linewidth=2, alpha=0.8)

#uvb=np.loadtxt('/home/vikram/Work/data_literature/gamma_h1/HM_gama.dat')
#z=uvb[:,0]
#g=uvb[:,1]
#ax.plot(z, g, color='magenta', label='Haardt & Madau 2012', linestyle='-.', linewidth=2, dashes=(5, 4, 1, 2), alpha=0.8)
#ax.plot(z, g, color='magenta', label='Haardt & Madau 2012', alpha=0.8)

# Gaikwad et al 2018
pz=np.array([0.11, 0.21, 0.31, 0.41])
pg=np.array([0.066, 0.1, 0.145, 0.210])*1e-12/1e-12
pe=np.array([0.015, 0.021, 0.037, 0.052])*1e-12/1e-12
t = ['g', 'orange', 'b', 'm', 'r']
l='Gaikwad et al. 2017'
ax.errorbar(pz, pg, pe, marker='D', label=l, markersize=8, ls='', c='k',  alpha=0.8, elinewidth=2.5, zorder = 10, capsize=4, capthick=2.2)


kz=np.array([0.03, 0.1, 0.2, 0.3,0.41])
kg=np.array([0.585, 0.756, 1.135, 1.479,1.418])*1e-13/1e-12
ke=np.array([0.17, 0.181, 0.32, 0.48,0.55])*1e-13/1e-12
t = ['g', 'orange', 'b', 'm', 'r']
l='Khaire et al. 2019'
ax.errorbar(kz, kg, ke, marker='s', label=l, markersize=8, ls='', c='g',  alpha=0.8, elinewidth=2.5, zorder = 10, capsize=4, capthick=2.2)


bz=np.array([2,3,4])
bg=np.array([1.29,0.86,0.97])*1e-12/1e-12
be1=np.array([0.8,0.34,0.48])*1e-12/1e-12
be2=np.array([0.46,0.26,0.33])*1e-12/1e-12
be=np.array([0.7,0.32,0.45])*1e-12/1e-12
t = ['g', 'orange', 'b', 'm', 'r']
l='Bolton et al. 2007'
ax.errorbar(bz, bg, be, marker='s', label=l, markersize=8, ls='', c='cyan',  alpha=0.8, elinewidth=2.5, zorder = 10, capsize=4, capthick=2.2)


bez=np.array([2.4,2.8,3.2,3.6,4.0])
beg=np.array([1.0351,0.8590,0.7889,0.7998,0.8472])*1e-12/1e-12
bee=np.array([0.32,0.26,0.23,0.24,0.23])*1e-12/1e-12
t = ['g', 'orange', 'b', 'm', 'r']
l='Becker et al. 2013'
ax.errorbar(bez, beg, bee, marker='s', label=l, markersize=8, ls='', c='purple',  alpha=0.8, elinewidth=2.5, zorder = 10, capsize=4, capthick=2.2)



l='Caruso et al. 2019'
z=[0.004,]
g=[7.27e-14/1e-12,]
err1=[2.93e-14/1e-12,]
err2=[2.90e-14/1e-12,]
ax.errorbar(z, g, yerr=[err1, err2,],  marker='s', label=l, markersize=8, zorder=11,  c='gold',
            alpha=alpha,  elinewidth=2.5, clip_on=False,capsize=4)

ax.set_yscale('log')
ax.set_ylabel(r'$\Gamma_{\rm H \, I}$ ($10^{-12}$ s$^{-1} )$')
ax.set_xlabel('Redshift')
ax.legend( loc = 'lower right', fontsize = 12, handlelength=3.6, ncol=2, labelspacing=1 )


ax.set_xlim(-0.1, 4.2)
ax.set_ylim(3*0.01, 2.1)
ax.tick_params(direction='in', length=7, width=1.7)
ax.tick_params(direction='in', which='minor', length=4, width=1.7)
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_ticks_position('both')
#ax.ticklabel_format(axis='y', style='sci')
#ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))



for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(1.7)

#ax.legend(loc='lower right')

fig.tight_layout(rect=[-0.03, -0.03, 1.02, 1.02])

fig.savefig(figname, bbox_inches='tight')

plt.show()

