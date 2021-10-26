# Illustrative code to make use of the methods used in the PLV calculation

from calc import Calc_PLV
from stats import Stat_PLV, Permute, Classifier
from plot import Prediction, Distributions, Spread
from helpers import split_groups

data_path       = ''

survivors       = [ ] # List of IDs associated with recordings
non_survivors   = [ ] # List of IDs associated with recordings
patients        = survivors + non_survivors

ch_names        = [ ] # Channel names
n_channels      = len(ch_names) # Number of electrodes

# Set parameters
split           = # Int: ID to make split between pilot and test
fmin, fmax      = # Touple of floats: Frequency range to calculate PLV within
alpha           = # Float: Alpha threshold for electrode-pairs test
n_permutations  = # Int: Number of permutations
sfreq           = # Float: Sampling frequency

# Calculate PLV values
plv_pats        = Calc_PLV.calc(data_path, ids = patients,
                                fmin = fmin, fmax = fmax,
                                sfreq = sfreq, n_eles = n_channels)

# Split the groups into separate lists
surv_est        = split_groups(plv_pats, 'PLV_ch', survivors, split, '-')
nsrv_est        = split_groups(plv_pats, 'PLV_ch', non_survivors, split, '-')
surv_tst        = split_groups(plv_pats, 'PLV_ch', survivors, split, '+')
nsrv_tst        = split_groups(plv_pats, 'PLV_ch', non_survivors, split, '+')

# Survivors, non-survivors, controls. Further split in pilot and test
groups          = [ [surv_est, surv_tst], [nsrv_est, nsrv_tst] ]

# Identify pairs significant different between survivors and non-survivors
# Sig_avg:
#   First dimension of sig_avg indicates group (surv/nsurv/[control])
#   Second dimension of sig_avg indicates subset (pilot/validation)
t_vals, p_vals_pairs, sig_avg, p_vals = Stat_PLV.plv_sig_pairs(groups, alpha)

# Plot PLV spread - use alpha = 1 to get from all electrodes
Spread.plot('', 'Phase-locking value',
            [sig_avg[0][0], sig_avg[1][0]],
            group_name = ['Survivor', 'Non-survivor'],
            colors = ['#1b9e77', '#d95f02'], save=False)

# Get number of significant connections per electrode
sig_conn_per_el = Calc_PLV.n_sig_conn(n_channels, p_vals_pairs, alpha)

# Display group statistics
print('\nSurvivors v. non-survivors test')
Stat_PLV.plv_group_diff([sig_avg[0][1], sig_avg[1][1]])

# Identify best thresholds given pilot group values
tresh_alts      = Classifier.find_best_split([sig_avg[0][0], sig_avg[1][0]])

# Iterate through all possible best thresholds
for i, threshold in enumerate(tresh_alts):

  print('\nThreshold value: ' + str(threshold))

  Prediction.plot('', 'Phase-locking value', sig_avg,
                  thresholds=[threshold], ylim=(0.15, 0.9))

  # Permutation tests and tests for classification accuracy
  # Example shows pilot group. For validation group:
  #   Stat_PLV.threshold_accuracy([sig_avg[0][1], sig_avg[1][1]], threshold)
  # AND
  #   Permute.permute(estimate_group = [sig_avg[0][0], sig_avg[1][0]],
  #                   test_group = [sig_avg[0][1], sig_avg[1][1]],
  #                   n_permutations = n_permutations,
  #                   shuffle_test = False,
  #                   shuffle_estimate = True,
  #                   threshold = threshold)

  # Sig_avg:
  #   First dimension of sig_avg indicates group (surv/nsurv/[control])
  #   Second dimension of sig_avg indicates subset (pilot/validation)
  sub_groups    = [sig_avg[0][0], sig_avg[1][0]]

  # Assess threshold accuracy
  outcome, ppv, npv, sens, spec, acc = Stat_PLV.threshold_accuracy(sub_groups,
                                                                   threshold)

  # Permutation tests
  ppv_scr, npv_scr, sens_scr, spec_scr, acc_scr = Permute.permute(est = [],
                                                                  test_group = sub_groups,
                                                                  n_permutations = n_permutations,
                                                                  shuffle_test = True,
                                                                  shuffle_estimate = False,
                                                                  threshold = threshold)

  # Plot permutation test results of pilot group
  Distributions.plot_multiple('Pilot permutation (PLV = '+str(threshold)+')',
                              elements=[[sens_scr, sens, 'Sensitivity'],
                                        [spec_scr, spec, 'Specificity'],
                                        [acc_scr, acc, 'Accuracy'],
                                        [npv_scr, npv, 'NPV'],
                                        [ppv_scr, ppv, 'PPV'] ] )

  print('OUTCOME FOR PILOT GROUP:')
  print('Survivors above     : ' + str(round(outcome[0][0],4)))
  print('Survivors below     : ' + str(round(outcome[0][1],4)))
  print('Non-survivors above : ' + str(round(outcome[1][0],4)))
  print('Non-survivors below : ' + str(round(outcome[1][1],4)))
  stat, p = Stat_PLV.permutation_significance(sens, sens_scr)
  print('Sensitivity         : ' + str(round(sens, 4)) + '(p = ' + str(round(p,5)) + ')')
  stat, p = Stat_PLV.permutation_significance(spec, spec_scr)
  print('Specificity         : ' + str(round(spec, 4)) + '(p = ' + str(round(p,5)) + ')')
  stat, p = Stat_PLV.permutation_significance(acc, acc_scr)
  print('Accuracy            : ' + str(round(acc, 4)) + '(p = ' + str(round(p,5)) + ')')
  stat, p = Stat_PLV.permutation_significance(ppv, ppv_scr)
  print('PPV                 : ' + str(round(ppv, 4)) + '(p = ' + str(round(p,5)) + ')')
  stat, p = Stat_PLV.permutation_significance(npv, npv_scr)
  print('NPV                 : ' + str(round(npv, 4)) + '(p = ' + str(round(p,5)) + ')')
