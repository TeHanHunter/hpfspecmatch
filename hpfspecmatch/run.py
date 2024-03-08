from importlib import reload
import os
import glob2
import pandas as pd
import numpy as np
import sys
import hpfspec
import hpfspecmatch, utils, config
from tqdm import trange


def run_hpfsm(targetname='TIC_39699837', filename=None, orders=['4', '5', '6', '14', '15', '16', '17']):
    utils.get_library()
    # List of stellar library fits files
    library_fitsfiles = config.LIBRARY_FITSFILES
    # Read in all files as a HPFSpecList object
    HLS = hpfspec.HPFSpecList(filelist=library_fitsfiles)
    df_lib = pd.read_csv(config.PATH_LIBRARY_DB)

    # outputdir = f'/home/tehan/Documents/SURFSUP/hpf/{targetname}/'
    outputdir = f'/home/tehan/Documents/GEMS/{targetname}/'
    os.mkdir(outputdir)
    hpfspecmatch.run_specmatch_for_orders(filename, targetname, outputdir, HLS=HLS, orders=orders)

    files = sorted(glob2.glob(f'{outputdir}*/*.pkl'))
    df_orders, df_orders_summary = hpfspecmatch.summarize_values_from_orders(files, targetname)

    return df_orders, df_orders_summary


if __name__ == '__main__':
    filenames = glob2.glob('/home/tehan/Documents/SURFSUP/hpf/spectra/Template_TIC_62560071_Fudge1.fits')
    # filenames = glob2.glob('/home/tehan/Documents/GEMS/TOI-5344/*.fits')
    ### Gummi comment: orders with less tellurics: 3, 18, 19, 26
    for i in trange(len(filenames)):
        target = 'TIC_' + os.path.basename(filenames[i]).split('_')[2]
        try:
            run_hpfsm(targetname=target, filename=filenames[i],
                      orders=['3', '4', '5', '6', '14', '15', '16', '18', '26'])
        except:
            continue