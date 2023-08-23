"""dF/F utility"""
import glob
import os

from aind_ophys_pipeline_utils.pipeline_util import (
    make_output_directory,
    get_frame_rate_platform_json,
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
    frame_rate_hz = get_frame_rate_platform_json(input_dir)
    output_dir = make_output_directory(output_dir, neuropil_trace)
    input_data = dict(
        input_file=neuropil_trace,
        movie_frame_rate_hz=frame_rate_hz,
        output_file=os.path.join(output_dir, f"{plane}um_dff.h5"),
    )

    return input_data
