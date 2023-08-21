import os
import pydload
import onnxruntime

DATA_DIR=os.path.normpath(os.path.join(os.path.dirname(__file__), '..', "models"))

DETECTOR_MODEL_PATH=os.path.join(DATA_DIR, 'detector_model.onnx')
DETECTOR_MODEL_URL='https://onedrive.live.com/download?cid=C5669415F4DE9E91&resid=C5669415F4DE9E91%21299479&authkey=ADVoe7wRG0KRcUo'

DETECTOR_CLASSES_PATH=os.path.join(DATA_DIR, 'detector_classes.onnx')
DETECTOR_CLASSES_URL='https://onedrive.live.com/download?cid=C5669415F4DE9E91&resid=C5669415F4DE9E91%21299477&authkey=AO1Ekn4UySCrzmk'

CLASSIFIER_MODEL_PATH=os.path.join(DATA_DIR, 'classifier_model.onnx')
CLASSIFIER_MODEL_URL='https://onedrive.live.com/download?cid=C5669415F4DE9E91&resid=C5669415F4DE9E91%21299478&authkey=AATSwER87jN2084'
        
def load_classifier_model():
    if not os.path.exists(CLASSIFIER_MODEL_PATH):
        download_data(CLASSIFIER_MODEL_URL, CLASSIFIER_MODEL_PATH)
    data = onnxruntime.InferenceSession(CLASSIFIER_MODEL_PATH)
    return data

def load_detector_model():
    if not os.path.exists(DETECTOR_MODEL_PATH):
        download_data(DETECTOR_MODEL_URL, DETECTOR_MODEL_PATH)
    data = onnxruntime.InferenceSession(DETECTOR_MODEL_PATH)
    return data

def load_detector_classes():
    if not os.path.exists(DETECTOR_CLASSES_PATH):
        download_data(DETECTOR_CLASSES_URL, DETECTOR_CLASSES_PATH)
    data = [c.strip() for c in open(DETECTOR_CLASSES_PATH).readlines() if c.strip()]
    return data

def download_data(url, save_path):
    if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
    print("Downloading file to " + save_path)
    try:
        pydload.dload(url, save_to_path=save_path, max_time=None)
    except:
        print("An exception occured during the download.")
