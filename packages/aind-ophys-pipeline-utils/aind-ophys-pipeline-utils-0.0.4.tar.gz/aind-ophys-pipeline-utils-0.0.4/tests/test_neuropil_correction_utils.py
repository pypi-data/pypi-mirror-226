"""Tests neuropil_correction_utils"""
import pytest

from aind_ophys_pipeline_utils import neuropil_correction_utils
from aind_ophys_pipeline_utils.pipeline_util import get_plane


@pytest.mark.parametrize(
    "neuropil_trace_h5, roi_trace_h5, neuropil_trace_output_json",
    [
        ("300um_neuropil_trace.h5", "300um_roi_traces.h5", "300um_neuropil_trace_output.json"),
    ],
)
def test_create_input_json(
    neuropil_trace_h5,
    roi_trace_h5,
    neuropil_trace_output_json,
    ophys_files_capsule_post_process,
    helper_functions,
):
    """Test neuropil correction input json"""
    postprocess_dir = ophys_files_capsule_post_process
    plane = get_plane(postprocess_dir)
    output_dir = helper_functions.create_results_dir(
        "results/", "Other_614171_2023-03-03_12-00-00/"
    )
    expected = {
        "neuropil_trace_file": str(postprocess_dir / neuropil_trace_h5),
        "roi_trace_file": str(postprocess_dir / roi_trace_h5),
        "storage_directory": str(output_dir),
        "output_json": str(output_dir / neuropil_trace_output_json),
    }

    actual = neuropil_correction_utils.create_input_json(postprocess_dir, output_dir.parent, plane)
    assert actual == expected
