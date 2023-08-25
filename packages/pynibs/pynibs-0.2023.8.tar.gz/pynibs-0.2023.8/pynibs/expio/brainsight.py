""" Functions to import data from Rogue Research Brainsight neuronavigation systems """
from collections import OrderedDict
import pandas as pd
import numpy as np
import datetime
import pynibs
import h5py
import io
import os


class BrainsightCSVParser:
    """
    Parser for Brainsight CSV files.

    Attributes
    ----------
    current_state : BrainsightCSVParser.State
        The current state of the parser.
    header_file : str
        The file header.
    header_data : list of str
        The header data.
    data : list of list of str
        The parsed data rows.

    Methods
    -------
    check_state_transition(line)
        Checks the state transition based on the given line.
    parse_line(line)
        Parses a line and updates the corresponding attributes.
    """
    class State:
        FILE_HEADER = 0
        SKIPPING = 1
        DATA_HEADER = 2
        DATA = 3
        FIN = 4

    def __init__(self):
        """
        Initialize the BrainsightCSVParser object.
        """
        self.current_state = BrainsightCSVParser.State.FILE_HEADER
        self.header_file = ""
        self.header_data = []
        self.data = []

    def check_state_transition(self, line):
        """
        Checks the state transition based on the given line.

        Parameters
        ----------
        line : str
            The line to check.
        """
        new_state = BrainsightCSVParser.State.SKIPPING
        if line.startswith("# Sample Name"):  # data header info
            new_state = BrainsightCSVParser.State.DATA_HEADER
        elif line.startswith("Sample "):
            new_state = BrainsightCSVParser.State.DATA
        elif line.startswith("# Target Name"):
            new_state = BrainsightCSVParser.State.SKIPPING
        elif line.startswith("# "):
            # we are still parsing the file header
            if self.current_state == BrainsightCSVParser.State.FILE_HEADER:
                new_state = BrainsightCSVParser.State.FILE_HEADER
            # if we surpassed the 'FILE_HEADER' state already, a line with
            # a leading '#' is a comment, which should be skipped
            else:
                new_state = BrainsightCSVParser.State.SKIPPING
        # all other lines should be skipped

        self.current_state = new_state

    def parse_line(self, line):
        """
        Parses a line and updates the corresponding attributes.

        Parameters
        ----------
        line : str
            The line to parse.
        """
        if self.current_state == BrainsightCSVParser.State.FILE_HEADER:
            self.header_file += line
        elif self.current_state == BrainsightCSVParser.State.DATA_HEADER:
            line = line[2:-1]  # strip leading comment character '# ' and trailing newline '\n'
            self.header_data = line.split('\t')
        elif self.current_state == BrainsightCSVParser.State.DATA:
            line = line[:-1]  # strip trailing newline '\n'
            data_row = line.split('\t')
            self.data.append(data_row)


