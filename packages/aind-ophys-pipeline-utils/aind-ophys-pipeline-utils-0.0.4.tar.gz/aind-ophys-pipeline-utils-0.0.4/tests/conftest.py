"""conftest for testing aind-ophys-pipeline-utility"""
from typing import Union
from pathlib import Path
import tempfile

import h5py
import pytest
import json

# import atexit
# import shutil

import numpy as np


class HelperFunctions(object):
    """Helper functions for directoy and file creation"""

    @staticmethod
    def raw_movie_and_platform_dir(child_dir: Union[str, Path]):
        """
        Create a temporary directory to write data to

        """
        temp_dir = tempfile.mkdtemp()
        base_dir = Path(temp_dir)
        base_dir = base_dir / child_dir
        base_dir.mkdir()

        full_dir = base_dir / "Other_614171_2023-03-03_12-00-00"
        full_dir.mkdir()
        full_dir = full_dir / "Other"
        full_dir.mkdir()
        platform_dir = full_dir / "ophys"
        platform_dir.mkdir()
        full_dir = platform_dir / "planes"
        full_dir.mkdir()
        full_dir = full_dir / "300"
        full_dir.mkdir()

        return base_dir, platform_dir, full_dir

    @staticmethod
    def create_input_dir(data_dir: Union[str, Path], child_dir: Union[str, Path]):
        """create statndard directory"""
        temp_dir = tempfile.mkdtemp()
        base_dir = Path(temp_dir)
        base_dir = base_dir / data_dir
        base_dir.mkdir()
        base_dir = base_dir / child_dir
        base_dir.mkdir()
        # def remove_temp_dir():
        #     """Remove the temporary directory"""
        #     shutil.rmtree(temp_dir, ignore_errors=True)

        # atexit.register(remove_temp_dir)
        return base_dir

    @staticmethod
    def create_results_dir(results_dir: Union[str, Path], child_dir: Union[str, Path]):
        """
        Create a temporary directory to write data to

        """
        temp_dir = tempfile.mkdtemp()
        base_dir = Path(temp_dir)
        base_dir = base_dir / results_dir
        base_dir.mkdir()
        base_dir = base_dir / child_dir
        return base_dir


@pytest.fixture
def helper_functions():
    """
    See solution to making helper functions available across
    a pytest module in
    https://stackoverflow.com/questions/33508060/create-and-import-helper-functions-in-tests-without-creating-packages-in-test-di
    """
    return HelperFunctions


@pytest.fixture
def platform_json():
    """platform json data for testing"""
    return {"imaging_plane_groups": [{"acquisition_framerate_Hz": 30.0}]}


@pytest.fixture
def rois():
    """segmented roi masks for testing"""
    return [
        {
            "x": 222,
            "y": 365,
            "width": 12,
            "height": 18,
            "mask_matrix": [
                [False, False, False, False, True, True, True, False, False, False, False, False],
                [False, False, False, True, True, True, True, True, False, False, False, False],
                [False, False, False, True, True, True, True, True, True, False, False, False],
                [False, False, False, True, True, True, True, True, True, True, True, False],
                [False, False, False, True, True, True, True, True, True, True, True, True],
                [False, False, True, True, True, True, True, True, True, True, True, True],
                [False, False, True, True, True, True, True, True, True, True, True, True],
                [False, True, True, True, True, True, True, True, True, True, True, True],
                [False, True, True, True, True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True, True, True, True, True],
                [False, True, True, True, True, True, True, True, True, True, True, True],
                [False, True, True, True, True, True, True, True, True, True, True, True],
                [False, False, True, True, True, True, True, True, True, True, True, True],
                [False, False, False, True, True, True, True, True, True, True, True, False],
                [False, False, False, False, True, True, True, True, True, True, True, False],
                [False, False, False, False, False, True, True, True, True, True, False, False],
                [False, False, False, False, False, False, True, True, True, False, False, False],
            ],
            "valid_roi": True,
            "mask_image_plane": 0,
            "exclusion_labels": [],
            "id": 0,
            "max_correction_up": 0,
            "max_correction_down": 0,
            "max_correction_left": 0,
            "max_correction_right": 0,
        },
        {
            "x": 70,
            "y": 273,
            "width": 14,
            "height": 10,
            "mask_matrix": [
                [
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    True,
                    True,
                    True,
                    True,
                    False,
                    False,
                ],
                [
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    False,
                ],
                [
                    False,
                    False,
                    False,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                ],
                [
                    False,
                    False,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                ],
                [
                    False,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                ],
                [
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    False,
                ],
                [
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    False,
                    False,
                ],
                [
                    False,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    False,
                    False,
                    False,
                ],
                [
                    False,
                    False,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    False,
                    False,
                    False,
                    False,
                ],
                [
                    False,
                    False,
                    False,
                    False,
                    False,
                    True,
                    True,
                    True,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                ],
            ],
            "valid_roi": True,
            "mask_image_plane": 0,
            "exclusion_labels": [],
            "id": 1,
            "max_correction_up": 0,
            "max_correction_down": 0,
            "max_correction_left": 0,
            "max_correction_right": 0,
        },
    ]


