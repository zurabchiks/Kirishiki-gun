"""
-------------------------------------------------
   @File Name:     config.py
   @Author:        Siplusplusov (KIRISHIKI TEAM)
   @Date:          2023/11/16
   @Description: Config file type
-------------------------------------------------
"""

from pathlib import Path
import sys

# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the current working directory
ROOT = root_path.relative_to(Path.cwd())


# Source
SOURCES_LIST = ["Image", "Video", "Webcam"]

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'ex.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'ex_det.jpg'

# DL model config
DETECTION_MODEL_DIR = ROOT / 'weights' / 'detection'
SEGMENT_MODEL_DIR = ROOT / 'weights' / 'segment'
POSE_MODEL_DIR = ROOT / 'weights' / 'pose'

YOLOv8s = DETECTION_MODEL_DIR / "yolov8s.pt"
YOLOv8m = DETECTION_MODEL_DIR / "yolov8m.pt"
YOLOv8l = DETECTION_MODEL_DIR / "yolov8l.pt"

DETECTION_MODEL_LIST = [
    "yolov8s.pt",
    "yolov8m.pt",
    "yolov8l.pt"]

SEGMENT_MODEL_LIST = [
    "yolov8l.pt"]