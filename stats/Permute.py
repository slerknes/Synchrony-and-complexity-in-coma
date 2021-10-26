# Permutation test on PLV classifier accuracy
# Includes methods for both pilot and validation groups, see comments below

import random
import numpy as np
from stats import Stat_PLV, Classifier

def permute(est_group = [], test_group = [], n_permutations = 100, shuffle_test = False, shuffle_estimate = False, threshold = None):

  ppv_scores            = np.zeros(n_permutations)
  npv_scores            = np.zeros(n_permutations)
  sensitivity_scores    = np.zeros(n_permutations)
  specificity_scores    = np.zeros(n_permutations)
  accuracy_scores       = np.zeros(n_permutations)
  
  for per_i in range(n_permutations):
    
    # Used on pilot group
    # Shuffles the pilot group values, and tests with previously found threshold
    if shuffle_test and not shuffle_estimate:
      
      shuffled_groups = test_group[0].copy() + test_group[1].copy()
      random.shuffle(shuffled_groups)
      
      _, ppv_scores[per_i], npv_scores[per_i], sensitivity_scores[per_i], specificity_scores[per_i], accuracy_scores[per_i] = Stat_PLV.threshold_accuracy([shuffled_groups[:len(test_group[0])], shuffled_groups[len(test_group[0]):]], threshold)
    
    # Used on validation group
    # Shuffles the pilot group values, and finds new possible threshold.
    # Tests the new threshold on the validation group
    elif shuffle_estimate and not shuffle_test:
            
      shuffled_groups = est_group[0].copy() + est_group[0].copy()
      random.shuffle(shuffled_groups)
      possible_thresholds = Classifier.find_best_split([shuffled_groups[:len(est_group[0])], shuffled_groups[len(est_group[0]):]])
  
      # Select one at random of the possible thresholds
      random_threshold_index  = random.randint(0, len(possible_thresholds) - 1)
      threshold               = possible_thresholds[random_threshold_index]

      _, ppv_scores[per_i], npv_scores[per_i], sensitivity_scores[per_i], specificity_scores[per_i], accuracy_scores[per_i] = Stat_PLV.threshold_accuracy([test_group[0], test_group[1]], threshold)

  return ppv_scores, npv_scores, sensitivity_scores, specificity_scores, accuracy_scores