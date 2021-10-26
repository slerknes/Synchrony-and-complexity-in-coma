import numpy as np
import mne

def calc(data_path, ids, fmin, fmax, sfreq, n_eles):
    
  pat_data        = [{} for x in range(max(ids) + 1)]
  
  for p_id in ids:
    
    print('Calculating PLV for ID ' + str(p_id))  
        
    epochs_path     = data_path + str(p_id) + '-epo.fif'
          
    epochs          = mne.read_epochs(epochs_path, verbose=40, preload=True)
        
    epochs.set_eeg_reference('average')
          
    data            = epochs._data
    
    mode            = 'multitaper'
                     
    con, _, _, _, _ = mne.connectivity.spectral_connectivity(data     = data,
                                                             method   = 'plv',
                                                             sfreq    = sfreq,
                                                             mode     = mode,
                                                             faverage = True,
                                                             fmin     = fmin,
                                                             fmax     = fmax,
                                                             verbose  = 40)
    
    pat_data[p_id]['PLV'] = np.average(con.flatten())
    pat_data[p_id]['PLV_ch'] = con
    
    tmp_sum = []
    for ch_a in range(n_eles):
      for ch_b in range(ch_a):
        tmp_sum.append(con[ch_a][ch_b][0])
              
  return pat_data

def n_sig_conn(n_channels, p_vals_pairs, alpha):
  sig_conn_per_el = [[0] for el in range(n_channels)]

  for p_a_i, p_a in enumerate(p_vals_pairs):
    for p_b_i, p_b in enumerate(p_a):
      if p_b < alpha:
        sig_conn_per_el[p_a_i][0] += 1
        sig_conn_per_el[p_b_i][0] += 1
        
  return sig_conn_per_el