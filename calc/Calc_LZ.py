import numpy as np
import mne
from scipy.signal import hilbert
from scipy.fft import fft, ifft
import random



# Generate a phased shuffled version of the signal
def rand_phase(signal):
  spectrum            = fft(signal)
  magnitude           = np.abs(spectrum)
  phase               = np.unwrap(np.angle(spectrum))

  # Shuffle the phase
  phase_lh            = phase.copy()[1:int(len(phase)/2)]
  np.random.shuffle(phase_lh)
  phase_rh            = -phase_lh[::-1]
  rand_phase          = np.append(phase[0],
                                  np.append(phase_lh,
                                            np.append(phase[int(len(phase)/2)],
                                                      phase_rh)))

  # Generate new signal with random phase
  shuf_phase_spectrum = magnitude * np.exp( 1j * rand_phase )
  shuf_phase_signal   = ifft(shuf_phase_spectrum).real
  
  return shuf_phase_signal



def binarize(signal):
  signal = abs(hilbert(signal))
  ch_mean = np.median(signal)
  s = ''
  for x in signal:
    if x < ch_mean:
      s += '0'
    else:
      s += '1'
  return s



def time_shuffling(binary_signal):
  random_signal = ''.join(random.sample(binary_signal,len(binary_signal)))
  return random_signal



# Source for this implementation:
# https://github.com/Naereen/Lempel-Ziv_Complexity/tree/master/

def lz_complexity(sequence):
  sub_strings = set()
  ind = 0
  inc = 1
  while True:
    if ind + inc > len(sequence):
      break
    sub_str = sequence[ind : ind + inc]
    if sub_str in sub_strings:
      inc += 1
    else:
      sub_strings.add(sub_str)
      ind += inc
      inc = 1
  return len(sub_strings)



def calc(data_path, ids, n_perm, norm_technique='time', concatenate = False):

  result        = [ {} for x in range(np.amax(ids) + 1) ]
  
  print('Calculating LZ complexity. This may take a while ... \n')
  
  for p_id in ids:
    
    print('Calculating LZ for patient ' + str(p_id))
    
    epochs_path     = data_path + str(p_id) + '-epo.fif'
          
    epochs          = mne.read_epochs(epochs_path, verbose=40, preload=True)
        
    epochs.set_eeg_reference('average')
          
    data            = epochs._data
    
    # Concatenate data to one continuous epoch
    if concatenate:
      c = [ [] for i in range(len(data[0])) ]
      for epo_i, epo_e in enumerate(data):
        for ch_i, ch_e in enumerate(epo_e):
          c[ch_i].extend(ch_e)
      data = np.array([c])
      
    ch_lz       = [ 0 for i in range(data.shape[1]) ]
    orig_ch_lz  = [ [ 0 for a in range(data.shape[0]) ] for i in range(data.shape[1]) ]
    ch_ep_time  = [ [ 0 for a in range(data.shape[0]) ] for i in range(data.shape[1]) ]
    ch_ep_phase = [ [ 0 for a in range(data.shape[0]) ] for i in range(data.shape[1]) ]
    
    for ch_idx in range(data.shape[1]):
      
      ep_lz    = [ 0 for a in range(data.shape[0]) ]
      
      for ep_idx in range(data.shape[0]):
        
        # Get signal for one channel, for one epoch
        signal = data[ep_idx, ch_idx]
        
        # Make binary representation of the signal
        binary = binarize(signal)
        
        # Calculate the original, "raw", LZ comlpexity
        lz_orig = lz_complexity( binary )
        orig_ch_lz[ch_idx][ep_idx] = lz_orig
        
        
        
        # Calculate LZ with permuted time dimension of binary representation
        if norm_technique in [ 'time', 'time-phase', 'time-phase-norm' ]:
          
          binary_permutations = np.zeros((n_perm))
          
          for perm_i in range(n_perm):
            
              time_shuffled = time_shuffling(binary)
              binary_permutations[perm_i] = lz_complexity( time_shuffled )
              
          time_rand_avg = np.average(binary_permutations)
          
          ch_ep_time[ch_idx][ep_idx] = time_rand_avg
              
              
              
        # Calculate the phase-permuted LZ complexity
        if norm_technique in [ 'phase', 'time-phase' ]:
          
          phase_permutations = np.zeros((n_perm))
          
          for perm_i in range(n_perm):
            
            phase_shuffled = rand_phase(signal)
            binary_phase_shuffled = binarize( phase_shuffled )
            phase_permutations[perm_i] = lz_complexity( binary_phase_shuffled )
            
          phase_rand_avg = np.average(phase_permutations)
          
          ch_ep_phase[ch_idx][ep_idx] = phase_rand_avg
          
          
          
        # Calculate the time-normalized phase-permuted LZ complexity
        if norm_technique in [ 'time-phase-norm' ]:
          
          phase_permutations = np.zeros((n_perm))
          
          for phase_perm_i in range(n_perm):
            
            phase_shuffled = rand_phase(signal)
            binary_phase_shuffled = binarize( phase_shuffled )
            
            binary_permutations = np.zeros((n_perm))
            
            for time_perm_i in range(n_perm):
              
              time_shuffled = time_shuffling(binary_phase_shuffled)
              binary_permutations[time_perm_i] = lz_complexity( time_shuffled )
            
            phase_permutations[phase_perm_i] = lz_complexity( binary_phase_shuffled ) / np.average(binary_permutations)
            
          phase_rand_avg = np.average(phase_permutations)
          
          ch_ep_phase[ch_idx][ep_idx] = phase_rand_avg
        
        if norm_technique == 'time':
          norm = lz_orig / time_rand_avg
        elif norm_technique == 'phase':
          norm = lz_orig / phase_rand_avg
        elif norm_technique == 'time-phase':
          norm = ( lz_orig / time_rand_avg ) / phase_rand_avg
        elif norm_technique == 'time-phase-norm':
          norm = ( lz_orig / time_rand_avg ) / phase_rand_avg
        elif norm_technique in [ 'len' ]:
          norm = lz_orig / len(binary)
        
        ep_lz[ep_idx] = norm
        
      ch_lz[ch_idx] = np.average(ep_lz)
        
    result[p_id]['LZ'] = np.average(ch_lz)
    result[p_id]['LZ_ch'] = ch_lz
    result[p_id]['orig_LZ'] = orig_ch_lz
    result[p_id]['time_LZ'] = ch_ep_time
    result[p_id]['phase_LZ'] = ch_ep_phase
    
  return result