def write_targets_brainsight(targets, fn_out, names=None, overwrite=True):
    """
    Writes coil position and orientations in .txt file for import into Brainsight.

    Parameters
    ----------
    targets : np.ndarray of float
    (4, 4, N_targets), Tensor containing the 4x4 matrices with coil orientation and position.
    fn_out : str
        Filename of output file.
    names : list of str, optional
        Target names (if None they will be numbered by their order).
    overwrite : bool, default: True
        Overwrite existing .txt file.

    Returns
    -------
    <file> .txt file containing the targets for import into Brainsight
    """

    targets = np.atleast_3d(targets)

    if names is None:
        names = [f"{i:04}" for i in range(targets.shape[2])]
    if isinstance(names, str):
        names = [names]
    assert targets.shape[:2] == (4, 4), 'Expecting array with shape (4, 4, N instrument marker).'

    if not fn_out.lower().endswith('.txt'):
        fn_out += '.txt'

    assert not os.path.exists(fn_out) or overwrite, '.txt file already exists. Remove or set overwrite=True.'

    with io.open(fn_out, 'w', newline='\n') as f:  # correct windows style would be \r\n, but Localite uses \n
        f.write('# Version: 12\n')
        f.write('# Coordinate system: NIfTI:Aligned\n')
        f.write('# Created by: pynibs\n')
        f.write('# Units: millimetres, degrees, milliseconds, and microvolts\n')
        f.write('# Encoding: UTF-8\n')
        f.write('# Notes: Each column is delimited by a tab. Each value within a column is delimited by a semicolon.\n')
        f.write(
            '# Target Name	Loc. X	Loc. Y	Loc. Z	m0n0	m0n1	m0n2	m1n0	m1n1	m1n2	m2n0	m2n1	m2n2\n')

        for i_t in range(targets.shape[2]):
            f.write(f'{names[i_t]}\t' +
                    f'{targets[0, 3, i_t]:.4f}\t{targets[1, 3, i_t]:.4f}\t{targets[2, 3, i_t]:.4f}\t' +
                    f'{targets[0, 0, i_t]:.4f}\t{targets[1, 0, i_t]:.4f}\t{targets[2, 0, i_t]:.4f}\t' +
                    f'{targets[0, 1, i_t]:.4f}\t{targets[1, 1, i_t]:.4f}\t{targets[2, 1, i_t]:.4f}\t' +
                    f'{targets[0, 2, i_t]:.4f}\t{targets[1, 2, i_t]:.4f}\t{targets[2, 2, i_t]:.4f}\n')


def read_targets_brainsight(fn):
    """
    Reads target coil position and orientations from .txt file and returns it as 4 x 4 x N_targets numpy array.

    Parameters
    ----------
    fn : str
        Filename of output file.

    Returns
    -------
    m_nnav : np.ndarray of float
        (4, 4, N_targets) Tensor containing the 4x4 matrices with coil orientation and position.
    """
    with io.open(fn, 'r') as f:
        lines = f.readlines()
    start_idx = [i + 1 for i, l in enumerate(lines) if l.startswith("# Target")][0]
    stop_idx = [i for i, l in enumerate(lines) if l.startswith("# Sample Name") or l.startswith("# Session Name")]

    if not stop_idx:
        stop_idx = len(lines)
    else:
        stop_idx = np.min(stop_idx)

    n_targets = stop_idx - start_idx
    names = ['' for _ in range(n_targets)]
    m_nnav = np.zeros((4, 4, n_targets))
    for i_loc, i_glo in enumerate(range(start_idx, stop_idx)):
        line = lines[i_glo].split(sep='\t')
        names[i_loc] = line[0]
        m_nnav[:3, 0, i_loc] = np.array(line[4:7]).astype(float)
        m_nnav[:3, 1, i_loc] = np.array(line[7:10]).astype(float)
        m_nnav[:3, 2, i_loc] = np.array(line[10:13]).astype(float)
        m_nnav[:3, 3, i_loc] = np.array(line[1:4]).astype(float)
        m_nnav[3, 3, i_loc] = 1
    return m_nnav


