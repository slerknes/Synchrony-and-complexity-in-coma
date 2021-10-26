from scipy import stats
import numpy as np
from mne.stats import fdr_correction



# Significance test for permutation
def permutation_significance(truth, permutation_list):
  return stats.wilcoxon([truth]*len(permutation_list), permutation_list)



# Assess the sensitivity, specificity, accuracy of a threshold, given groups
def threshold_accuracy(groups, threshold, decimal_places=2):
  
  tp              = sum([1 for x in groups[0] if np.round(x, decimal_places) > np.round(threshold, decimal_places)])
  fn              = sum([1 for x in groups[0] if np.round(x, decimal_places) < np.round(threshold, decimal_places)])
  fp              = sum([1 for x in groups[1] if np.round(x, decimal_places) > np.round(threshold, decimal_places)])
  tn              = sum([1 for x in groups[1] if np.round(x, decimal_places) < np.round(threshold, decimal_places)])
  
  sensitivity     = tp / (tp+fn) if tp > 0 else 0
  specificity     = tn / (tn+fp) if tn > 0 else 0
  accuracy        = (tn+tp) / (tp+fp+fn+tn)
  
  ppv             = tp / (tp+fp) if (tp+fp) else 0
  npv             = tn / (fn+tn) if (fn+tn) else 0
  
  return [[tp, fn], [fp, tn]], ppv, npv, sensitivity, specificity, accuracy



# Assess the sensitivity, specificity, accuracy of a threshold, given groups
def plv_group_diff(groups):
  t, p = stats.ttest_ind(groups[0], groups[1])
  print('GROUP ONE: N = '  + str(len(groups[0])) +\
                 ', M = '  + str(round(np.average(groups[0]),2)) +\
                 ', SD = ' + str(round(np.std(groups[0]),2)))
  print('GROUP TWO: N = '  + str(len(groups[1])) +\
                 ', M = '  + str(round(np.average(groups[1]),2)) +\
                 ', SD = ' + str(round(np.std(groups[1]),2)))
  df = len(groups[0])+len(groups[1])-2
  print('t(' + str(df) + ') = ' + str(round(t,2)) + ', p = ' + str(round(p,5)))
  print('t  = ' + str(round(t,2)) + '\np  = ' + str(round(p,5)))
  print('df = '+str(df))



# Identify electrode-pairs significantly different between two groups
# and return the patient-average of these per participant
def plv_sig_pairs(groups, alpha):
  
  n_eles       = 19
  
  p_vals       = []
  t_vals_pairs = [[0 for a in range(b)] for b in range(n_eles)]
  p_vals_pairs = [[1 for a in range(b)] for b in range(n_eles)]
  
  # Identify statistical difference between electrode-pairs
  for ch_a in range(n_eles):
    for ch_b in range(ch_a):
      
      # Get the PLV values for a specific electrode pair for estimate groups
      pair_vals = [ [ groups[gr_i][0][p_i][ch_a][ch_b][0] for p_i in
                        range(len(groups[gr_i][0]))
                    ] for gr_i in range(2)
                   ]

      stat, p = stats.ttest_ind(pair_vals[0], pair_vals[1])
      
      t_vals_pairs[ch_a][ch_b] = stat
      p_vals.append(p)
      
  _, pval_corrected = fdr_correction(p_vals, alpha=alpha, method='indep')
  
  # Generate empty list to hold values
  sig_vals = [ [ [ [] for p_i in range(len(groups[gr_i][sub_gr_i]))
                 ] for sub_gr_i in range(len(groups[gr_i]))
               ] for gr_i in range(len(groups))
             ]
  
  i             = 0
  count         = 0
  
  for ch_a in range(n_eles):
    for ch_b in range(ch_a):
      
      if pval_corrected[i] < alpha:
        
        count = count + 1
        p_vals_pairs[ch_a][ch_b] = pval_corrected[i]
        
        pair_vals = [ [ [ groups[gr_i][sub_gr_i][p_i][ch_a][ch_b][0] for p_i in
                            range(len(groups[gr_i][sub_gr_i]))
                        ] for sub_gr_i in
                          range(len(groups[gr_i]))
                      ] for gr_i in
                        range(len(groups))
                    ]
        
        for gr_i, gr in enumerate(pair_vals):
          for sub_gr_i, sub_gr in enumerate(gr):
            for p_i, p_val in enumerate(sub_gr):
              sig_vals[gr_i][sub_gr_i][p_i].append(p_val)
              
      i = i + 1
  
  print('There were ' + str(count) + ' significant electrode-pairs')
  
  sub_sig_avg = [ [ [ np.average(sig_vals[gr_i][sub_gr_i][p_i]) for p_i in
                        range(len(sig_vals[gr_i][sub_gr_i]))
                    ] for sub_gr_i in
                      range(len(sig_vals[gr_i]))
                  ] for gr_i in
                    range(len(sig_vals))
                ]

  return t_vals_pairs, p_vals_pairs, sub_sig_avg, pval_corrected