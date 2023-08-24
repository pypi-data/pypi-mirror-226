"""Test suite2p motion correction"""
from aind_ophys_pipeline_utils import trace_extraction_utils
from aind_ophys_pipeline_utils.pipeline_util import get_plane, clean_roi_table, add_motion_border
import pytest


@pytest.mark.parametrize(
    "motion_corrected_output",
    [
        ("300um_motion_output.h5"),
    ],
)
def test_create_input_json_capsule(
    motion_corrected_output, ophys_files_capsule_post_process, helper_functions, rois
):
    """Test trace extraction input json"""

    post_process_dir = ophys_files_capsule_post_process
    plane = get_plane(post_process_dir)
    output_dir = helper_functions.create_results_dir(
        "results/", "Other_614171_2023-03-03_12-00-00/"
    )
    motion_corrected_dir = post_process_dir
    input_data = {
        "storage_directory": str(output_dir),
        "motion_corrected_stack": str(motion_corrected_dir / motion_corrected_output),
        "output_json": str(output_dir / f"{plane}um_extract_traces.json"),
        "log_0": str(motion_corrected_dir / "300um_suite2p_rigid_motion_transform.csv"),
        "rois": clean_roi_table(rois),
    }
    expected = add_motion_border(
        str(motion_corrected_dir / "300um_suite2p_rigid_motion_transform.csv"), input_data
    )
    actual = trace_extraction_utils.create_input_json(post_process_dir, output_dir.parent, plane)
    assert actual == expected
