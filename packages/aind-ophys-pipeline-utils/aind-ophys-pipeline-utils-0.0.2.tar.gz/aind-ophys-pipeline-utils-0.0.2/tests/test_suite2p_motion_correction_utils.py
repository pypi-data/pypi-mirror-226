"""Test suite2p motion correction"""
from aind_ophys_pipeline_utils import suite2p_motion_correction_utils
from aind_ophys_pipeline_utils.pipeline_util import get_plane
import pytest


@pytest.mark.parametrize(
    "movie_frame_rate_hz, motion_corrected_output, \
        motion_diagnostics_output, max_projection_output, \
        avg_projection_output, registration_summary_output, \
        motion_correction_preview_output, output_json",
    [
        (
            30.0,
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
def test_create_input_json_capsule(
    movie_frame_rate_hz,
    motion_corrected_output,
    motion_diagnostics_output,
    max_projection_output,
    avg_projection_output,
    registration_summary_output,
    motion_correction_preview_output,
    output_json,
    ophys_files_capsule,
    helper_functions,
):
    """Test suite2p motion correction input json"""
    movie_fn, base_dir = ophys_files_capsule
    output_dir = helper_functions.create_results_dir("results/")
    plane = get_plane(base_dir)
    expected = {
        "h5py": str(movie_fn),
        "movie_frame_rate_hz": movie_frame_rate_hz,
        "motion_corrected_output": str(output_dir / plane / motion_corrected_output),
        "motion_diagnostics_output": str(output_dir / plane / motion_diagnostics_output),
        "max_projection_output": str(output_dir / plane / max_projection_output),
        "avg_projection_output": str(output_dir / plane / avg_projection_output),
        "registration_summary_output": str(output_dir / plane / registration_summary_output),
        "motion_correction_preview_output": str(
            output_dir / plane / motion_correction_preview_output
        ),
        "output_json": str(output_dir / plane / output_json),
    }
    actual = suite2p_motion_correction_utils.create_input_json(base_dir, output_dir, plane)
    assert actual == expected


@pytest.mark.parametrize(
    "movie_frame_rate_hz, raw_movie, \
        motion_diagnostics_output, max_projection_output, \
        avg_projection_output, registration_summary_output, \
        motion_correction_preview_output, output_json, \
        motion_corrected_movie_name",
    [
        (
            30.0,
            "300um.h5",
            "300um_suite2p_rigid_motion_transform.csv",
            "300um_suite2p_maximum_projection.png",
            "300um_suite2p_average_projection.png",
            "300um_suite2p_registration_summary.png",
            "300um_suite2p_motion_preview.webm",
            "300um_suite2p_motion_correction_output.json",
            "300um_suite2p_motion_output.h5",
        ),
    ],
)
def test_create_input_json_pipeline(
    movie_frame_rate_hz,
    raw_movie,
    motion_diagnostics_output,
    max_projection_output,
    avg_projection_output,
    registration_summary_output,
    motion_correction_preview_output,
    output_json,
    motion_corrected_movie_name,
    ophys_files_pipeline,
    helper_functions,
):
    """Test suite2p motion correction input json"""
    motion_corrected_output, base_dir = ophys_files_pipeline
    output_dir = helper_functions.create_results_dir("results/")
    plane = get_plane(base_dir)
    raw_movie_path = motion_corrected_output.parent / raw_movie
    expected = {
        "h5py": str(raw_movie_path),
        "movie_frame_rate_hz": movie_frame_rate_hz,
        "motion_corrected_output": str(output_dir / motion_corrected_movie_name),
        "motion_diagnostics_output": str(output_dir / motion_diagnostics_output),
        "max_projection_output": str(output_dir / max_projection_output),
        "avg_projection_output": str(output_dir / avg_projection_output),
        "registration_summary_output": str(output_dir / registration_summary_output),
        "motion_correction_preview_output": str(output_dir / motion_correction_preview_output),
        "output_json": str(output_dir / output_json),
    }
    actual = suite2p_motion_correction_utils.create_input_json(base_dir, output_dir, plane)
    assert actual == expected