@pytest.fixture
def roi_trace():
    """roi traces for testing"""
    return {
        "data": [
            np.array([22, 33, 44, 11, 39]).astype(np.float64),
            np.array([22, 33, 44, 11, 39]).astype(np.float64),
        ],
        "roi_names": ["0", "1"],
    }


@pytest.fixture
def extract_traces():
    """extract traces for testing"""
    return {
        "exclusion_labels": [
            {"exclusion_label_name": "motion_border", "roi_id": 0},
            {"exclusion_label_name": "motion_border", "roi_id": 1},
        ]
    }


@pytest.fixture
def rigid_motion_transform():
    """rigid motion transform for testing"""
    return [
        "framenumber,x,y,x_pre_clip,y_preclip,correlation,is_valid\n",
        "0,5,14,5,14,0.01,True\n",
        "1,5,13,5,13,0.012572901,True\n",
    ]


@pytest.fixture
def ophys_files_capsule_pre_process(platform_json):
    """create fileset for capsule testing"""
    base_dir, platform_dir, full_dir = HelperFunctions.raw_movie_and_platform_dir("data/")
    raw_movie_fp = full_dir / "300um.h5"
    with h5py.File(raw_movie_fp, "w") as f:
        f.create_dataset("data", data=np.random.rand(10, 20, 20))
    platform_json_fp = platform_dir / "platform.json"
    with open(platform_json_fp, "w") as f:
        json.dump(platform_json, f)
    return base_dir, full_dir


@pytest.fixture
def ophys_files_capsule_post_process(
    platform_json,
    rois,
    roi_trace,
    extract_traces,
    rigid_motion_transform
):
    """create fileset for capsule testing"""
    post_process_dir = HelperFunctions.create_input_dir(
        "data/", "Other_614171_2023-03-03_12-00-00/"
    )
    platform_json_fp = post_process_dir / "platform.json"
    with open(platform_json_fp, "w") as f:
        json.dump(platform_json, f)
    fn_motion_corrected = post_process_dir / "300um_motion_output.h5"
    with h5py.File(fn_motion_corrected, "w") as f:
        f.create_dataset("data", data=np.random.rand(10, 20, 20))
    rois_fp = post_process_dir / "300um_suite2p_segmentation_postprocess_rois.json"
    print(rois_fp)
    with open(rois_fp, "w") as f:
        json.dump(rois, f)
    rigid_motion_transforms_fp = post_process_dir / "300um_suite2p_rigid_motion_transform.csv"
    with open(rigid_motion_transforms_fp, "w") as f:
        for i in rigid_motion_transform:
            f.write(i)
    roi_traces = post_process_dir / "300um_roi_traces.h5"
    with h5py.File(roi_traces, "w") as f:
        for k, v in roi_trace.items():
            f.create_dataset(k, data=v)
    extract_traces_fp = post_process_dir / "300um_extract_traces_v2.json"
    with open(extract_traces_fp, "w") as f:
        json.dump(extract_traces, f)
    neuropil_trace_h5 = post_process_dir / "300um_neuropil_trace.h5"
    with h5py.File(neuropil_trace_h5, "w") as f:
        f.create_dataset("data", data=np.random.rand(10, 20, 20))
    neuropil_trace_json = post_process_dir / "300um_neuropil_trace_output.json"
    with open(neuropil_trace_json, "w") as f:
        json.dump(platform_json, f)
    return post_process_dir
