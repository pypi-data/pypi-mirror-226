"""Tests dff_utils"""
import pytest

from aind_ophys_pipeline_utils import dff_utils
from aind_ophys_pipeline_utils.pipeline_util import get_plane


@pytest.mark.parametrize(
    "neuropil_trace_h5, dff_h5, movie_frame_rate_hz",
    [
        ("300um_neuropil_trace.h5", "300um_dff.h5", 30.0),
    ],
)
def test_create_input_json_capsule(
    neuropil_trace_h5,
    dff_h5,
    movie_frame_rate_hz,
    ophys_files_capsule_post_process,
    helper_functions,
):
    """Test dff input json"""
    postprocess_dir = ophys_files_capsule_post_process
    plane = get_plane(postprocess_dir)
    output_dir = helper_functions.create_results_dir(
        "results/", "Other_614171_2023-03-03_12-00-00/"
    )
    expected = {
        "input_file": str(postprocess_dir / neuropil_trace_h5),
        "movie_frame_rate_hz": movie_frame_rate_hz,
        "output_file": str(output_dir / dff_h5),
    }

    actual = dff_utils.create_input_json(postprocess_dir, output_dir.parent, plane)
    assert actual == expected
