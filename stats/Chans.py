import numpy as np
from scipy.stats import stats
from mne.stats import fdr_correction



# Test for significantly different channels between two groups
def difference(gr_one, gr_two, ch_names, alpha):
  
  p_vals = []
  for ch_i, ch in enumerate(ch_names):
    gr_one_ch = [ p[ch_i ] for p in gr_one]
    gr_two_ch = [ p[ch_i ] for p in gr_two]
    t, p      = stats.ttest_ind(gr_one_ch, gr_two_ch)
    p_vals.append(p)
    
  _, pval_corrected = fdr_correction(p_vals, alpha=alpha, method='indep')
  sig_chs = [ i for i, p_val in enumerate(pval_corrected) if p_val < alpha ]
  
  return sig_chs, pval_corrected



# Get the average value of a list of channels
def avg_of_sig(gr_one, gr_two, sig_chs):
  
  gr_one = [ [ v for i, v in enumerate(p) if i in sig_chs ] for p in gr_one ]
  gr_two = [ [ v for i, v in enumerate(p) if i in sig_chs ] for p in gr_two ]
  
  gr_one_avg = np.average(gr_one, axis=1)
  gr_two_avg = np.average(gr_two, axis=1)
  
  return gr_one_avg, gr_two_avg