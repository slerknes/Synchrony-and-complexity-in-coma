import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def plot(values, truth, title='', ax=None):
  
  density = stats.gaussian_kde(values)
  x = np.linspace(0,1,100)
  ax.set_yticks([])
  max_val = max([density(v) for v in x])
  ax.fill_between(x, density(x), 0, color='black', alpha=0.2)
  ax.plot(x, density(x), color='black', alpha=0.6)
  ax.plot([truth, truth], [0, max_val], color='#d73027')
  ax.set_title(title)

def plot_multiple(title='', elements=[]):
  fig, axs = plt.subplots(2, 3)
  fig.suptitle(title, fontsize=22)
  x = 0
  y = 0
  for i, e in enumerate(elements):
    plot(e[0], e[1], e[2], ax=axs[x, y])
    x = x + 1 if y == 2 else x
    y = (y+1) % 3
  for i in range(len(elements), 6):
    axs[x, y].axis('off')
    x = x + 1 if y == 2 else x
    y = (y+1) % 3
  plt.show()