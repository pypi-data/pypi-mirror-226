import os

import onnxruntime
import pydload

DATA_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "models")
)

MAX_DOWNLOAD_ATTEMPTS = 10

DETECTOR_MODEL_PATH = os.path.join(DATA_DIR, "detector_model.onnx")
DETECTOR_MODEL_URL = "https://onedrive.live.com/download?cid=C5669415F4DE9E91&resid=C5669415F4DE9E91%21299479&authkey=ADVoe7wRG0KRcUo"

DETECTOR_CLASSES_PATH = os.path.join(DATA_DIR, "detector_classes.onnx")
DETECTOR_CLASSES_URL = "https://onedrive.live.com/download?cid=C5669415F4DE9E91&resid=C5669415F4DE9E91%21299477&authkey=AO1Ekn4UySCrzmk"

CLASSIFIER_MODEL_PATH = os.path.join(DATA_DIR, "classifier_model.onnx")
CLASSIFIER_MODEL_URL = "https://onedrive.live.com/download?cid=C5669415F4DE9E91&resid=C5669415F4DE9E91%21299478&authkey=AATSwER87jN2084"


def load_classifier_model() -> onnxruntime.InferenceSession:
    attempts = MAX_DOWNLOAD_ATTEMPTS
    while not is_file_valid(CLASSIFIER_MODEL_PATH) and attempts > 0:
        attempts -= 1
        download_data(CLASSIFIER_MODEL_URL, CLASSIFIER_MODEL_PATH)
    return onnxruntime.InferenceSession(CLASSIFIER_MODEL_PATH)


def load_detector_model() -> onnxruntime.InferenceSession:
    attempts = MAX_DOWNLOAD_ATTEMPTS
    while not is_file_valid(DETECTOR_MODEL_PATH) and attempts > 0:
        attempts -= 1
        download_data(DETECTOR_MODEL_URL, DETECTOR_MODEL_PATH)
    return onnxruntime.InferenceSession(DETECTOR_MODEL_PATH)


def load_detector_classes() -> list[str]:
    attempts = MAX_DOWNLOAD_ATTEMPTS
    while not is_file_valid(DETECTOR_CLASSES_PATH) and attempts > 0:
        attempts -= 1
        download_data(DETECTOR_CLASSES_URL, DETECTOR_CLASSES_PATH)
    return [c.strip() for c in open(DETECTOR_CLASSES_PATH).readlines() if c.strip()]


def is_file_valid(save_path: str) -> bool:
    return not (not os.path.exists(save_path) or os.path.getsize(save_path) == 0)


def download_data(url: str, save_path: str) -> None:
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    print("Downloading file to " + save_path)
    pydload.dload(
        url, save_to_path=save_path, max_time=1200, verbose=False
    )  # 1200secs = 20mins


def redownload_data() -> None:
    download_data(CLASSIFIER_MODEL_URL, CLASSIFIER_MODEL_PATH)
    download_data(DETECTOR_MODEL_URL, DETECTOR_MODEL_PATH)
    download_data(DETECTOR_CLASSES_URL, DETECTOR_CLASSES_PATH)
