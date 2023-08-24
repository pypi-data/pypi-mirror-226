"""Neuropil correction utility"""
import glob
import os

from aind_ophys_pipeline_utils.pipeline_util import (
    make_output_directory,
)


def create_input_json(input_dir: str, output_dir: str, plane: str) -> dict:
    """Creates input json for neuropil trace processing

    Args:
        input_dir (str): input directory, data directory (co)
        output_dir (str): output directory, results directory (co)
        plane (str): plane depth

    Returns:
        dict: input json for neuropil trace processing
    """
    try:
        neuropil_trace = glob.glob(
            f"{input_dir}/Other_[0-9]*/Other/ophys/planes/{plane}/*neuropil_trace.h5"
        )[0]
    except IndexError:
        neuropil_trace = glob.glob(f"{input_dir}/*neuropil_trace.h5")[0]
    try:
        roi_traces = glob.glob(
            f"{input_dir}/Other_[0-9]*/Other/ophys/planes/{plane}/*roi_traces.h5"
        )[0]
    except IndexError:
        roi_traces = glob.glob(f"{input_dir}/*roi_traces.h5")[0]
    output_dir = make_output_directory(output_dir, neuropil_trace)
    input_data = dict(
        neuropil_trace_file=neuropil_trace,
        roi_trace_file=roi_traces,
        storage_directory=output_dir,
        output_json=os.path.join(output_dir, f"{plane}um_neuropil_trace_output.json"),
    )

    return input_data
