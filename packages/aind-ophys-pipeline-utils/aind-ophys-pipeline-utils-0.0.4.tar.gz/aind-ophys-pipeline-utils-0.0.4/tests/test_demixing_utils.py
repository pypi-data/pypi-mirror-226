"""Tests demixing_utils"""
import pytest
import os

from aind_ophys_pipeline_utils import demixing_utils
from aind_ophys_pipeline_utils.pipeline_util import (
    get_plane,
    read_h5,
    remove_roi_nan,
    write_h5,
    read_json,
)


@pytest.mark.parametrize(
    "motion_corrected_output, roi_trace_h5, extract_traces_v2_json",
    [("300um_motion_output.h5", "300um_roi_traces.h5", "300um_extract_traces_v2.json")],
)
def test_create_input_json_capsule(
    motion_corrected_output,
    roi_trace_h5,
    extract_traces_v2_json,
    ophys_files_capsule_post_process,
    helper_functions,
):
    """Test demixing input json"""
    postprocess_dir = ophys_files_capsule_post_process
    motion_corrected_fn = postprocess_dir / motion_corrected_output
    plane = get_plane(postprocess_dir)
    output_dir = helper_functions.create_results_dir(
        "results/", "Other_614171_2023-03-03_12-00-00/"
    )
    os.makedirs("./scratch", exist_ok=True)
    roi_traces = postprocess_dir / roi_trace_h5
    extract_traces = postprocess_dir / extract_traces_v2_json
    rois = read_h5(roi_traces, "data", "roi_names")
    roi_data = rois["data"]
    roi_names = rois["roi_names"]
    traces = read_json(extract_traces)
    mod_roi_data, _ = remove_roi_nan(traces, roi_names, roi_data)
    write_h5("./scratch/roi_traces.h5", roi_names=roi_names, data=mod_roi_data)
    expected = {
        "movie_h5": str(motion_corrected_fn),
        "traces_h5": "./scratch/roi_traces.h5",
        "output_file": str(output_dir / f"{plane}um_demixing_output.h5"),
        "output_json": str(output_dir / f"{plane}um_demixing_output.json"),
        "roi_masks": traces,
    }

    actual = demixing_utils.create_input_json(postprocess_dir, output_dir.parent, plane)
    assert actual == expected
