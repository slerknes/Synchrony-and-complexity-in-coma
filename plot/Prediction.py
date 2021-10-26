import matplotlib.pyplot as plt
import numpy as np

def rand_jitter(pos, arr):
  x_arr = []
  x = pos - 0.1
  for i in range(len(arr)):
    x_arr.append(x + np.random.randint(-50,50) / 1000)
    x = x + 0.1
    if x >= (pos + 0.19):
      x = pos - 0.1
  return x_arr

def plot(title, ylabel, groups, thresholds, ylim):
  
  fig = plt.figure(num=None, figsize=(3, 3), dpi=300,
                   facecolor='w', edgecolor='k')
  
  plt.tight_layout()
  
  plt.rc('xtick', labelsize='x-small')
  plt.rc('ytick', labelsize='x-small')
  
  font = {'family' : 'sans',
          'size'   : 4.5}
  plt.rc('font', **font)

  ax = fig.add_axes([0.25, 0.25, 0.7, 0.7])
  
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)
  ax.spines['bottom'].set_visible(False)
  ax.spines['left'].set_linewidth(0.25)

  ax.tick_params(width=0.5, length=2)

  group_name  = ['Survivor', 'Non-survivor', 'Control']
  x_pos_color = ['#1b9e77', 'none', '#d95f02', 'none', 'none']
  x_facecolor = ['none', '#1b9e77', 'none', '#d95f02', '#7570b3']
  x_leg_color = ['#1b9e77', 'none', '#d95f02', 'none', '#7570b3']
  
  x_i         = 0
  
  for gr_i, gr in enumerate(groups):
    ax.scatter([-1], [0], marker='o', color='none', facecolors=x_leg_color[x_i],
               label=group_name[gr_i], alpha=.5, s=25)
    for _, sub_gr in enumerate(gr):
      ax.scatter(rand_jitter(x_i * 0.6, sub_gr), np.sort(sub_gr),
                 color=x_pos_color[x_i], facecolors=x_facecolor[x_i],
                 alpha=.5, s=25)
        
      x_i = x_i + 1

  for e in thresholds:
    ax.plot([-0.3,2.7], [e, e], linewidth=0.25, color='black')
  
  plt.xticks([])
  plt.xlim(-0.3, 2.7)
  plt.yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
             ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9'])
  plt.ylim(ylim)
  plt.tight_layout()
  
  plt.plot([-1], [0], marker='o', color='w', label='Pilot',
           markerfacecolor='white', markersize=4, markeredgecolor='black')
  plt.plot([-1], [0], marker='o', color='w', label='Test',
           markerfacecolor='gray', markersize=4, markeredgecolor='gray')
  plt.plot([-1], [0], marker='o', color='w', label=' ',
           markerfacecolor='white', markersize=4, markeredgecolor='white')
  
  plt.ylabel(ylabel)
  plt.title(title)
  
  ax.legend(loc='lower center', frameon=False,
            bbox_to_anchor=(0.5, 0), ncol=2,
            fancybox=False, shadow=False,
            labelspacing=1, borderpad=1,
            fontsize='x-small')

  plt.show()