"""Test suite2p motion correction"""
from aind_ophys_pipeline_utils import segmentation_utils
from aind_ophys_pipeline_utils.pipeline_util import get_plane
import pytest


@pytest.mark.parametrize(
    "movie_frame_rate_hz, motion_corrected_output, segmentation_output",
    [
        (30.0, "300um_motion_output.h5", "300um_segmentation_output.json"),
    ],
)
def test_create_input_json_capsule(
    movie_frame_rate_hz,
    motion_corrected_output,
    segmentation_output,
    helper_functions,
    ophys_files_capsule_post_process,
):
    """Test segmentation input json"""
    post_process_dir = ophys_files_capsule_post_process
    output_dir = helper_functions.create_results_dir(
        "results/", "Other_614171_2023-03-03_12-00-00/"
    )
    plane = get_plane(post_process_dir)
    expected = {
        "suite2p_args": {
            "h5py": str(post_process_dir / motion_corrected_output),
            "tmp_dir": "/scratch",
            "movie_frame_rate_hz": movie_frame_rate_hz,
        },
        "postprocess_args": {
            "motion_corrected_video": str(post_process_dir / motion_corrected_output),
            "output_json": str(output_dir / segmentation_output),
        },
    }
    actual = segmentation_utils.create_input_json(post_process_dir, output_dir.parent, plane)
    assert actual == expected
