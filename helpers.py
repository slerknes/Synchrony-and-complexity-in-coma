# Split groups into test and estimate
# vals : The data
# para : Which data key to use
# ids  : Which IDs to use
# split: At what ID to split
# d:   : To return above (+) or below/at (-) the split ID
def split_groups(vals, para, ids, split = 0, d = False):
  if d == '-':
    return [vals[p_id][para] for p_id in
            [*filter(lambda x: x <= split, ids)]
            ]
  elif d == '+':
    return [vals[p_id][para] for p_id in
            [*filter(lambda x: x > split, ids)]
            ]
  else:
    return [vals[p_id][para] for p_id in ids]
    
