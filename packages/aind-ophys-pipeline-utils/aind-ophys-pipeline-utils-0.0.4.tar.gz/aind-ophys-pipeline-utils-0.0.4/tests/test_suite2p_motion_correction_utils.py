"""Test suite2p motion correction"""
from aind_ophys_pipeline_utils import suite2p_motion_correction_utils
from aind_ophys_pipeline_utils.pipeline_util import get_plane
import pytest


@pytest.mark.parametrize(
    "movie_frame_rate_hz, raw_movie, motion_corrected_output, \
        motion_diagnostics_output, max_projection_output, \
        avg_projection_output, registration_summary_output, \
        motion_correction_preview_output, output_json",
    [
        (
            30.0,
            "300um.h5",
            "300um_suite2p_motion_output.h5",
            "300um_suite2p_rigid_motion_transform.csv",
            "300um_suite2p_maximum_projection.png",
            "300um_suite2p_average_projection.png",
            "300um_suite2p_registration_summary.png",
            "300um_suite2p_motion_preview.webm",
            "300um_suite2p_motion_correction_output.json",
        ),
    ],
)
def test_create_input_json(
    movie_frame_rate_hz,
    raw_movie,
    motion_corrected_output,
    motion_diagnostics_output,
    max_projection_output,
    avg_projection_output,
    registration_summary_output,
    motion_correction_preview_output,
    output_json,
    ophys_files_capsule_pre_process,
    helper_functions,
):
    """Test suite2p motion correction input json"""
    base_dir, full_dir = ophys_files_capsule_pre_process
    output_dir = helper_functions.create_results_dir(
        "results/", "Other_614171_2023-03-03_12-00-00/"
    )
    plane = get_plane(full_dir)
    raw_movie_fp = str(full_dir / raw_movie)
    expected = {
        "h5py": raw_movie_fp,
        "movie_frame_rate_hz": movie_frame_rate_hz,
        "motion_corrected_output": str(output_dir / motion_corrected_output),
        "motion_diagnostics_output": str(output_dir / motion_diagnostics_output),
        "max_projection_output": str(output_dir / max_projection_output),
        "avg_projection_output": str(output_dir / avg_projection_output),
        "registration_summary_output": str(output_dir / registration_summary_output),
        "motion_correction_preview_output": str(output_dir / motion_correction_preview_output),
        "output_json": str(output_dir / output_json),
    }
    # Tests capsule input with only base_dir
    actual_capsule = suite2p_motion_correction_utils.create_input_json(
        base_dir, output_dir.parent, plane
    )
    assert actual_capsule == expected
    # Tests pipeline input with full_dir
    actual_pipeline = suite2p_motion_correction_utils.create_input_json(
        raw_movie_fp, output_dir.parent, plane
    )
    assert actual_pipeline == expected
