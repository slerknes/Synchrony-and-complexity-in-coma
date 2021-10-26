import matplotlib.pyplot as plt
import numpy as np


# Jitter x-axis values
def rand_jitter(pos, arr):
  x_arr = []
  x = pos - 0.1
  for i in range(len(arr)):
    x_arr.append(x + np.random.randint(-50,50) / 1000)
    x = x + 0.1
    if x >= (pos + 0.19):
      x = pos - 0.1
  return x_arr



# Plot group data
def plot(title, ylabel, groups, group_name, colors, save=False):
  
  if len(groups) == 3:
    fig = plt.figure(num=None, figsize=(6, 4), dpi=200,
                     facecolor='w', edgecolor='k')
    plt.xlim(0.4, 3.6)
  else:
    fig = plt.figure(num=None, figsize=(3, 6), dpi=200,
                     facecolor='w', edgecolor='k')
    plt.xlim(0.6, 2.4)
    
  plt.rc('xtick', labelsize='x-small')
  plt.rc('ytick', labelsize='x-small')

  ax = fig.add_axes([0.15, 0.15, 0.8, 0.8])
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)

  bp = ax.violinplot(groups, positions=list(range(1,len(groups)+1)),
                     widths=0.5,
                     showmeans=False,
                     showmedians=False,
                     showextrema=False,
                     vert=True,
                     points=1000,
                     bw_method='silverman')
  
  for pc_i, pc in enumerate(bp['bodies']):
      pc.set_facecolor(colors[pc_i])
      pc.set_alpha(0.15)
      
  for gr_i, gr in enumerate(groups):
    ax.scatter( rand_jitter((gr_i+1) * 1, gr),
                np.sort(gr),
                color = 'none',
                facecolors = colors[gr_i],
                alpha = .5,
                s = 25,
                label = group_name[gr_i])
    
  plt.ylabel(ylabel)
  plt.title(title)
  plt.xticks(list(range(1,len(groups)+1)), group_name)
  plt.show()