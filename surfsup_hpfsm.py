import hpfspec
import hpfspecmatch
import os
from glob import glob
from astropy.io import fits
import pickle
import csv

def process_fits_spectra(
    input_folder,
    output_folder,
    orders=None,
    maxvsini=250,
    calibrate_feh=True,
    scaleres=1.0,
    verbose=True
):
    """
    Process all FITS spectra in input_folder using hpfspecmatch.
    """
    if orders is None:
        orders = [str(i) for i in [4, 5, 6, 14, 15, 16, 17]]

    # Make sure the library is available
    hpfspecmatch.get_library()
    path_df_lib = hpfspecmatch.config.PATH_LIBRARY_DB

    # Find all FITS files
    fits_files = sorted(glob(os.path.join(input_folder, "*.fits")))

    if verbose:
        print(f"Found {len(fits_files)} FITS files.")

    for filepath in fits_files:
        filename = os.path.basename(filepath)
        try:
            with fits.open(filepath) as hdul:
                targetname = hdul[0].header.get('OBJECT', 'Unknown')

            if verbose:
                print(f"\nProcessing {filename} (Target: {targetname})...")

            # Run specmatch
            hpfspecmatch.run_specmatch_for_orders(
                targetfile=filepath,
                targetname=targetname,
                outputdirectory=os.path.join(
                    output_folder,
                    os.path.basename(filepath).split(".")[0]
                ),
                path_df_lib=path_df_lib,
                orders=orders,
                maxvsini=maxvsini,
                calibrate_feh=calibrate_feh,
                scaleres=scaleres
            )
        except Exception as e:
            if verbose:
                print(f"Error processing {filename}: {e}")
            continue

def gather_pickle_results(
        base_dir,
        output_csv="results_summary.csv",
        slope_prefix="Slope",
        verbose=True
):
    """
    Traverse the given directory, extract .pkl results, and save them to a CSV.

    Each row = one Slope folder.
    Each column = teff/logg/feh/vsini per order.
    """
    rows = []
    all_orders = set()

    # First pass: collect all unique order numbers
    for slope_folder in sorted(os.listdir(base_dir)):
        slope_path = os.path.join(base_dir, slope_folder)
        if not os.path.isdir(slope_path) or not slope_folder.startswith(slope_prefix):
            continue
        for subfolder in sorted(os.listdir(slope_path)):
            subfolder_path = os.path.join(slope_path, subfolder)
            if os.path.isdir(subfolder_path) and "_" in subfolder:
                order = subfolder.split("_")[-1]
                all_orders.add(order)

    all_orders = sorted(all_orders, key=lambda x: int(x) if x.isdigit() else x)

    # Build headers
    headers = ["Folder", "TIC"]
    for order in all_orders:
        headers += [f"teff_{order}", f"logg_{order}", f"feh_{order}", f"vsini_{order}"]

    # Second pass: extract data
    for slope_folder in sorted(os.listdir(base_dir)):
        slope_path = os.path.join(base_dir, slope_folder)
        if not os.path.isdir(slope_path) or not slope_folder.startswith(slope_prefix):
            continue

        row_data = {"Folder": slope_folder, "TIC": ""}
        for order in all_orders:
            row_data[f"teff_{order}"] = ""
            row_data[f"logg_{order}"] = ""
            row_data[f"feh_{order}"] = ""
            row_data[f"vsini_{order}"] = ""

        any_subfolder_found = False

        for subfolder in sorted(os.listdir(slope_path)):
            subfolder_path = os.path.join(slope_path, subfolder)
            if os.path.isdir(subfolder_path) and "_" in subfolder:
                any_subfolder_found = True
                parts = subfolder.split("_")
                if len(parts) >= 2:
                    tic_name = "_".join(parts[:-1])
                    if not row_data["TIC"]:
                        row_data["TIC"] = tic_name
                    order = parts[-1]
                    # Correct prefix
                    pkl_prefix = "_".join(parts[:-1])
                    pkl_file = os.path.join(subfolder_path, f"{pkl_prefix}_results.pkl")
                    if os.path.exists(pkl_file):
                        try:
                            with open(pkl_file, "rb") as f:
                                data = pickle.load(f)
                            row_data[f"teff_{order}"] = data.get("teff", "")
                            row_data[f"logg_{order}"] = data.get("logg", "")
                            row_data[f"feh_{order}"] = data.get("feh", "")
                            row_data[f"vsini_{order}"] = data.get("vsini", "")
                            if verbose:
                                print(f"Loaded: {pkl_file}")
                        except Exception as e:
                            if verbose:
                                print(f"Error reading {pkl_file}: {e}")

        # If no subfolders, still keep the row
        rows.append([row_data.get(col, "") for col in headers])

    # Write CSV
    with open(base_dir+output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)

    if verbose:
        print(f"\nDone! Results saved to {base_dir+output_csv}")



if __name__ == '__main__':
    input_folder = "/home/tehan/Documents/SURFSUP/hpf/transfer/"  # folder containing spectra
    output_folder = "/home/tehan/Documents/SURFSUP/hpf/hpfsm/"
    process_fits_spectra(
        input_folder,
        output_folder,
        orders=None,
        maxvsini=250,
        calibrate_feh=True,
        scaleres=1.0,
        verbose=True
    )

    gather_pickle_results(output_folder)
