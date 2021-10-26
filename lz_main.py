# Illustrative code to make use of the methods used in the LZ calculation

# Calculating LZ with specified normalization approach, and testing for diff.

from calc import Calc_LZ
from stats import Group, Chans
from plot import Spread
from helpers import split_groups

data_path       = ''

survivors       = [ ] # List of IDs associated with recordings
non_survivors   = [ ] # List of IDs associated with recordings
patients        = survivors + non_survivors

ch_names        = [ ] # Channel names

split           = # Int: ID for where to make split between pilot and test
alpha           = # Float: To compare electrodes in pilot-group on outcome
norm_technique  = # String: time, phase, time-phase, or time-phase-norm
concatenate     = # Boolean: Concatenate epochs or calculate LZ on epochs
n_permutations  = # Int: Number of permutations

# Calculate LZ values
lz_pats         = Calc_LZ.calc(data_path, ids = patients,
                               n_perm = n_permutations,
                               norm_technique = norm_technique,
                               concatenate = concatenate)

# Split the groups into separate lists. Patient-average across electrodes
surv            = split_groups(lz_pats, 'LZ', survivors)
nsrv            = split_groups(lz_pats, 'LZ', non_survivors)

# Print group statistics
print('\nSurvivors v. non-survivors')
Group.diff([surv, nsrv])

# Identify channels that differ significantly between pilot group outcomes
sig_chs, p_vals = Chans.difference(split_groups(lz_pats, 'LZ_ch',
                                                survivors, split, '-'),
                                   split_groups(lz_pats, 'LZ_ch',
                                                non_survivors, split, '-'),
                                   ch_names,
                                   alpha=alpha)

print('Number of significant electrodes: ' + str(len(sig_chs)))

# Plot LZ complexity
Spread.plot('', 'Lempel-Ziv Complexity',
            [surv, nsrv],
            group_name = ['Survivor', 'Non-survivor'],
            colors = ['#1b9e77', '#d95f02'], save=False)