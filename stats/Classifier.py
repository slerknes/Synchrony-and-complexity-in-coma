import numpy as np
from stats import Stat_PLV



# Find the optimal thresholds to split two groups
def find_best_split(groups):
  
  smallest_minority_n         = None
  smallest_minority_threshold = []
  smallest_num_too_close      = None
  
  for _, val in enumerate(groups[0] + groups[1]):

    for _, threshold in enumerate([round(val,2)]):

      side_count = [[] for x in range(2)]

      for gr_i, gr in enumerate(groups):
        for _, val in enumerate(gr):
          if val > threshold: side_count[0].append(gr_i)
          if val < threshold: side_count[1].append(gr_i)
      
      _, _, _, _, _, accuracy = Stat_PLV.threshold_accuracy(groups, threshold)
      
      num_too_close = sum( [ 1 if round(val,2) == round(threshold,2) else 0
                             for val in groups[0] + groups[1]
                           ]
                         )
      
      if smallest_minority_n == None or accuracy > smallest_minority_n:
        smallest_minority_threshold = [round(threshold,2)]
        smallest_minority_n         = accuracy
        smallest_num_too_close      = num_too_close
        
      elif accuracy == smallest_minority_n and\
           num_too_close < smallest_num_too_close and\
           not round(threshold,2) in smallest_minority_threshold:
        smallest_minority_threshold = [round(threshold,2)]
        smallest_num_too_close      = num_too_close
        
      elif accuracy == smallest_minority_n and\
           num_too_close == smallest_num_too_close and\
           not round(threshold,2) in smallest_minority_threshold:
        smallest_minority_threshold.append(round(threshold,2))
        
  return smallest_minority_threshold



# Test the accuracy of a threshold
def test_threshold_accuracy(groups, threshold):
  
  classification  = [[] for x in range(len(groups))]
  group_accuracy  = [ 0 for x in range(len(groups))]
  side_accuracy   = [ 0 for x in range(2)]
  
  n_on_pred_side  = [ 0 for x in range(2)]
  n_on_side       = [ sum( [1 if np.round(x,2) > threshold else 0 for x in (groups[0] + groups[1])]), sum( [1 if np.round(x,2) < threshold else 0 for x in (groups[0] + groups[1])]) ]
  
  for gr_i, gr in enumerate(groups):

    classification[gr_i] = [ ( (1 if np.round(val,2) > threshold else 0) if gr_i == 0 else (1 if np.round(val,2) < threshold else 0) ) for val in gr] 
    group_accuracy[gr_i] = classification[gr_i].count(1) / len(classification[gr_i])
    
    n_on_pred_side[0] = n_on_pred_side[0] + sum([1 if gr_i == 0 and np.round(x,2) > threshold else 0 for x in gr])
    n_on_pred_side[1] = n_on_pred_side[1] + sum([1 if gr_i == 1 and np.round(x,2) < threshold else 0 for x in gr])

  both_sides_accuracy = (n_on_pred_side[0] + n_on_pred_side[1]) / (n_on_side[0] + n_on_side[1])
  side_accuracy = [ n_on_pred_side[0] / n_on_side[0] if not n_on_side[0] == 0 else 0, n_on_pred_side[1] / n_on_side[1] if not n_on_side[1] == 0 else 0, both_sides_accuracy ]

  return side_accuracy, group_accuracy, ((classification[0] + classification[1]).count(1) / len(classification[0] + classification[1])), classification