def create_merged_nnav_emg_file_brainsight(fn_brainsight_nnav_info, fn_emg_info, fn_out, p2p_window_start=18,
                                           p2p_window_end=35):
    """
    Creates a merged file containing TMS coil positions and EMG data from Brainsight information.

    Parameters
    ----------
    fn_brainsight_nnav_info : str
        File path of the Brainsight nnav coil information.
    fn_emg_info : str
        File path of the EMG information.
    fn_out : str
        File path of the output merged file.
    p2p_window_start : int, default: 18
        Start of the time frame after TMS pulse where p2p value is evaluated (in ms).
    p2p_window_end : int, default: 35
        End of the time frame after TMS pulse where p2p value is evaluated (in ms).
    """
    # read EMG information
    _, ext = os.path.splitext(fn_emg_info)

    if ext == ".mat":
        with h5py.File(fn_emg_info, 'r') as data_h5:
            keys = list(data_h5.keys())
            keys = [k for k in keys if k != '#refs#']

            if len(keys) != 1:
                raise ValueError(f"Key ambiguity! Please provide only exactly one data field in file: {fn_emg_info}")

            emg_data = data_h5[f"/{keys[0]}/values"][:]
            emg_start = data_h5[f"/{keys[0]}/start"][0][0]
            emg_res = data_h5[f"/{keys[0]}/interval"][0][0]

            if emg_res < .1:  # time step between samples might be stored in seconds
                emg_res *= 1e3

            num_stim = emg_data.shape[0]
            num_channels = emg_data.shape[1]
            num_emg_samples = emg_data.shape[2]

            emg_timestamps_h5_ref = data_h5[f"/{keys[0]}/frameinfo/start"][:]
            emg_timestamps = []
            for stim_idx in range(num_stim):
                emg_timestamps.append(data_h5[emg_timestamps_h5_ref[0][stim_idx]][0][0])
            emg_timestamps = np.asarray(emg_timestamps, dtype=np.float32)
            emg_timestamps -= emg_timestamps[0]
    elif ext == ".cfs":
        emg_data, emg_timestamps, num_stim, num_channels, num_emg_samples, sampling_rate = \
            pynibs.read_biosig_emg_data(fn_data=fn_emg_info, include_first_trigger=True, type="cfs")
        emg_res = 1000 / sampling_rate  # [ms]
        emg_start = 0  # EMG start time not included in CSF file / always 0 for CED Signal (?)
    else:
        print(f"[Error] create_merged_nnav_emg_file_brainsight: unsupported EMG data file extension: {ext}"
              "Only CED Signal files (*.cfs) or MATLAB v.7.3 files are supported."
              "Does the file you specified have a file extension at all?")
        return 1

    # read nnav coil information
    with open(fn_brainsight_nnav_info, 'r') as data_txt_f:
        csv_parser = BrainsightCSVParser()
        while True:
            line = data_txt_f.readline()
            if not line:
                break
            csv_parser.check_state_transition(line)
            csv_parser.parse_line(line)

        nnav_timestamps = []
        start_time_string = current_time_string = csv_parser.data[0][24]  # 25. column of CSv data = time stamp
        start_time = datetime.datetime.strptime(start_time_string, '%H:%M:%S.%f')
        for c_idx in range(0, num_stim):
            current_time_string = csv_parser.data[c_idx][24]  # 25. column of CSv data = time stamp
            current_time = datetime.datetime.strptime(current_time_string, '%H:%M:%S.%f')
            nnav_timestamps.append((current_time - start_time).total_seconds())

        nnav_timestamps = np.asarray(nnav_timestamps, dtype=np.float32)

    # verify timesteps
    timestamp_difference = np.abs(nnav_timestamps - emg_timestamps)
    if np.any(timestamp_difference > 1):
        print("[ WARNING ] Detected time stamp differences larger than 1 second. "
              "Please check whether data from the neuronavigation are aligned with the EMG data.")

    # append EMG info to the nnav coil info
    # 1) header
    header_out = csv_parser.header_data.copy()
    header_out.append("EMG Start")
    header_out.append("EMG End")
    header_out.append("EMG Res.")
    header_out.append("EMG Channels")
    header_out.append("EMG Window Start")
    header_out.append("EMG Window End")
    for c_idx in range(num_channels):
        header_out.append(f"EMG Peak-to-peak {c_idx + 1}")
        header_out.append(f"EMG Data {c_idx + 1}")

    # 2) data
    data_text_out = []
    for stim_idx in range(len(emg_data)):
        # take what we already have in the nnav data
        row = csv_parser.data[stim_idx].copy()
        # extend it by the EMG data
        row.extend([str(emg_start),  # EMG Start
                    "(null)",  # EMG End
                    str(emg_res),  # EMG Res.
                    str(num_channels),  # EMG Channels
                    str(p2p_window_start),  # EMG Window Start
                    str(p2p_window_end)])  # EMG Window End
        for c_idx in range(num_channels):
            row.append("0")  # EMG Peak-to-peak c_idx+1
            emg_data_list = emg_data[stim_idx, c_idx, :].tolist()
            row.append(  # EMG data
                    ';'.join(map(str, emg_data_list))
            )
        data_text_out.append('\t'.join(row))

    with open(fn_out, 'w') as outfile:
        outfile.write(csv_parser.header_file)
        outfile.write("# " + '\t'.join(header_out))
        outfile.write('\n')
        outfile.write('\n'.join(data_text_out))
        outfile.write('\n')
        outfile.write("# Session Name: END")


