import numpy as np
import scipy.stats as stats

# Statistical test for difference between patient groups

def diff(groups):
  print('GROUP ONE: N = ' + str(len(groups[0])) + \
                 ', M = ' + str(round(np.average(groups[0]),3)) + \
                 ', SD = ' + str(round(np.std(groups[0]),3)))
  print('GROUP TWO: N = ' + str(len(groups[1])) + \
                 ', M = ' + str(round(np.average(groups[1]),3)) + \
                 ', SD = ' + str(round(np.std(groups[1]),3)))
  _, group_one_not_normal_p = stats.normaltest(groups[0])
  _, group_two_not_normal_p = stats.normaltest(groups[1])
  if group_one_not_normal_p or group_two_not_normal_p:
    U, p                    = stats.mannwhitneyu(groups[0], groups[1],
                                                alternative = 'two-sided')
    print('Non-normal distribution')
    print('           U('+ str(len(groups[0])) + ', ' + str(len(groups[1])) + ') = ' + str(int(round(U,5))) + ', p = ' + str(round(p,10)))
  else:
    t, p                    = stats.ttest_ind(groups[0], groups[1])
    print('           t = ' + str(round(t,5)) + \
                        ', p = ' + str(round(p,10)) + \
                        ', df = ' + str(len(groups[0]) + len(groups[1]) - 2))
