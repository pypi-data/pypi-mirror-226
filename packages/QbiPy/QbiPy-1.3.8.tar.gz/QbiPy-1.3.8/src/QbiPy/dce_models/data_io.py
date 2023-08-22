'''
Utility functions for reading and writing DCE-MRI dynamic series images and meta data
'''

import numpy as np

from QbiPy.image_io.analyze_format import read_analyze
from QbiPy.image_io.xtr_files import read_xtr_file
#-----------------------------------------------------------------------------------
def get_dyn_vals(root_path, num_vols, roi, index_fmt = '01d', ext = '.hdr'):
    '''GET_DYN_VALS given directory of volumes and ROI mask, get array of
    time-series for voxels in the ROI
    [times] = get_dyn_vals(root_path, num_vols, roi, index_fmt)

    Parameters:
        root_path : str
            folder + filename root where volumes are, or 4D array of loaded volumes

        num_vols : int
            number of volumes to load

        roi : str or np.array
            mask volume. if string, path to ROIvolume. If np.array, 
            must have same dims as dynamic volumes

        index_fmt : str = '01d'
            format that converts indexes into volume suffix

        ext : str = '.hdr
            extension of image volumes

    Returns:
        dyn_signals - N_vox x N_times array of time-series for each voxel
      '''

    #If ROI is a path, load it from disk
    if type(roi) == str:
        roi = read_analyze(roi)[0] > 0


    num_pts = np.count_nonzero(roi)
    dyn_signals = np.empty((num_pts, num_vols))

    load_vols = type(root_path) == str
    for i_vol in range(num_vols):
        if load_vols:
            vol_path = f"{root_path}{i_vol+1:{index_fmt}}{ext}"
            vol = read_analyze(vol_path)[0]
        else:
            vol = root_path[:,:,:,i_vol]
        
        dyn_signals[:,i_vol] = vol[roi]

    return dyn_signals

#-----------------------------------------------------------------------------------
def get_dyn_vols(root_path, num_vols, index_fmt = '01d', ext = '.hdr'):
    '''
    Load series of image volumes
    [times] = get_dyn_times(root_path, index_fmt, num_vols)

    Parameters:
        root_path : str
            folder + filename root where volumes are, or 4D array of loaded volumes

        num_vols : int
            number of volumes to load

        index_fmt : str = '01d'
            format that converts indexes into volume suffix

        ext : str = '.hdr
            extension of image volumes

    Returns:
        dyn_vols - (Ny, Nx, Nz, Nvols) array containing each dynamic volume

        dyn_headers - header information for each volume'''
    dyn_headers = []
    dyn_vols = []
    for i_vol in range(num_vols):
        
        vol_path = f"{root_path}{i_vol+1:{index_fmt}}{ext}"
        d, d_hdr = read_analyze(vol_path)
        
        
        if i_vol == 0:
            [n_y, n_x, n_z] = d.shape
            dyn_vols = np.empty((n_y, n_x, n_z, num_vols))
        
        dyn_vols[:,:,:,i_vol] = d
        dyn_headers.append(d_hdr)
    
    return dyn_vols, dyn_headers

#-----------------------------------------------------------------------------------
def get_dyn_xtr_data(root_path, num_vols, index_fmt = '01d'):
    '''get meta information (scan time, FA, TR) from xtr files for 
    folder of dynamic volumes
    [times] = get_dyn_times(root_path, index_fmt, num_vols)

    Parameters:
        root_path - folder + filename root where volumes are

        num_vols - number of volumes to load

        index_fmt ('01d') - format that converts indexes into volume suffix


    Returns:
        dyn_times - 1D array containing the acquisition time of each dynamic volume

        dyn_TR - repetition time of dynamic volumes in ms. Given as 1D array although all should be the same

        dyn_FA - flip-angle of dynamic volumes in degrees. Given as 1D array although all should be the same

        dyn_noise - estimate of temporally varying noise on each dynamic volume
        
    '''
    #Pre-allocate arrays
    dyn_times = np.zeros(num_vols)
    dyn_TR = np.zeros(num_vols)
    dyn_FA = np.zeros(num_vols)
    dyn_noise = np.zeros(num_vols)

    #Load each xtr file and extract data
    for i_vol in range(num_vols):
        vol_path = f"{root_path}{i_vol+1:{index_fmt}}.xtr"
        xtr_data = read_xtr_file(vol_path)
        if 'TimeStamp' in xtr_data:
            dyn_times[i_vol] = xtr_data['TimeStamp']
        if 'TR' in xtr_data:
            dyn_TR[i_vol] = xtr_data['TR']
        if 'FlipAngle' in xtr_data:
            dyn_FA[i_vol] = xtr_data['FlipAngle']
        if 'NoiseSigma' in xtr_data:
            dyn_noise[i_vol] = xtr_data['NoiseSigma']

    return dyn_times, dyn_TR, dyn_FA, dyn_noise