def merge_exp_data_brainsight(subject, exp_idx, mesh_idx, coil_outlier_corr_cond=False,
                              remove_coil_skin_distance_outlier=True, coil_distance_corr=True,
                              average_emg_data_from_same_condition=False, verbose=False, plot=False,
                              start_mep=18, end_mep=35):
    """
    Merge the TMS coil positions and the mep data into an experiment.hdf5 file.

    Parameters
    ----------
    subject : pynibs.Subject
        Subject object.
    exp_idx : str
        Experiment ID.
    mesh_idx : str
        Mesh ID.
    coil_outlier_corr_cond : bool, default: False
        Correct outlier of coil position and orientation (+-2 mm, +-3 deg) in case of conditions.
    remove_coil_skin_distance_outlier : bool, default: True
        Remove outlier of coil position lying too far away from the skin surface (+- 5 mm).
    coil_distance_corr : bool, default: True
        Perform coil <-> head distance correction (coil is moved towards head surface until coil touches scalp).
    average_emg_data_from_same_condition : bool, default: False
        Flag indicating whether to average EMG data from the same condition. Only meaningful in conjunction with
        'coil_distance_correction', which averages the coil position within a condition.
    verbose : bool, default: False
        Plot output messages.
    plot : bool, default: False
        Plot MEPs and p2p evaluation.
    start_mep : float, default: 18
        Start of time frame after TMS pulse where p2p value is evaluated (in ms).
    end_mep : float, default: 35
        End of time frame after TMS pulse where p2p value is evaluated (in ms).
    """

    nii_exp_path_lst = subject.exp[exp_idx]['fn_mri_nii']
    # nii_conform_path = os.path.join(os.path.split(subject.mesh[mesh_idx]["fn_mesh_hdf5"])[0],
    #                                subject.id + "_T1fs_conform.nii.gz")
    nii_conform_path = subject.exp[exp_idx]["fn_mri_nii"][0][0]
    fn_exp_hdf5 = subject.exp[exp_idx]['fn_exp_hdf5'][0]
    fn_coil = subject.exp[exp_idx]['fn_coil'][0][0]
    fn_mesh_hdf5 = subject.mesh[mesh_idx]['fn_mesh_hdf5']
    temp_dir = os.path.join(os.path.split(subject.exp[exp_idx]['fn_exp_hdf5'][0])[0],
                            "nnav2simnibs",
                            f"mesh_{mesh_idx}")
    fn_data = None
    if "fn_data" in subject.exp[exp_idx].keys():
        if isinstance(subject.exp[exp_idx]["fn_data"], list):
            if isinstance(subject.exp[exp_idx]["fn_data"][0], str):
                fn_data = subject.exp[exp_idx]["fn_data"][0]
            else:
                fn_data = subject.exp[exp_idx]["fn_data"][0][0]
        elif isinstance(subject.exp[exp_idx]["fn_data"], str):
            fn_data = subject.exp[exp_idx]["fn_data"]
        else:
            print("[Error] Invalid exp[*]['fn_data']: "
                  "either specify the path as a single string or as a nested list of strings [['path']]!"
                  "Will attempt to read EMG data from exp[*]['fn_tms_nav']")
    else:
        print("[Warn] No EMG data specified in exp[*]['fn_data']: Will read EMG data from exp[*]['fn_tms_nav']")

    if "fn_tms_nav" in subject.exp[exp_idx]:
        if isinstance(subject.exp[exp_idx]["fn_tms_nav"], list):
            if isinstance(subject.exp[exp_idx]["fn_tms_nav"][0], str):
                fn_tms_nav = subject.exp[exp_idx]["fn_tms_nav"][0]
            else:
                fn_tms_nav = subject.exp[exp_idx]["fn_tms_nav"][0][0]
        elif isinstance(subject.exp[exp_idx]["fn_tms_nav"], str):
            fn_tms_nav = subject.exp[exp_idx]["fn_tms_nav"][0][0]
        else:
            raise ValueError("Invalid exp[*]['fn_tms_nav']: "
                             "Either specify the path as a single string or as a nested list of strings [['path']]!")
    else:
        raise KeyError("No exp[*]['fn_tms_nav'] found in subject object. Cannot continue to merge data,")

    if fn_data is not None:
        fn_out, out_ext = os.path.splitext(fn_tms_nav)
        fn_out += "_merged" + out_ext

        if not os.path.exists(fn_out):
            create_merged_nnav_emg_file_brainsight(
                    fn_brainsight_nnav_info=fn_tms_nav,
                    fn_emg_info=fn_data,
                    fn_out=fn_out
            )

        fn_tms_nav = fn_out

    # read Brainsight data
    ######################
    if verbose:
        print(f"Reading Brainsight data from file: {fn_tms_nav}")

    d_bs = OrderedDict()

    with io.open(fn_tms_nav, 'r') as f:
        lines = f.readlines()

    start_idx = [i + 1 for i, l in enumerate(lines) if l.startswith("# Sample Name")][0]
    stop_idx = [i for i, l in enumerate(lines) if l.startswith("# Session Name")]

    if not stop_idx:
        stop_idx = len(lines)
    else:
        stop_idx = np.min(stop_idx)

    n_stims = stop_idx - start_idx
    m_nnav = np.zeros((4, 4, n_stims))

    keys = lines[start_idx - 1].split('\t')
    keys[0] = keys[0].replace('# ', '')
    keys[-1] = keys[-1].replace('\n', '')

    # create brainsight dict
    for key in keys:
        d_bs[key] = []

    # collect data; for each line...
    for idx_coil_sample, idx_line in enumerate(range(start_idx, stop_idx)):
        line = lines[idx_line].split(sep='\t')

        # ...populate the keys of the brainsight-dict
        for idx_key, key in enumerate(d_bs.keys()):
            # standard (string) entries can be appended straightforwardly
            if key in ["Sample Name", "Session Name", "Creation Cause", "Crosshairs Driver", "Date", "Time",
                       "EMG Channels", "Assoc. Target"]:
                d_bs[key].append(line[idx_key])
            # other keys include:  "Loc. X/Y/Z", "EMG Data 1/2", "EMG Peak-to-Peak 1" etc...
            else:
                # each sample of EMG data is separated by a semicolon
                if ";" in line[idx_key]:
                    d_bs[key].append(np.array(line[idx_key].split(';')).astype(float))
                # other non-EMG-data (numeric) entries
                else:
                    # if key was selected for export but no corresponding data could be collected, "(null)" is entered
                    if line[idx_key] != "(null)":
                        d_bs[key].append(float(line[idx_key]))
                    else:
                        d_bs[key].append(float(-1))

            # assemble coil configuration matrix
            if key in ["Loc. X"]:
                m_nnav[0, 3, idx_coil_sample] = float(d_bs[key][-1])
            elif key in ["Loc. Y"]:
                m_nnav[1, 3, idx_coil_sample] = float(d_bs[key][-1])
            elif key in ["Loc. Z"]:
                m_nnav[2, 3, idx_coil_sample] = float(d_bs[key][-1])
            elif key in ["m0n0"]:
                m_nnav[0, 0, idx_coil_sample] = float(d_bs[key][-1])
            elif key in ["m0n1"]:
                m_nnav[1, 0, idx_coil_sample] = float(d_bs[key][-1])
            elif key in ["m0n2"]:
                m_nnav[2, 0, idx_coil_sample] = float(d_bs[key][-1])
            elif key in ["m1n0"]:
                m_nnav[0, 1, idx_coil_sample] = float(d_bs[key][-1])
            elif key in ["m1n1"]:
                m_nnav[1, 1, idx_coil_sample] = float(d_bs[key][-1])
            elif key in ["m1n2"]:
                m_nnav[2, 1, idx_coil_sample] = float(d_bs[key][-1])
            elif key in ["m2n0"]:
                m_nnav[0, 2, idx_coil_sample] = float(d_bs[key][-1])
            elif key in ["m2n1"]:
                m_nnav[1, 2, idx_coil_sample] = float(d_bs[key][-1])
            elif key in ["m2n2"]:
                m_nnav[2, 2, idx_coil_sample] = float(d_bs[key][-1])

            m_nnav[3, 3, idx_coil_sample] = 1

    # transform from brainsight to simnibs space
    ############################################
    if verbose:
        print(f"Transforming coil positions from Brainsight to SimNIBS space")
    print(nii_conform_path)

    m_simnibs = pynibs.nnav2simnibs(fn_exp_nii=nii_exp_path_lst[0][0],
                                    fn_conform_nii=nii_conform_path,
                                    m_nnav=m_nnav,
                                    nnav_system="brainsight",
                                    mesh_approach="headreco",
                                    fiducials=None,
                                    orientation='RAS',
                                    fsl_cmd=None,
                                    target='simnibs',
                                    temp_dir=temp_dir,
                                    rem_tmp=True,
                                    verbose=verbose)

    # create dictionary containing stimulation and physiological data
    if verbose:
        print(f"Creating dictionary containing stimulation and physiological data")

    current_scaling_factor = 1.43 if "current_scaling_factor" not in subject.exp[exp_idx].keys() \
        else subject.exp[exp_idx]["current_scaling_factor"]

    # create output directory (which is going to be persisted to experiment.hdf5)
    d = dict()
    d['coil_0'] = []
    d['coil_1'] = []
    d['coil_mean'] = []
    d['number'] = []
    d['condition'] = []
    d['current'] = []
    d['date'] = []
    d['time'] = []
    d['coil_sn'] = []
    d['patient_id'] = []

    for i in range(n_stims):
        d['coil_0'].append(m_simnibs[:, :, i])
        d['coil_1'].append(np.zeros((4, 4)) * np.NaN)
        d['coil_mean'].append(np.nanmean(np.stack((d['coil_0'][-1],
                                                   d['coil_1'][-1]), axis=2), axis=2))
        d['number'].append(d_bs['Index'][i])
        # Sample Name is unique for each pulse, so no conditions will be detected
        # d['condition'].append(d_bs['Sample Name'][i])
        # Assoc. Target will assignt he same number to pulses that had the same target/marker
        # (despite minor deviations in the true location of the coil after the pulse)
        d['condition'].append(d_bs['Assoc. Target'][i])
        d['current'].append(1 * current_scaling_factor)
        d['date'].append(d_bs["Date"][i])
        d['time'].append(d_bs["Time"][i])
        d['coil_sn'].append(os.path.split(fn_coil)[1])
        d['patient_id'].append(subject.id)

        # add remaining data to keys that have not aleady been added or that should not not be added
        for key in d_bs.keys():
            if key not in ['Sample Name', 'Session Name', 'Index',
                           'Loc. X', 'Loc. Y', 'Loc. Z',
                           'm0n0', 'm0n1', 'm0n2',
                           'm1n0', 'm1n1', 'm1n2',
                           'm2n0', 'm2n1', 'm2n2',
                           'Date', 'Time'] and \
                    not (key.startswith('EMG Peak-to-peak') or
                         key.startswith('EMG Data')):

                try:
                    d[key].append(d_bs[key][i])
                except KeyError:
                    d[key] = []
                    d[key].append(d_bs[key][i])

    # add physiological raw data
    channels = subject.exp[exp_idx]["channels"]

    if verbose:
        print(f"Postprocessing MEP data")
        if plot:
            print(" Creating MEP plots ...")

    for c_idx, chan_name in enumerate(channels):
        # brainsight indexes channels 1-based
        c_idx += 1

        d[f"mep_raw_data_time_{chan_name}"] = []
        d[f"mep_filt_data_time_{chan_name}"] = []
        d[f"mep_raw_data_{chan_name}"] = []
        d[f"mep_filt_data_{chan_name}"] = []
        d[f"p2p_brainsight_{chan_name}"] = []
        d[f"p2p_{chan_name}"] = []
        d[f"mep_latency_{chan_name}"] = []

        for i in range(n_stims):
            fn_plot = None
            if plot:
                fn_channel = os.path.join(os.path.dirname(fn_tms_nav), "plots", str(chan_name))
                fn_plot = os.path.join(fn_channel, f"mep_{i:04}")
                os.makedirs(fn_channel, exist_ok=True)

            # filter data and calculate p2p values
            p2p, mep_filt_data, latency = pynibs.calc_p2p(sweep=d_bs[f"EMG Data {c_idx}"][i],
                                                          tms_pulse_time=d_bs[f"Offset"][i],
                                                          sampling_rate=1000 / d_bs["EMG Res."][i],
                                                          start_mep=start_mep, end_mep=end_mep,
                                                          measurement_start_time=float(d["EMG Start"][i]),
                                                          fn_plot=fn_plot)

            d[f"mep_raw_data_time_{chan_name}"].append(np.arange(d_bs["EMG Start"][i],
                                                                 d_bs["EMG End"][i], d_bs["EMG Res."][i]))
            d[f"mep_filt_data_time_{chan_name}"].append(
                    np.arange(d_bs["EMG Start"][i], d_bs["EMG End"][i], d_bs["EMG Res."][i]))
            d[f"mep_raw_data_{chan_name}"].append(d_bs[f"EMG Data {c_idx}"][i])
            d[f"mep_filt_data_{chan_name}"].append(mep_filt_data)
            d[f"p2p_brainsight_{chan_name}"].append(d_bs[f"EMG Peak-to-peak {c_idx}"][i])
            d[f"p2p_{chan_name}"].append(p2p)
            d[f"mep_latency_{chan_name}"].append(latency)

    # set filename of experiment.hdf5
    if subject.exp[exp_idx]["fn_exp_hdf5"] is not None or subject.exp[exp_idx]["fn_exp_hdf5"] != []:
        fn_exp_hdf5 = subject.exp[exp_idx]["fn_exp_hdf5"][0]

    elif subject.exp[exp_idx]["fn_exp_csv"] is not None or subject.exp[exp_idx]["fn_exp_csv"] != []:
        fn_exp_hdf5 = subject.exp[exp_idx]["fn_exp_csv"][0]

    elif fn_exp_hdf5 is None or fn_exp_hdf5 == []:
        fn_exp_hdf5 = os.path.join(subject.subject_folder, "exp", exp_idx, "experiment.hdf5")

    # remove coil position outliers (in case of conditions)
    if coil_outlier_corr_cond:
        if verbose:
            print("Removing coil position outliers")
        d = pynibs.coil_outlier_correction_cond(exp=d, outlier_angle=5., outlier_loc=3., fn_exp_out=fn_exp_hdf5)

    # perform coil <-> head distance correction
    if coil_distance_corr:
        if verbose:
            print("Performing coil <-> head distance correction")
        d = pynibs.coil_distance_correction(exp=d,
                                            fn_geo_hdf5=fn_mesh_hdf5,
                                            remove_coil_skin_distance_outlier=remove_coil_skin_distance_outlier,
                                            fn_plot=os.path.split(fn_exp_hdf5)[0])

    d_avg = dict()
    for key in d.keys():
        d_avg[key] = []

    # TODO: This only meaningfully works in conjunction with 'coil_distance_correction', which averages the
    #       coil position within a condition. For each condition, we wil then have 1) and average coil position,
    #       2) an average EMG sample, 3) only 1 full dataset (all but one samples are discarded after averaging)
    if average_emg_data_from_same_condition:
        if verbose:
            print("Averaging samples from the same condition")

        conditions_per_sample = np.array(d['condition'])
        conditions_unique = np.unique(conditions_per_sample)

        # Create new, dedicated dictionary with all EMG data to:
        # 1) collect all EG related keys of the main dictionary
        # 2) convert the stored lists to numpy arrays (for list-based indexing)
        all_emg_data = dict()
        for c_idx, chan_name in enumerate(channels):
            all_emg_data[f"mep_raw_data_{chan_name}"] = np.array(d[f"mep_raw_data_{chan_name}"])
            all_emg_data[f"mep_filt_data_{chan_name}"] = np.array(d[f"mep_filt_data_{chan_name}"])
            all_emg_data[f"p2p_brainsight_{chan_name}"] = np.array(d[f"p2p_brainsight_{chan_name}"])
            all_emg_data[f"p2p_{chan_name}"] = np.array(d[f"p2p_{chan_name}"])

        # create a single entry in the new result dictionary (d_avg) for each condition
        for condition_id in conditions_unique:
            condition_idcs = np.where(conditions_per_sample == condition_id)[0]

            # just copy the first occurrence (within a condition) of non-emg related keys
            if len(condition_idcs) > 0:
                for key in d.keys():
                    if key not in all_emg_data.keys():
                        d_avg[key].append(d[key][condition_idcs[0]])

                # average all emg-related keys of a condition
                for key in all_emg_data.keys():
                    d_avg[key].append(np.mean(all_emg_data[key][condition_idcs], axis=0))

        d = d_avg

    # create dictionary of stimulation data
    d_stim_data = dict()
    d_stim_data["coil_0"] = d["coil_0"]
    d_stim_data["coil_1"] = d["coil_1"]
    d_stim_data["coil_mean"] = d["coil_mean"]
    d_stim_data["number"] = d["number"]
    d_stim_data["condition"] = d["condition"]
    d_stim_data["current"] = d["current"]
    d_stim_data["date"] = d["date"]
    d_stim_data["time"] = d["time"]
    d_stim_data["Creation Cause"] = d["Creation Cause"]
    d_stim_data["Offset"] = d["Offset"]

    # create dictionary of raw physiological data
    d_phys_data_raw = dict()
    d_phys_data_raw["EMG Start"] = d["EMG Start"]
    d_phys_data_raw["EMG End"] = d["EMG End"]
    d_phys_data_raw["EMG Res."] = d["EMG Res."]
    d_phys_data_raw["EMG Channels"] = d["EMG Channels"]
    d_phys_data_raw["EMG Window Start"] = d["EMG Window Start"]
    d_phys_data_raw["EMG Window End"] = d["EMG Window End"]

    for chan in channels:
        d_phys_data_raw[f"mep_raw_data_time_{chan}"] = d[f"mep_raw_data_time_{chan}"]
        d_phys_data_raw[f"mep_raw_data_{chan}"] = d[f"mep_raw_data_{chan}"]

    # create dictionary of postprocessed physiological data
    d_phys_data_postproc = dict()

    for chan in channels:
        d_phys_data_postproc[f"mep_filt_data_time_{chan}"] = d[f"mep_filt_data_time_{chan}"]
        d_phys_data_postproc[f"mep_filt_data_{chan}"] = d[f"mep_filt_data_{chan}"]
        d_phys_data_postproc[f"p2p_brainsight_{chan}"] = d[f"p2p_brainsight_{chan}"]
        d_phys_data_postproc[f"p2p_{chan}"] = d[f"p2p_{chan}"]
        d_phys_data_postproc[f"mep_latency_{chan}"] = d[f"mep_latency_{chan}"]

    # create pandas dataframes from dicts
    df_stim_data = pd.DataFrame.from_dict(d_stim_data)
    df_phys_data_raw = pd.DataFrame.from_dict(d_phys_data_raw)
    df_phys_data_postproc = pd.DataFrame.from_dict(d_phys_data_postproc)

    # save in .hdf5 file
    if verbose:
        print(f"Saving experimental data to file: {fn_exp_hdf5}")
    df_stim_data.to_hdf(fn_exp_hdf5, "stim_data")
    df_phys_data_raw.to_hdf(fn_exp_hdf5, "phys_data/raw/EMG")
    df_phys_data_postproc.to_hdf(fn_exp_hdf5, "phys_data/postproc/EMG")
