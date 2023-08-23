"""suite2p motion utility"""
import glob
import os
from pathlib import Path

from aind_ophys_pipeline_utils.pipeline_util import (
    make_output_directory,
    get_frame_rate_platform_json,
)


def get_base_dir(input_dir: Path) -> str:
    """Returns base directory from input directory specific to this action
    (i.e. suite2p motion correction)

    Args:
        input_dir (Path): path to data directory

    Returns:
        str: base directory
    """
    return str(input_dir.parent.parent.parent)


def create_input_json(input: str, output_dir: str, plane: str) -> dict:
    """Generates suite2p motion correction input json for a given plane

    Args:
        input (str): path to data directory or path to raw movie
        output_dir (str): path to results directory
        plane (int, optional): Plane to process if session directory is passed. Defaults to None.

    Returns:
        dict: suite2p motion correction input json
    """
    try:
        h5_file = glob.glob(f"{input}/Other_[0-9]*/Other/ophys/planes/{plane}/*um.h5")[0]
        base_dir = input
    except IndexError:
        h5_file = input
        base_dir = get_base_dir(Path(input))
    output_dir = make_output_directory(output_dir, h5_file)

    frame_rate_hz = get_frame_rate_platform_json(base_dir)
    return {
        "h5py": h5_file,
        "movie_frame_rate_hz": frame_rate_hz,
        "motion_corrected_output": os.path.join(output_dir, f"{plane}um_suite2p_motion_output.h5"),
        "motion_diagnostics_output": os.path.join(
            output_dir, f"{plane}um_suite2p_rigid_motion_transform.csv"
        ),
        "max_projection_output": os.path.join(
            output_dir, f"{plane}um_suite2p_maximum_projection.png"
        ),
        "avg_projection_output": os.path.join(
            output_dir, f"{plane}um_suite2p_average_projection.png"
        ),
        "registration_summary_output": os.path.join(
            output_dir, f"{plane}um_suite2p_registration_summary.png"
        ),
        "motion_correction_preview_output": os.path.join(
            output_dir, f"{plane}um_suite2p_motion_preview.webm"
        ),
        "output_json": os.path.join(output_dir, f"{plane}um_suite2p_motion_correction_output.json"),
    }
